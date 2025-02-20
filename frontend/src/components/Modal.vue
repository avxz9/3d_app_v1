<template>
    <Teleport to="body">
      <div v-if="isOpen" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
           @click.self="closeModal">
        <div class="bg-white p-6 rounded-lg shadow-lg max-w-lg w-full relative">
          
          <button class="absolute top-3 right-3 text-gray-500 hover:text-gray-800" @click="closeModal">
            ✕
          </button>
  
          <slot></slot>
        </div>
      </div>
    </Teleport>
  </template>
  
  <script setup>
  import { 
    onMounted, onUnmounted } from "vue";
  
  const props = defineProps({
    isOpen: Boolean, 
  });
  
  const emit = defineEmits(["close"]);
  
  const closeModal = () => {
    emit("close");
  };
  
  const handleEscape = (event) => {
    if (event.key === "Escape") {
      closeModal();
    }
  };
  
  onMounted(() => window.addEventListener("keydown", handleEscape));
  onUnmounted(() => window.removeEventListener("keydown", handleEscape));
  </script>
  
  