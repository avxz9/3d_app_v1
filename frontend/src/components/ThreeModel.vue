<template>
  <div ref="sceneContainer" class="scene-container"></div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
import { OBJLoader } from 'three/examples/jsm/loaders/OBJLoader';
import { PLYLoader } from 'three/examples/jsm/loaders/PLYLoader';
import { STLLoader } from 'three/examples/jsm/loaders/STLLoader';

const sceneContainer = ref(null);
let renderer, camera, controls, scene, group, currentObject;

const props = defineProps({
  currentmodel: String,
});

onMounted(() => {
  initThreeJS();
  window.addEventListener('resize', onWindowResize);
});

function initThreeJS() {
  scene = new THREE.Scene();
  scene.background = null; 

  camera = new THREE.PerspectiveCamera(
    75,
    sceneContainer.value.clientWidth / sceneContainer.value.clientHeight,
    0.1,
    1000
  );
  camera.position.set(0, 2, 5);

  renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true }); 
  renderer.setPixelRatio(window.devicePixelRatio);
  renderer.setSize(
    sceneContainer.value.clientWidth,
    sceneContainer.value.clientHeight
  );
  sceneContainer.value.appendChild(renderer.domElement);

  controls = new OrbitControls(camera, renderer.domElement);

  
  const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
  directionalLight.position.set(5, 10, 7.5);
  directionalLight.castShadow = true;
  scene.add(directionalLight);


  const ground = new THREE.Mesh(
    new THREE.PlaneGeometry(200, 200),
    new THREE.ShadowMaterial({ opacity: 0.2 })
  );
  ground.rotation.x = -Math.PI / 2;
  ground.receiveShadow = true;
  scene.add(ground);

  loadModel(props.currentmodel);

  animate();
}

function loadModel(filePath) {
  const fileExtension = filePath.split('.').pop().toLowerCase();
  let loader;
  let material;
  let object;

  console.log('Loading model:', filePath);

  switch (fileExtension) {
    case 'obj':
      loader = new OBJLoader();
      break;
    case 'ply':
      loader = new PLYLoader();
      break;
    case 'stl':
      loader = new STLLoader();
      break;
    default:
      console.error('Unsupported file format:', fileExtension);
      return;
  }

  loader.load(
    filePath,
    (geometryOrObject) => {
      console.log('Model loaded successfully:', geometryOrObject);

      if (fileExtension === 'ply' || fileExtension === 'stl') {
        material = new THREE.MeshStandardMaterial({ color: 0x0055ff });

        if (geometryOrObject instanceof THREE.BufferGeometry) {
          object = new THREE.Mesh(geometryOrObject, material);
        } else {
          object = geometryOrObject;
        }
      } else {
        object = geometryOrObject;
      }

      if (group) {
        scene.remove(group);
        if (currentObject && currentObject.geometry) {
          currentObject.geometry.dispose();
        }
        if (currentObject && currentObject.material) {
          if (Array.isArray(currentObject.material)) {
            currentObject.material.forEach((material) => material.dispose());
          } else {
            currentObject.material.dispose();
          }
        }
      }

      currentObject = object;

      group = new THREE.Group();
      const box = new THREE.Box3().setFromObject(currentObject);
      const center = new THREE.Vector3();
      box.getCenter(center);
      const size = new THREE.Vector3();
      box.getSize(size);

      currentObject.position.sub(center);
      group.add(currentObject);

      const maxDimension = Math.max(size.x, size.y, size.z);
      const scaleFactor = 6 / maxDimension;
      group.scale.setScalar(scaleFactor);

   
      scene.add(group);

      controls.target.set(0, 0, 0);
      controls.update();

      renderer.render(scene, camera);
    },
    (xhr) => {
      console.log((xhr.loaded / xhr.total) * 100 + '% loaded');
    },
    (error) => {
      console.error('Error loading model:', error);
    }
  );
}

function onWindowResize() {
  const container = sceneContainer.value;
  const width = container.clientWidth;
  const height = container.clientHeight;

  camera.aspect = width / height;
  camera.updateProjectionMatrix();

  renderer.setSize(width, height);
  renderer.domElement.style.width = '100%';
  renderer.domElement.style.height = '100%';

  controls.target.set(0, 0, 0);
  controls.update();

  renderer.render(scene, camera);
}

watch(
  () => props.currentmodel,
  (newModel) => {
    console.log('Model changed to:', newModel);
    loadModel(newModel);
  }
);

function animate() {
  requestAnimationFrame(animate);
  controls.update();
  renderer.render(scene, camera);
}
</script>

<style scoped>
.scene-container {
  min-width: 300px;
  max-width: 700px;
  height: auto;
  aspect-ratio: 16 / 9;
  margin: 0 auto;
  cursor: grab;
  box-sizing: border-box;
  position: relative;
  z-index: 10;
}

.scene-container canvas {
  width: 100% !important;
  height: 100% !important;
  display: block;
  position: absolute;
  z-index: 10;
  background-color: transparent; 
}

@media (max-width: 768px) {
  .scene-container {
    width: 90%;
    aspect-ratio: 4 / 3;
    border: none;
  }
}

@media (max-width: 480px) {
  .scene-container {
    width: 90%;
    aspect-ratio: 1 / 1;
  }
}
</style>
