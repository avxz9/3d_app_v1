<template>
    <div class="p-6 max-w-5xl mx-auto bg-white rounded-lg shadow-sm mt-1">
     
      <div class="relative w-full h-[400px] rounded-lg overflow-hidden mb-6">
        <div class="w-full h-full" v-if="model">
          <ThreeModel :currentmodel="modelUrl" v-if="modelUrl" />
          <div v-else class="flex items-center justify-center h-full">
            <div class="text-center text-gray-500">
              <i class="pi pi-cube text-5xl mb-2"></i>
              <p>Unable to load 3D model preview</p>
            </div>
          </div>
        </div>
        <div v-else class="flex items-center justify-center h-full">
          <div class="text-center text-gray-500">
            <i class="pi pi-spin pi-spinner text-4xl mb-3"></i>
            <p>Loading model...</p>
          </div>
        </div>
      </div>
      
      <div v-if="model">
        <div class="border-b pb-4 mb-6">
          <div class="flex justify-between items-center">
            <h2 class="text-3xl font-bold text-gray-800">{{ model.file_name }}</h2>
            <div class="flex space-x-2">
              <button 
                @click="downloadModel"
                class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm flex items-center">
                <i class="pi pi-download mr-2"></i>
                Download
              </button>
              <button 
                @click="activeModal='analysis'"
                class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-md text-sm flex items-center">
                <i class="pi pi-check-circle mr-2"></i>
                Run Analysis
              </button>
            </div>
          </div>
        </div>
  
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <!-- File Info -->
          <div class="bg-gray-50 p-4 rounded-lg border border-gray-200">
            <div class="flex items-center">
              <div class="bg-blue-100 rounded-full mr-3">
                <i class="pi pi-file text-blue-600 p-2"></i>
              </div>
              <div>
                <p class="text-sm text-gray-500">File Name</p>
                <p class="font-semibold truncate">{{ model.file_name }}</p>
              </div>
            </div>
          </div>
  
          <!-- Uploader -->
          <div class="bg-gray-50 p-4 rounded-lg border border-gray-200">
            <div class="flex items-center">
              <div class="bg-purple-100 rounded-full mr-3">
                <i class="pi pi-user text-purple-600 p-2"></i>
              </div>
              <div>
                <p class="text-sm text-gray-500">Uploaded By</p>
                <p class="font-semibold">{{ model.user }}</p>
              </div>
            </div>
          </div>
  
          <div class="bg-gray-50 p-4 rounded-lg border border-gray-200">
            <div class="flex items-center">
              <div class="bg-amber-100 rounded-full mr-3">
                <i class="pi pi-calendar text-amber-600 p-2"></i>
              </div>
              <div>
                <p class="text-sm text-gray-500">Upload Date</p>
                <p class="font-semibold">{{ formatDate(model.uploaded_at) }}</p>
              </div>
            </div>
          </div>
  
          <div class="bg-gray-50 p-4 rounded-lg border border-gray-200">
            <div class="flex items-center">
              <div class="bg-green-100 rounded-full mr-3">
                <i class="pi pi-chart-bar text-green-600 p-2"></i>
              </div>
              <div>
                <p class="text-sm text-gray-500">Analyses</p>
                <p class="font-semibold">{{ analysesCount }}</p>
              </div>
            </div>
          </div>
        </div>
  
        <div class="mb-8">
          <h3 class="text-xl font-semibold mb-4 text-gray-800">Geometry Information</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          
            <div class="bg-gray-50 p-5 rounded-lg border border-gray-200">
              <h4 class="text-lg font-medium mb-4">Model Complexity</h4>
              <div class="space-y-4">
                <div>
                  <div class="flex justify-between items-center mb-2">
                    <span class="text-gray-600">Vertices</span>
                    <span class="font-medium">{{ formatNumber(model.vertices_count) }}</span>
                  </div>
                  <div class="w-full bg-gray-200 rounded-full h-2">
                    <div class="bg-blue-600 h-2 rounded-full" :style="{width: getVerticesComplexity()}"></div>
                  </div>
                </div>
                
                <div>
                  <div class="flex justify-between items-center mb-2">
                    <span class="text-gray-600">Faces</span>
                    <span class="font-medium">{{ formatNumber(model.faces_count) }}</span>
                  </div>
                  <div class="w-full bg-gray-200 rounded-full h-2">
                    <div class="bg-green-600 h-2 rounded-full" :style="{width: getFacesComplexity()}"></div>
                  </div>
                </div>
              </div>
            </div>
  
            <div class="bg-gray-50 p-5 rounded-lg border border-gray-200">
              <h4 class="text-lg font-medium mb-4">Analysis History</h4>
              <div v-if="analyses.length > 0" class="h-40">
                <div class="flex h-full items-end justify-around">
                  <div
                    v-for="(analysis, index) in analyses.slice(0, 5)"
                    :key="index"
                    class="flex flex-col items-center mx-1"
                  >
                    <div class="text-xs mb-1">{{ analysis.defect_count }}</div>
                    <div
                      :style="{ height: `${Math.min(Math.max(analysis.defect_count * 5, 10), 100)}%` }"
                      :class="`w-8 ${getStatusColor(analysis.status)} rounded-t`"
                    ></div>
                    <div class="text-xs mt-2 truncate w-16 text-center">{{ formatDate(analysis.created_at, true) }}</div>
                  </div>
                </div>
              </div>
              <div v-else class="flex items-center justify-center h-40 text-gray-500">
                <div class="text-center">
                  <i class="pi pi-chart-line text-3xl mb-2"></i>
                  <p>No analysis history</p>
                </div>
              </div>
            </div>
          </div>
        </div>
  
        <div>
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-xl font-semibold text-gray-800">Recent Analyses</h3>
            <router-link 
              :to="`/analyses/${model.id}`"
              class="text-blue-600 hover:text-blue-800 text-sm flex items-center">
              View All
              <i class="pi pi-arrow-right ml-1"></i>
            </router-link>
          </div>
          
          <div v-if="analyses.length > 0" class="space-y-4">
            <div
              v-for="(analysis, index) in analyses.slice(0, 3)"
              :key="index"
              class="bg-white p-4 rounded-lg border border-gray-200 shadow-sm hover:shadow-md transition-shadow flex justify-between items-center"
            >
              <div class="flex items-center">
                <div :class="`w-3 h-3 rounded-full mr-3 ${getStatusColor(analysis.status)}`"></div>
                <div>
                  <div class="font-medium">Analysis #{{ analysis.id }}</div>
                  <div class="text-sm text-gray-500">{{ formatDate(analysis.created_at) }}</div>
                </div>
              </div>
              
              <div class="flex items-center">
                <span :class="[
                  'inline-block px-3 py-1 text-xs rounded-full font-medium mr-4 border capitalize', 
                  {
                    'bg-green-100 text-green-800 border-green-200': analysis.status === 'completed',
                    'bg-yellow-100 text-yellow-800 border-yellow-200': analysis.status === 'pending',
                    'bg-red-100 text-red-800 border-red-200': analysis.status === 'failed',
                    'bg-blue-100 text-blue-800 border-blue-200': analysis.status === 'processing'
                  }
                ]">
                  {{ analysis.status }}
                </span>
                <router-link :to="`/analyses/${analysis.id}`" class="text-blue-600 hover:text-blue-800">
                  <i class="pi pi-external-link"></i>
                </router-link>
              </div>
            </div>
          </div>
          
          <div v-else class="bg-gray-50 p-8 rounded-lg border border-gray-200 text-center">
            <i class="pi pi-search text-4xl mb-4 text-blue-300"></i>
            <p class="text-lg font-semibold">No analyses found for this model.</p>
            <p class="text-sm mt-2 mb-4">Run your first analysis to get started.</p>
            <button 
              @click="activeModal='analysis'"
              class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-md text-sm">
              Run Analysis
            </button>
          </div>
        </div>
      </div>
  
      <div v-else class="text-center py-16 text-gray-500">
        <i class="pi pi-spin pi-spinner text-4xl mb-4"></i>
        <p class="text-lg font-semibold">Loading model information...</p>
      </div>
    </div>
  
    <Modal
      :isOpen="activeModal === 'analysis'"
      @close="closeModal"
      myClass="bg-white w-[90%] max-w-[380px] p-6 rounded-lg"
    >
      <h3 class="text-xl font-semibold mb-4">Run Defect Analysis</h3>
      <p class="text-gray-600 mb-4">
        Running a defect analysis will scan your model to detect issues.
      </p>
      
      <div class="bg-blue-50 p-4 rounded-lg mb-6 flex">
        <i class="pi pi-info-circle text-blue-600 mr-3 mt-1"></i>
        <div>
          <p class="text-sm text-blue-800">Analysis may take several minutes.</p>
        </div>
      </div>
  
      <div class="flex justify-end mt-6">
        <button
          class="bg-gray-200 text-gray-800 px-4 py-2 rounded-md hover:bg-gray-300 mr-2"
          @click="closeModal"
        >
          Cancel
        </button>
        <button
          class="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700"
          @click="runAnalysis"
        >
          Start Analysis
        </button>
      </div>
    </Modal>
    
  </template>
  
  <script setup>
  import { ref, onMounted, computed, inject } from 'vue';
  import { useRoute, useRouter } from 'vue-router';
  import { useToast } from 'vue-toastification';
  
  
  import api from '../api';
  import Modal from '../components/Modal.vue';
  import ThreeModel from '../components/ThreeModel.vue';
  
  const toast = useToast()
  const model = ref(null);
  const analyses = ref([]);
  const route = useRoute();
  const router = useRouter();
  const activeModal = ref(null);
  const user = inject('user');
  
  const modelUrl = computed(() => {
    if (!user.value || !model.value || !model.value.file_name) return '';
    return `http://localhost/models/${model.value.user}/${model.value.file_name}`;
  });
  
  const analysesCount = computed(() => {
    return analyses.value.length;
  });
  
  const closeModal = () => {
    activeModal.value = null;
  };
  
  const formatDate = (dateString, short = false) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    if (short) {
      return date.toLocaleDateString();
    }
    return date.toLocaleString();
  };
  
  const formatNumber = (number) => {
    return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  };
  
  const getStatusColor = (status) => {
    switch (status) {
      case 'completed':
        return 'bg-green-500';
      case 'processing':
        return 'bg-blue-500';
      case 'pending':
        return 'bg-yellow-500';
      case 'failed':
        return 'bg-red-500';
      default:
        return 'bg-gray-500';
    }
  };
  
  const getVerticesComplexity = () => {
    if (!model.value) return '0%';
    const percentage = Math.min((model.value.vertices_count / 200000) * 100, 100);
    return `${percentage}%`;
  };
  
  const getFacesComplexity = () => {
    if (!model.value) return '0%';
    const percentage = Math.min((model.value.faces_count / 400000) * 100, 100);
    return `${percentage}%`;
  };
  
  const downloadModel = () => {
    if (!model.value) return;
    
    const downloadUrl = modelUrl.value;
    const link = document.createElement('a');
    link.href = downloadUrl;
    link.download = model.value.file_name;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };
  
  const runAnalysis = async () => {
    if (!model.value) return;
    
    try {
        const res = await api.post(`/model-files/${model.value.id}/analyze/`, {}, 
        )
      
      closeModal();
      
      await fetchAnalyses();
      toast.success("Analysis started successfully")


      
    } catch (error) {
      console.error("Error starting analysis:", error);
      
    }
  };
  
  const fetchAnalyses = async () => {
    if (!model.value) return;
    
    try {
      const response = await api.get(`/analysis?modelid=${model.value.id}`);
      analyses.value = response.data || [];
    } catch (error) {
      console.error("Error fetching analyses:", error);
      analyses.value = [];
    }
  };
  
  onMounted(async () => {
    try {
      const res = await api.get(`/model-files/${route.params.modelId}`);
      model.value = res.data;
      await fetchAnalyses();
    } catch (error) {
      console.error("Error loading model:", error);
    }
  });
  </script>