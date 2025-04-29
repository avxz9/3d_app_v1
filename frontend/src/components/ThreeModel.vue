<template>
  <div ref="sceneContainer" class="scene-container"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, defineEmits, defineProps } from 'vue'
import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'
import { OBJLoader } from 'three/examples/jsm/loaders/OBJLoader'
import { PLYLoader } from 'three/examples/jsm/loaders/PLYLoader'
import { STLLoader } from 'three/examples/jsm/loaders/STLLoader'

const emit = defineEmits(['loading-start', 'loading-end'])
const props = defineProps({ currentmodel: String })

const sceneContainer = ref(null)
let scene, camera, renderer, controls
let group = null
let boundingSphere = null
let loadingModel = false
let animationFrameId = null
let isVisible = true

// Create loaders only once
const loaders = {
  obj: new OBJLoader(),
  ply: new PLYLoader(),
  stl: new STLLoader(),
}

onMounted(() => {
  initScene()
  observeResize()
  observeVisibility()
  if (props.currentmodel) loadModel(props.currentmodel)
})

onUnmounted(() => {
  cancelAnimationFrame(animationFrameId)
  if (renderer) renderer.dispose()
  if (controls) controls.dispose()
  // Clean up all three.js objects
  if (scene) {
    disposeScene(scene)
  }
})

watch(() => props.currentmodel, (newVal, oldVal) => {
  if (newVal && newVal !== oldVal) loadModel(newVal)
})

const initScene = () => {
  scene = new THREE.Scene()

  camera = new THREE.PerspectiveCamera(45, 1, 0.01, 5000)
  camera.position.set(0, 2, 10)

  // Set renderer with optimized parameters
  renderer = new THREE.WebGLRenderer({ 
    antialias: true, 
    alpha: true,
    powerPreference: 'high-performance',
    precision: 'mediump' // Better performance with medium precision
  })
  
  // Use modern color space setting
  renderer.outputColorSpace = THREE.SRGBColorSpace
  renderer.toneMapping = THREE.ACESFilmicToneMapping
  renderer.toneMappingExposure = 1
  
  // Set pixel ratio with upper limit to prevent performance issues on high-DPI displays
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
  
  sceneContainer.value.appendChild(renderer.domElement)

  // Light setup - simplified with better performance
  const directionalLight = new THREE.DirectionalLight(0xffffff, 1)
  directionalLight.position.set(5, 10, 7.5)
  scene.add(directionalLight)
  
  scene.add(new THREE.AmbientLight(0x404040))

  controls = new OrbitControls(camera, renderer.domElement)
  controls.autoRotate = true
  controls.autoRotateSpeed = 1.5
  controls.enableDamping = true
  controls.dampingFactor = 0.05

  updateSize()
  animate()
}

const observeResize = () => {
  // Use ResizeObserver with debouncing
  let resizeTimer
  const observer = new ResizeObserver(() => {
    clearTimeout(resizeTimer)
    resizeTimer = setTimeout(updateSize, 100)
  })
  observer.observe(sceneContainer.value)
}

const observeVisibility = () => {
  // Pause rendering when component is not visible
  const observer = new IntersectionObserver((entries) => {
    isVisible = entries[0].isIntersecting
    if (isVisible && !animationFrameId) {
      animate()
    }
  }, { threshold: 0.1 })
  
  observer.observe(sceneContainer.value)
}

const updateSize = () => {
  if (!renderer) return
  
  const w = sceneContainer.value.clientWidth
  const h = sceneContainer.value.clientHeight
  camera.aspect = w / h
  camera.updateProjectionMatrix()
  renderer.setSize(w, h, false) 
  if (boundingSphere) fitCameraToBoundingSphere(boundingSphere)
}

const loadModel = (filePath) => {
  if (!filePath || loadingModel) return
  loadingModel = true
  emit('loading-start')

  if (group) {
    scene.remove(group)
    disposeObject(group)
    group = null
    boundingSphere = null
  }

  const ext = filePath.split('.').pop().toLowerCase()
  const loader = loaders[ext]
  if (!loader) {
    console.error('Unsupported file format:', ext)
    emit('loading-end')
    loadingModel = false
    return
  }

  loader.load(filePath, 
    // Success callback
    obj => {
      // Create appropriate material with better performance
      const material = new THREE.MeshStandardMaterial({ 
        color: 0xcccccc, 
        side: THREE.DoubleSide,
        flatShading: true // Better performance with flat shading
      })
      
      const mesh = (ext === 'ply' || ext === 'stl')
        ? new THREE.Mesh(obj, material)
        : obj

      group = new THREE.Group()
      const box = new THREE.Box3().setFromObject(mesh)
      const center = box.getCenter(new THREE.Vector3())
      mesh.position.sub(center)
      group.add(mesh)
      
      const size = box.getSize(new THREE.Vector3())
      const scaleFactor = 5 / Math.max(size.x, size.y, size.z)
      group.scale.setScalar(scaleFactor)

      scene.add(group)

      // Optimize geometry if possible
      mesh.traverse((child) => {
        if (child.geometry) {
          child.geometry.center() // Center geometry for better frustum culling
          if (ext !== 'ply' && ext !== 'stl' && child.geometry.index) {
            child.geometry.setIndex(child.geometry.index) // Ensure indexed geometry for performance
          }
        }
      })

      const groupBox = new THREE.Box3().setFromObject(group)
      boundingSphere = new THREE.Sphere()
      groupBox.getBoundingSphere(boundingSphere)

      fitCameraToBoundingSphere(boundingSphere)
      renderer.render(scene, camera)

      emit('loading-end')
      loadingModel = false
    }, 
    // Progress callback
    (xhr) => {
      // Could emit loading progress here
      // emit('loading-progress', (xhr.loaded / xhr.total) * 100)
    },
    // Error callback
    (error) => {
      console.error('Error loading model:', error)
      emit('loading-end')
      loadingModel = false
    }
  )
}

const fitCameraToBoundingSphere = (sphere) => {
  const fitOffset = 0.8
  const aspect = camera.aspect
  const fovRad = camera.fov * (Math.PI / 180)
  const diam = sphere.radius * 2

  const distV = diam / (2 * Math.tan(fovRad / 2))
  const horizFov = 2 * Math.atan(Math.tan(fovRad / 2) * aspect)
  const distH = diam / (2 * Math.tan(horizFov / 2))

  const distance = fitOffset * Math.max(distV, distH)
  camera.position.set(sphere.center.x, sphere.center.y, sphere.center.z + distance)
  camera.lookAt(sphere.center)
  controls.target.copy(sphere.center)
  controls.update()
}

const disposeObject = (obj) => {
  if (!obj) return
  
  obj.traverse(child => {
    if (child.geometry) {
      child.geometry.dispose()
      child.geometry = null
    }
    
    if (child.material) {
      if (Array.isArray(child.material)) {
        child.material.forEach(m => {
          // Safely dispose material textures
          if (m.map) m.map.dispose()
          if (m.lightMap) m.lightMap.dispose()
          if (m.bumpMap) m.bumpMap.dispose()
          if (m.normalMap) m.normalMap.dispose()
          if (m.specularMap) m.specularMap.dispose()
          if (m.envMap) m.envMap.dispose()
          
          m.dispose()
        })
      } else {
        // Safely dispose material textures
        if (child.material.map) child.material.map.dispose()
        if (child.material.lightMap) child.material.lightMap.dispose()
        if (child.material.bumpMap) child.material.bumpMap.dispose()
        if (child.material.normalMap) child.material.normalMap.dispose()
        if (child.material.specularMap) child.material.specularMap.dispose()
        if (child.material.envMap) child.material.envMap.dispose()
        
        child.material.dispose()
      }
      child.material = null
    }
  })
}

const disposeScene = (scene) => {
  scene.traverse(disposeObject)
  scene = null
}

const animate = () => {
  if (!isVisible) {
    animationFrameId = null
    return
  }
  
  animationFrameId = requestAnimationFrame(animate)
  controls.update()
  renderer.render(scene, camera)
}
</script>

<style scoped>
.scene-container {
  width: 100%;
  height: 100%;
  position: relative;
  cursor: grab;
}
.scene-container canvas {
  width: 100% !important;
  height: 100% !important;
  position: absolute;
  top: 0;
  left: 0;
}
</style>