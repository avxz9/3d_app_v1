<template>
    <div class="flex flex-col items-center justify-center h-[calc(100vh-6rem)] min-h-[400px]  text-center">
      <h1 class="text-8xl font-bold text-gray-800 mb-8">404</h1>
      <p class="text-3xl text-gray-600 mt-2">Page Not Found</p>
      
      <button
        class="bg-gray-700 hover:bg-black text-white px-4 py-2 rounded mt-4 uppercase"
        @click="goHome" 
      >
        Go To Homepage
      </button>
    </div>
  </template>
  
  <script setup>
  import { useRouter } from 'vue-router';
  const router = useRouter();
  
  const goHome = () => {
    router.push('/');
  };
  </script>
  