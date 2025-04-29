<template>


    <div class="p-6 max-w-5xl mx-auto bg-white rounded-lg shadow-sm mt-1">
      <div v-if="analysis">
    
        <div class="border-b pb-4 mb-6">
          <div class="flex justify-between items-center">
            <h2 class="text-3xl font-bold text-gray-800">Analysis #{{ analysis.id }}</h2>
            <button 
              @click="activeModal='report'"
              class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm flex items-center">
              <i class="pi pi-download mr-2"></i>
              Export Report
            </button>
          </div>
        </div>
  
        <!-- Info Cards -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          <!-- Model -->
          <div class="bg-gray-50 p-4 rounded-lg border border-gray-200">
            <div class="flex items-center">
              <div class="bg-blue-100 rounded-full mr-3">
                <i class="pi pi-info-circle text-blue-600 p-2"></i>
              </div>
              <div>
                <p class="text-sm text-gray-500">Model</p>
                <p class="font-semibold">{{ analysis.model_file }}</p>
              </div>
            </div>
          </div>
  
          <!-- Status -->
          <div class="bg-gray-50 p-4 rounded-lg border border-gray-200">
            <div class="flex items-center">
              <div class="bg-green-100 rounded-full mr-3">
                <i class="pi pi-check-circle text-green-600 p-2"></i>
              </div>
              <div>
                <p class="text-sm text-gray-500">Status</p>
                <p :class="[
                  'inline-block px-3 py-1 text-sm rounded-full font-medium mt-1 border capitalize', 
                  {
                    'bg-green-100 text-green-800 border-green-200': analysis.status === 'completed',
                    'bg-yellow-100 text-yellow-800 border-yellow-200': analysis.status === 'pending',
                    'bg-red-100 text-red-800 border-red-200': analysis.status === 'failed',
                    'bg-blue-100 text-blue-800 border-blue-200': analysis.status === 'processing',
                    'bg-gray-100 text-gray-800 border-gray-200': analysis.status === 'no-analysis'
                  }
                ]">
                  {{ analysis.status }}
                </p>
              </div>
            </div>
          </div>
  
          <!-- Date -->
          <div class="bg-gray-50 p-4 rounded-lg border border-gray-200">
            <div class="flex items-center">
              <div class="bg-amber-100 rounded-full mr-3">
                <i class="pi pi-calendar text-amber-600 p-2"></i>
              </div>
              <div>
                <p class="text-sm text-gray-500">Date</p>
                <p class="font-semibold">{{ formatDate(analysis.created_at) }}</p>
              </div>
            </div>
          </div>
        </div>
  
        <!-- Summary -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <div class="bg-gray-50 p-5 rounded-lg border border-gray-200">
            <h3 class="text-lg font-semibold mb-3 text-gray-800">Analysis Summary</h3>
            <div class="space-y-3">
              <div class="flex justify-between items-center pb-2 border-b border-gray-200">
                <span class="text-gray-600">Watertight</span>
                <span class="font-medium flex items-center">
                  {{ analysis.is_watertight ? "Sí" : "No" }}
                </span>
              </div>
              <div class="flex justify-between items-center">
                <span class="text-gray-600">Total defects</span>
                <span class="font-medium text-lg">
                  {{ analysis.defect_count }}
                </span>
              </div>
            </div>
          </div>
  
          <!-- Defect distribution -->
          <div class="bg-gray-50 p-5 rounded-lg border border-gray-200">
            <h3 class="text-lg font-semibold mb-3 text-gray-800">Defect Distribution</h3>
            <div class="h-32 flex items-end justify-around">
              <div
                v-for="severity in ['high', 'medium', 'low']"
                :key="severity"
                class="flex flex-col items-center"
              >
                <div class="text-sm mb-1">{{ getDefectCountBySeverity(severity) }}</div>
                <div
                  :style="{ height: `${Math.max(getDefectPercentageBySeverity(severity), 10)}%` }"
                  :class="`w-12 ${getSeverityColor(severity)} rounded-t`"
                ></div>
                <div class="text-xs mt-2">{{ severity }}</div>
              </div>
            </div>
          </div>
        </div>
  
        <!-- Defect list -->
        <h3 class="text-xl font-semibold mb-4 text-gray-800">Detected Defects</h3>
        <div class="space-y-4">
          <div
            v-for="(defect, index) in analysis.defect_data"
            :key="index"
            class="bg-white p-5 rounded-lg border border-gray-200 shadow-sm hover:shadow-md transition-shadow"
          >
            <div class="flex justify-between">
              <div class="flex items-center">
                <div :class="`w-3 h-3 rounded-full mr-3 ${getSeverityColor(defect.severity)}`"></div>
                <h4 class="font-semibold text-lg">{{ defect.type }}</h4>
              </div>
              <span class="px-3 py-1 text-sm rounded-full font-medium text-gray-700 bg-gray-100">
                {{ defect.points_count }} affected points
              </span>
            </div>
  
            <div class="mt-3 text-gray-600">
              <p class="text-sm">
                <span class="font-medium">Location: </span>
                x={{ defect.location[0].toFixed(2) }},
                y={{ defect.location[1].toFixed(2) }},
                z={{ defect.location[2].toFixed(2) }}
              </p>
              <p class="text-sm mt-1">
                <span class="font-medium">Severity: </span>
                {{ defect.severity }}
              </p>
            </div>
          </div>
        </div>
      </div>
  
      <div v-else class="text-center py-16 text-gray-500">
        <i class="pi pi-search text-4xl mb-4 text-blue-300"></i>
        <p class="text-lg font-semibold">No analysis found for this model.</p>
        <p class="text-sm mt-2">Try uploading and running an analysis to get started.</p>
      </div>
    </div>
  
    <Modal
      :isOpen="activeModal === 'report'"
      @close="closeModal"
      myClass="bg-white w-[90%] max-w-[340px] p-6 rounded-lg"
    >
      <h3 class="text-xl font-semibold mb-4">Export Report</h3>
      <label class="block">
        <span class="text-gray-700">Select Report Format:</span>
        <select
          v-model="chosenFormat"
          class="w-full mt-2 p-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
        >
          <option value="excel">Excel (.xlsx)</option>
          <option value="pdf">PDF (.pdf)</option>
        </select>
      </label>
  
      <div class="flex justify-end mt-6">
        <button
          class="bg-gray-200 text-gray-800 px-4 py-2 rounded-md hover:bg-gray-300 mr-2"
          @click="closeModal"
        >
          Cancel
        </button>
        <button
          class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
          @click="handleExport"
        >
          Export
        </button>
      </div>
    </Modal>

  </template>

<script setup>
import { ref, onMounted, computed, inject , watch} from 'vue';
import { useRoute } from 'vue-router';
import api from '../api';
import Modal from '../components/Modal.vue';

const analysis = ref(null);
const model = ref(null);
const route = useRoute();
const activeModal = ref(null);
const chosenFormat = ref('pdf');

const user = inject('user');

const closeModal = () => {
  activeModal.value = null;
};

const formatDate = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleString();
};

const getSeverityColor = (severity) => {
  switch (severity) {
    case 'high':
      return 'bg-red-500';
    case 'medium':
      return 'bg-yellow-500';
    case 'low':
      return 'bg-blue-500';
    default:
      return 'bg-gray-500';
  }
};

const getDefectCountBySeverity = (severity) => {
  if (!analysis.value?.defect_data) return 0;
  return analysis.value.defect_data.filter((d) => d.severity === severity).length;
};

const getDefectPercentageBySeverity = (severity) => {
  if (!analysis.value?.defect_data || analysis.value.defect_count === 0) return 0;
  const count = getDefectCountBySeverity(severity);
  return (count / analysis.value.defect_count) * 100;
};

const handleExport = () => {
  console.log('Exporting as:', chosenFormat.value);
};

onMounted(async () => {
  try {

    try {
      const res2 = await api.get(`/analysis/${route.params.analysisId}`);
      console.log(res2.data)
      analysis.value = res2.data;
    } catch (err) {
      console.warn("No analysis found for model:", err.response?.status);
      analysis.value = null;
    }

  } catch (error) {
    console.error("Error loading model:", error);
  }
});
</script>
