<template>
   <div class="mt-32 space-y-6 px-4">
      <h1 class="text-3xl font-bold text-gray-800 mb-4">My Reports</h1>
  
      <div v-if="analyses.length === 0" class="text-center text-gray-500 mt-10">
        <i class="pi pi-file text-4xl text-blue-300 mb-3"></i>
        <p class="text-lg font-semibold">No reports available</p>
        <p class="text-sm">Generate an analysis to download reports.</p>
      </div>
  
      <div v-else class="grid gap-4">
        <div
          v-for="analysis in analyses"
          :key="analysis.id"
          class="bg-white p-4 rounded-lg border shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center"
        >
          <div class="mb-2 md:mb-0">
            <p class="font-semibold text-gray-800">Model id: {{ analysis.model_file }}</p>
            <p class="text-sm text-gray-500">Defects: {{ analysis.defect_count }}</p>
          </div>
          <div class="flex gap-2">
            <a
              @click="generateReport(analysis.model_file, 'pdf')"
              class="px-3 py-2 bg-blue-600 text-white rounded-md text-sm hover:bg-blue-700 cursor-pointer"
            >
              Download PDF
            </a>
            <a
              @click="generateReport(analysis.model_file, 'excel')"
              class="px-3 py-2 bg-green-600 text-white rounded-md text-sm hover:bg-green-700 cursor-pointer" 
            >
              Download Excel
            </a>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { onMounted, ref } from 'vue'
  import api from '../api'
  
  const analyses = ref([])
  

  
const generateReport = async (id, format) => {
  try {
    const response = await api.get(`/model/${id}/report?report_format=${format}`, {
      responseType: "blob", 
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });

    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement("a");
    link.href = url;
    link.download = `report.${format === "excel" ? "xlsx" : "pdf"}`;
    document.body.appendChild(link);
    link.click();
    link.remove();
  } catch (error) {
    console.error('Error fetching PDF:', error);
  }
};


  onMounted(async () => {
    try {
      const res = await api.get('/analysis/')
      analyses.value = res.data.filter(a => a.status === 'completed')
    } catch (err) {
      console.error('Error loading reports:', err)
    }
  })
  </script>
  