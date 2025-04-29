<template>
    <div class="p-6 max-w-6xl mx-auto">
      <div class="mb-6" v-if="user">
        <h1 class="text-2xl font-bold text-gray-800">Hello, {{ user?.username || 'User' }}</h1>
        <p class="text-sm text-gray-500 mt-2">Welcome back! Here's an overview of your 3D work.</p>
      </div>
  
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div class="bg-white shadow rounded-lg p-5 text-center">
          <i class="pi pi-box text-2xl text-blue-500 mb-2"></i>
          <p class="text-gray-500 text-sm">My Models</p>
          <p class="text-xl font-semibold">{{ stats.models }}</p>
        </div>
        <div class="bg-white shadow rounded-lg p-5 text-center">
          <i class="pi pi-chart-line text-2xl text-green-500 mb-2"></i>
          <p class="text-gray-500 text-sm">My Analyses</p>
          <p class="text-xl font-semibold">{{ stats.analyses }}</p>
        </div>
        <div class="bg-white shadow rounded-lg p-5 text-center">
          <i class="pi pi-file text-2xl text-purple-500 mb-2"></i>
          <p class="text-gray-500 text-sm">Reports</p>
          <p class="text-xl font-semibold">{{ stats.reports }}</p>
        </div>
      </div>
  
    
      <div v-if="models.length === 0 && analyses.length === 0" class="bg-white shadow rounded-lg p-8 text-center text-gray-500">
        <i class="pi pi-inbox text-4xl text-blue-300 mb-4"></i>
        <p class="text-lg font-semibold">No models or analyses yet</p>
        <p class="text-sm mt-1">Upload a 3D model to get started with your first analysis!</p>
      </div>
  
      <div v-else>
        <div class="bg-white shadow rounded-lg p-6 mb-6" v-if="models.length > 0">
          <h2 class="text-lg font-semibold text-gray-800 mb-4">Recent Models</h2>
          <table class="w-full text-left text-sm">
            <thead class="text-gray-500 border-b">
              <tr>
                <th>File</th>
                <th>Vertices</th>
                <th>Faces</th>
                <th>Uploaded</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="model in models"
                :key="model.id"
                class="border-b hover:bg-gray-50 [&>td]:py-3"
              >
                <td>{{ model.file_name }}</td>
                <td>{{ model.vertices_count }}</td>
                <td>{{ model.faces_count }}</td>
                <td>{{ new Date(model.uploaded_at).toLocaleString() }}</td>
              </tr>
            </tbody>
          </table>
        </div>
  
        <div class="bg-white shadow rounded-lg p-6" v-if="analyses.length > 0">
          <h2 class="text-lg font-semibold text-gray-800 mb-4">Recent Analyses</h2>
          <ul class="space-y-3">
            <li
              v-for="a in analyses"
              :key="a.id"
              class="p-4 border rounded-lg bg-gray-50 flex justify-between"
            >
              <div>
                <p class="text-sm font-medium">
                  Model id: {{ a.model_file || 'Unknown' }}
                </p>
                <p class="text-xs text-gray-500">
                  Created: {{ new Date(a.created_at).toLocaleString() }}
                </p>
              </div>
              <span
                :class="[ 
                  'text-xs font-semibold px-3 py-1 rounded-full',
                  {
                    'bg-yellow-100 text-yellow-800': a.status === 'pending',
                    'bg-blue-100 text-blue-800': a.status === 'processing',
                    'bg-green-100 text-green-800': a.status === 'completed',
                    'bg-red-100 text-red-800': a.status === 'failed'
                  }
                ]"
              >
                {{ a.status }}
              </span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </template>
  
  
  <script setup>
  import { ref, onMounted , inject} from 'vue'
  import api from '../api' 
  
  const stats = ref({ models: 0, analyses: 0, reports: 0 })
  const models = ref([])
  const analyses = ref([])
  const user = inject("user")
  onMounted(async () => {
    try {
      const [modelRes, analysisRes] = await Promise.all([
        api.get('/model-files/'),
        api.get('/analysis/')
      ])
  
      models.value = modelRes.data.slice(-5).reverse()
      analyses.value = analysisRes.data.slice(-5).reverse()
  
      stats.value.models = modelRes.data.length
      stats.value.analyses = analysisRes.data.length
  
      stats.value.reports = analysisRes.data.reduce((acc, a) => {
        return acc + (a.reports?.length || 0)
      }, 0)
    } catch (err) {
      console.error( 'Error loading dashboard data:', err)
    }
  })
  </script>
  