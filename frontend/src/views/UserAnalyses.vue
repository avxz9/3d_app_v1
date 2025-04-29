<template>
     <div class="mt-32 space-y-6 px-4">
      <h1 class="text-3xl font-bold text-gray-800 mb-4">My Analyses</h1>
  
      <div v-if="analyses.length === 0" class="text-center text-gray-500 mt-10">
        <i class="pi pi-search text-4xl text-blue-300 mb-3"></i>
        <p class="text-lg font-semibold">No analyses found</p>
        <p class="text-sm">Run an analysis to see it here.</p>
      </div>
  
      <div v-else class="grid gap-4">
        <div
           
          v-for="analysis in analyses"
          :key="analysis.id"
          class="bg-white p-4 rounded-lg border shadow-sm flex justify-between items-center hover:bg-gray-100 hover:cursor-pointer"
          @click="goToAnalysis(analysis.id)"
          >
          <div>
            <p class="font-semibold text-gray-800">Model id: {{ analysis.model_file }}</p>
            <p class="text-sm text-gray-500">Created: {{ new Date(analysis.created_at).toLocaleString() }}</p>
          </div>
          <span
            :class="[
              'text-xs font-medium px-3 py-1 rounded-full',
              {
                'bg-yellow-100 text-yellow-800': analysis.status === 'pending',
                'bg-blue-100 text-blue-800': analysis.status === 'processing',
                'bg-green-100 text-green-800': analysis.status === 'completed',
                'bg-red-100 text-red-800': analysis.status === 'failed'
              }
            ]"
          >
            {{ analysis.status }}
          </span>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { onMounted, ref } from 'vue'

  import api from '../api'
  import { useRouter } from 'vue-router'

  const router = useRouter()
  const analyses = ref([])
  
  const goToAnalysis = (id) => {
    router.push(`/analyses/${id}`)
  }

  onMounted(async () => {
    try {
      const res = await api.get('/analysis/')
      analyses.value = res.data
    } catch (err) {
      console.error('Error loading analyses:', err)
      analyses.value = []
    }
  })
  </script>
  