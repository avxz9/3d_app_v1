<script setup>
import { computed, inject, ref } from 'vue';
import Modal from '../components/Modal.vue';

import ThreeModel from '../components/ThreeModel.vue';

import { api } from '../api.js';


const isLoggedIn = inject('isLoggedIn');
const user = inject('user');
const accessToken = inject('accessToken');
const fetchModels = inject("fetchModels");
const currentModelData = inject("currentModelData");
const currentModel = inject("currentModel");

const activeModal = ref(null); 
const loading = ref(false); 


const chosenFormat = ref("pdf");

const defects = ref([
  { type: "Holes edges", pressed: false },
  { type: "Non-manifold vertices", pressed: false },
  { type: "Self-Intersections", pressed: false },
  { type: "Isolated components", pressed: false },
  { type: "Poor quality triangles", pressed: false },
  { type: "Noise", pressed: false }
]);

const modelsData = ref([]);

const handleModelLoadingStart = () => {
  loading.value = true;
};

const handleModelLoadingEnd = () => {
  loading.value = false;
};

const openModal = (modalType) => {
  activeModal.value = modalType;
};
const closeModal = () => {
  activeModal.value = null;
};




const modelUrl = computed(() => `http://localhost/models/${user.value.username}/${currentModel.value}`);

const generateReport = async () => {
  try {
    const response = await api.get(`/generate-report/?format=${chosenFormat.value}`, {
      responseType: "blob", 
    });

    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement("a");
    link.href = url;
    link.download = `report.${chosenFormat.value === "excel" ? "xlsx" : "pdf"}`;
    document.body.appendChild(link);
    link.click();
    link.remove();
  } catch (error) {
    console.error('Error fetching PDF:', error);
  }
};

const handleDefectClick = (i) => {
  defects.value[i].pressed = !defects.value[i].pressed;
};

const addModel = async (event) => {
  console.log("in add model");
  const file = event.target.files[0];
  if (!file) {
    alert('Please select a valid file.');
    return;
  }

  const formData = new FormData();
  formData.append('model_file', file);

  try {
    const response = await api.post('/model-files/', formData, {
      headers: {
        Authorization: `Bearer ${accessToken.value}`,
        'Content-Type': 'multipart/form-data'
      }
    });
    modelsData.value.push(response.data);
    console.log('Model added:', response.data);
    await fetchModels();
  } catch (error) {
    console.error('Failed to add model:', error);
  }
};
</script>

<template>
 

  <div v-if="user && isLoggedIn" class="z-0 relative">
     <p class="p-4 mb-4 text-xl">Welcome, {{ user.username }}</p>
    <div class="flex flex-col sm:flex-row justify-between gap-4">
      <div class="flex flex-col gap-2 w-full sm:w-[300px] mt-8">
        <h3 class="font-semibold text-center">Select possible defects</h3>
        <button
          v-for="(defect, index) in defects"
          :key="index"
          @click="handleDefectClick(index)"
          :class="[' py-2 px-1 w-full rounded hover:bg-gray-300', defect.pressed ? 'bg-gray-300' : 'bg-gray-200']">
          {{ defect.type }}
        </button>

        <h2 class="mt-8 text-black text-center font-bold">Model Actions</h2>
        <div class="flex items-center justify-center gap-2 flex-col ">
        <button class="bg-gray-200 hover:bg-gray-300 px-3 py-2 rounded-md w-full" @click="openModal('report')">
          Export Defect Report
        </button>
        <button class="bg-gray-200 hover:bg-gray-300 px-3 py-2 rounded-md w-full" @click="openModal('defects')">
          Display Model Defects
        </button>
      </div>
      </div>

      <div class="flex relative flex-wrap justify-center items-start mb-16 mx-auto w-[100%] h-[500px] 
         overflow-hidden">
        <div class="mx-auto w-full h-full relative z-10 " v-if="currentModel">
          <ThreeModel
            :currentmodel="modelUrl"
            @loading-start="handleModelLoadingStart"
            @loading-end="handleModelLoadingEnd" />
        </div>

        <div v-if="loading" class="absolute inset-0 flex items-center justify-center bg-white/50 z-20 pointer-events-none">
          <div class="animate-spin rounded-full h-16 w-16 border-4 border-gray-300 border-t-gray-600"></div>
        </div>

        <div class="absolute top-4 right-4" v-if="currentModelData">
          Faces: {{ currentModelData.faces_count }} / Vertices: {{ currentModelData.vertices_count }}
        </div>
      </div>
    </div>

    

    <div class="mx-auto flex flex-col justify-center items-center mt-4">
      <div>
        <input type="file"  accept=".obj, .ply, .stl" 
          class="border rounded-md px-4 py-2 w-64 mb-2 hidden" id="file-upload" @change="addModel" />
      </div>
    </div>

    <Modal :isOpen="activeModal === 'default'" @close="closeModal"></Modal>
    <Modal :isOpen="activeModal === 'defects'" @close="closeModal" myClass="bg-white w-[95%] h-[90vh]">
      <div class="w-[100vw] max-w-[500px] h-[400px] mx-auto mt-4">
        <ThreeModel :currentmodel="modelUrl" />
      </div>
    </Modal>
    <Modal :isOpen="activeModal === 'report'" @close="closeModal" myClass="bg-white w-[70%] max-w-[300px] h-[200px] p-4">      
      <label class="block mt-4">
        <span class="text-gray-700">Select Report Format:</span>
        <select v-model="chosenFormat" class="w-full mt-2 p-2 border rounded">
          <option value="excel">Excel (.xlsx)</option>
          <option value="pdf">PDF (.pdf)</option>
        </select>
      </label>

      <button 
        @click="generateReport"
        class="mt-4 bg-gray-200 text-black px-4 py-2 rounded hover:bg-gray-300 w-full">
        Export
      </button>
    </Modal>
  </div>

  
  <div v-else>
    <div class="min-h-screen flex flex-col items-center text-center p-8">
    <section class="max-w-3xl">
      <h1 class="text-4xl md:text-5xl font-bold text-gray-800 font-sans">3D Model Inspector</h1>
      <p class="text-lg text-gray-600 mt-3">
        Upload, view, and analyze 3D models in your browser.
      </p>
      
    </section>

    <section class="mt-12 max-w-4xl">
      <h2 class="text-2xl sm:text-3xl font-semibold">Why Choose Our App?</h2>
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-6 mt-6 mb-4">
        <div class="p-4 border rounded-md shadow">
          <i class="pi pi-cloud-upload text-4xl text-blue-600"></i>
          <h3 class="font-semibold text-lg mt-2">Easy Upload</h3>
          <p class="text-sm text-gray-600">Upload your 3D models <br>(.obj, .stl, .ply).</p>
        </div>
        <div class="p-4 border rounded-md shadow">
          <i class="pi pi-eye text-4xl text-green-600"></i>
          <h3 class="font-semibold text-lg mt-2">Fast 3D Viewer</h3>
          <p class="text-sm text-gray-600">View & interact with your 3D models in real-time.</p>
        </div>
        <div class="p-4 border rounded-md shadow">
          <i class="pi pi-chart-line text-4xl text-purple-600"></i>
          <h3 class="font-semibold text-lg mt-2">Analyze Defects</h3>
          <p class="text-sm text-gray-600">Identify potential issues in your 3D models.</p>
        </div>
      </div>
    </section>

    <section class="mt-12 ">
      <h2 class="text-2xl sm:text-3xl font-semibold">View and Analyze your 3D Model</h2>

      <div class="h-[50vh]  w-[70vw] flex relative max-w-[500px] max-h-[500px]
        items-center justify-center  mx-auto">
        <ThreeModel currentmodel="/2.obj" />
      </div>
    </section>

    

    <section class="mt-12">
      <h2 class="text-2xl sm:text-3xl font-semibold">Supported Formats</h2>
      <p class="text-lg text-gray-600 mt-2">We support: .obj, .stl, .ply</p>
    </section>

    <section class="mt-12">
      
    </section>
  </div>

  </div>


</template>
