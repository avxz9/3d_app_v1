<template>
    <div
      class="top-16 left-0 h-[calc(100vh-3.5rem)] sm:w-[16rem] border-r shadow-lg fixed 
             z-10 sm:flex flex-col gap-3 px-4 py-4 overflow-y-auto bg-white"
    >
    
      <div class="hidden">
        <label for="file">
          <i class="pi pi-folder-plus cursor-pointer text-2xl text-gray-500"></i>
        </label>
        <input
          type="file"
          accept=".obj"
          id="file"
          class="hidden"
          @change="handleFileUpload"
        />
      </div>
  
      <template v-if="user">
        <h2 class="text-center font-bold text-xl">My Models</h2>

        <label for="file-upload" class="mb-4 cursor-pointer text-lg 
            text-gray-500 hover:text-black flex items-center gap-2">
            <i class="pi pi-plus"></i>
            <span>Add Model</span>
        </label>
  
        <div v-if="models.length > 0">
          <div
            v-for="(item, index) in models"
            :key="item.id"
            class="flex items-center justify-between border rounded-md px-4 py-1 hover:text-black"
            :class="{ 'text-black font-semibold': currentIndex === index, 'text-gray-600': currentIndex !== index }"
          >
            <button
              class="w-[90%] text-left truncate"
              @click="handleChange(item, index)"
            >
              {{ item.file_name }}
            </button>
  
            <button
              class="text-2xl text-gray-400 hover:text-red-600"
              @click.stop="handleDelete(item, index)"
            >
              &times;
            </button>
          </div>
        </div>
  
        <p v-else class="text-center text-gray-500">No models found.</p>
      </template>
    </div>
  </template>
  
  <script setup>
  import { inject, ref, computed } from "vue";
  import { api } from "../api";
  
  const models = inject("models");
  const currentModel = inject("currentModel");
  const currentModelData = inject("currentModelData");
  const isLoggedIn = inject("isLoggedIn");
  const accessToken = inject("accessToken");
  const user = inject("user")
  const currentIndex = ref(0);
  
  const handleDelete = async (item, index) => {
    const answer = confirm("Are you sure you want to delete this model?");
    if (!answer) return;
  
    try {
      await api.delete(`/model-files/${item.id}/`, {
        headers: {
          Authorization: `Bearer ${accessToken.value}`,
        },
      });
  
      models.value.splice(index, 1);
  
      if (models.value.length === 0) {
        currentModel.value = null;
        currentModelData.value = null;
        currentIndex.value = 0;
      } else if (currentIndex.value === index) {
        currentIndex.value = Math.max(0, index - 1);
        currentModel.value = models.value[currentIndex.value]?.file_name || null;
        currentModelData.value = models.value[currentIndex.value] || null;
      }
    } catch (error) {
      console.error("Failed to delete model:", error);
    }
  };
  
  
  const handleChange = (item, index) => {
    currentModel.value = item.file_name;
    currentModelData.value = item;
    currentIndex.value = index;
  };
  
  
  
  
  </script>
  