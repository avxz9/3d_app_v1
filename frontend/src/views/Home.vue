<script setup>
  import { RouterLink } from 'vue-router';
  import ThreeModel from '../components/ThreeModel.vue';
</script>

<template>
  <div >
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
          <div class="p-6 border rounded-lg shadow-sm hover:shadow-md transition-shadow duration-200">
            <i class="pi pi-cloud-upload text-4xl text-blue-600"></i>
            <h3 class="font-semibold text-lg mt-3">Easy Upload</h3>
            <p class="text-gray-600 mt-2">Upload your 3D models (.obj, .stl, .ply) with just a few clicks.</p>
          </div>
          <div class="p-6 border rounded-lg shadow-sm hover:shadow-md transition-shadow duration-200">
            <i class="pi pi-eye text-4xl text-green-600"></i>
            <h3 class="font-semibold text-lg mt-3">Fast 3D Viewer</h3>
            <p class="text-gray-600 mt-2">View & interact with your 3D models in real-time with our optimized viewer.</p>
          </div>
          <div class="p-6 border rounded-lg shadow-sm hover:shadow-md transition-shadow duration-200">
            <i class="pi pi-chart-line text-4xl text-purple-600"></i>
            <h3 class="font-semibold text-lg mt-3">Analyze Defects</h3>
            <p class="text-gray-600 mt-2">Identify and fix potential issues in your 3D models before production.</p>
          </div>
        </div>
      </section>

      <section class="mt-16">
        <h2 class="text-2xl sm:text-3xl font-semibold mb-6">View and Analyze your 3D Model</h2>
        <div class="bg-white rounded-lg shadow-md p-4 h-[50vh] w-[80vw] flex relative max-w-[800px] max-h-[500px] items-center justify-center mx-auto">
          <ThreeModel currentmodel="/2.obj" />
        </div>
      </section>

      <section class="mt-16">
        <h2 class="text-2xl sm:text-3xl font-semibold">Supported Formats</h2>
        <p class="text-lg text-gray-600 mt-2">We support: .obj, .stl, .ply</p>
        <div class="mt-6">
          <RouterLink class="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white 
              rounded-md font-medium transition-colors duration-150" to="/login">
            Sign In to Get Started
        </RouterLink>
        </div>
      </section>
    </div>
  </div>

</template>