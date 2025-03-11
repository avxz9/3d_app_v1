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


const loaders = {
  obj: new OBJLoader(),
  ply: new PLYLoader(),
  stl: new STLLoader(),
}

onMounted(() => {
  initScene()
  observeResize()
  if (props.currentmodel) loadModel(props.currentmodel)
})

onUnmounted(() => {
  if (renderer) renderer.dispose()
  if (controls) controls.dispose()
})

watch(() => props.currentmodel, (newVal, oldVal) => {
  if (newVal && newVal !== oldVal) loadModel(newVal)
})

const initScene = () => {
  scene = new THREE.Scene()

  camera = new THREE.PerspectiveCamera(45, 1, 0.01, 5000)
  camera.position.set(0, 2, 10)

  renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true })
 
  
  renderer.outputEncoding = THREE.sRGBEncoding
  renderer.toneMapping = THREE.ACESFilmicToneMapping
  renderer.toneMappingExposure = 1
  sceneContainer.value.appendChild(renderer.domElement)

  
  const directionalLight = new THREE.DirectionalLight(0xffffff, 1)
  directionalLight.position.set(5, 10, 7.5)
  scene.add(directionalLight)

  
  scene.add(new THREE.AmbientLight(0x404040))

  controls = new OrbitControls(camera, renderer.domElement)
  controls.autoRotate = true
  controls.autoRotateSpeed = 1.5

  animate()
  updateSize()
}

const observeResize = () =>  {
  const observer = new ResizeObserver(() => updateSize())
  observer.observe(sceneContainer.value)
}

const updateSize = () =>  {
  const w = sceneContainer.value.clientWidth
  const h = sceneContainer.value.clientHeight
  camera.aspect = w / h
  camera.updateProjectionMatrix()
  renderer.setSize(w, h)
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

  loader.load(filePath, obj => {
    const mesh = (ext === 'ply' || ext === 'stl')
      ? new THREE.Mesh(obj, new THREE.MeshStandardMaterial({ color: 0xcccccc, side: THREE.DoubleSide }))
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

    const groupBox = new THREE.Box3().setFromObject(group)
    boundingSphere = new THREE.Sphere()
    groupBox.getBoundingSphere(boundingSphere)

    fitCameraToBoundingSphere(boundingSphere)
    renderer.render(scene, camera)

    emit('loading-end')
    loadingModel = false
  }, undefined, error => {
    console.error('Error loading model:', error)
    emit('loading-end')
    loadingModel = false
  })
}

const fitCameraToBoundingSphere = (sphere) => {
  const fitOffset = 1.1
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
  obj.traverse(child => {
    if (child.geometry) child.geometry.dispose()
    if (child.material) {
      if (Array.isArray(child.material)) child.material.forEach(m => m.dispose())
      else child.material.dispose()
    }
  })
}

const  animate = () =>  {
  requestAnimationFrame(animate)
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
