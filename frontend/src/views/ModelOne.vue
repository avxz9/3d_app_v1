<template>


   <div class="p-6 max-w-5xl mx-auto bg-white rounded-lg shadow-sm mt-6" v-if="analysis">
    <!-- Header section -->
    <div class="border-b pb-4 mb-6">
      <div class="flex justify-between items-center">
        <h2 class="text-3xl font-bold text-gray-800">Análisis #{{ analysis.id }}</h2>
        <button 
          @click="activeModal='report'"
          class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
          Export Report
        </button>
      </div>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
      <div class="bg-gray-50 p-4 rounded-lg border border-gray-200">
        <div class="flex items-center">
          <div class=" bg-blue-100 rounded-full mr-3">
            <i class="pi pi-info-circle text-blue-600 p-2"></i>
          </div>
          <div>
            <p class="text-sm text-gray-500">Model</p>
            <p class="font-semibold">{{ analysis.model_file }}</p>
          </div>
        </div>
      </div>
      
      <div class="bg-gray-50 p-4 rounded-lg border border-gray-200">
        <div class="flex items-center">
  
          <div class=" bg-green-100 rounded-full mr-3">
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
      
      <div class="bg-gray-50 p-4 rounded-lg border border-gray-200">
        <div class="flex items-center">
          <div class=" bg-amber-100 rounded-full mr-3">
            <i class="pi pi-calendar text-amber-600 p-2"></i>
          </div>
          <div>
            <p class="text-sm text-gray-500">Date</p>
            <p class="font-semibold">{{ formatDate(analysis.created_at) }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Additional info -->
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
      
      <div class="bg-gray-50 p-5 rounded-lg border border-gray-200">
        <h3 class="text-lg font-semibold mb-3 text-gray-800">Defect Distribution</h3>
        <div class="h-32 flex items-end justify-around">
          <div v-for="severity in ['high', 'medium', 'low']" :key="severity" class="flex flex-col items-center">
            <div class="text-sm mb-1">{{ getDefectCountBySeverity(severity) }}</div>
            <div 
              :style="{height: `${Math.max(getDefectPercentageBySeverity(severity), 10)}%`}" 
              :class="`w-12 ${getSeverityColor(severity)} rounded-t`">
            </div>
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


  <Modal :isOpen="activeModal === 'report'" @close="closeModal" myClass="bg-white w-[90%] max-w-[400px] p-6 rounded-lg">      
      <h3 class="text-xl font-semibold mb-4">Export Report</h3>
      <label class="block">
        <span class="text-gray-700">Select Report Format:</span>
        <select v-model="chosenFormat" class="w-full mt-2 p-2 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
          <option value="excel">Excel (.xlsx)</option>
          <option value="pdf">PDF (.pdf)</option>
        </select>
      </label>

      <div class="flex justify-end mt-6">
        <button class="bg-gray-200 text-gray-800 px-4 py-2 rounded-md hover:bg-gray-300 mr-2" @click="closeModal">
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
    import { ref, onMounted ,computed} from 'vue'
    import { useRoute } from 'vue-router'
    import api from '../api'
    import Modal from '../components/Modal.vue'
    const analysis = ref(null)
    const model = ref(null)
    const route = useRoute()

    const status = ref("no-analysis")
    const activeModal = ref(null)

    const closeModal = () => {
        activeModal.value = null
    }


    const statusStyle = computed(() => {
    switch (status.value) {
        case 'analyzed':
        return 'bg-green-100 text-green-800 border-green-200';
        case 'pending':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
        case 'failed':
        return 'bg-red-100 text-red-800 border-red-200';
        case 'processing':
        return 'bg-blue-100 text-blue-800 border-blue-200';
        case 'no-analysis':
        default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
    });

    const statusText = computed(() => {
    switch (status.value) {
        case 'analyzed':
        return 'Analyzed';
        case 'pending':
        return 'Pending';
        case 'processing':
        return "Processing"
        case "failed":
        return "Failed"
        case 'no-analysis':
        default:
        return 'No Analysis';
    }
    });
    
    const formatDate = (dateString) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleString();
    };

    const getSeverityColor = (severity) => {
    switch(severity) {
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
    return analysis.value.defect_data.filter(d => d.severity === severity).length;
    };

    const getDefectPercentageBySeverity = (severity) => {
    if (!analysis.value?.defect_data || analysis.value.defect_count === 0) return 0;
    const count = getDefectCountBySeverity(severity);
    return (count / analysis.value.defect_count) * 100;
    };


    const handleExport = () => {
        
    }

    onMounted(async() => {
        console.log(route.params)

        const res = await api.get(`/model-files/${route.params.modelId}`)
        const res2 = await api.get(`/analysis?modelid=${route.params.modelId}`);
        model.value = res.data
        analysis.value = res2.data[0]
        console.log(res.data)
        console.log(res2.data)
    })
</script>