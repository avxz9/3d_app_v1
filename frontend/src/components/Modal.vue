<template>
    <Teleport to="body">
      <div v-if="isOpen" 
        class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
       
           @click.self="closeModal">
        <div class=" py-6 rounded-lg shadow-lg max-w-[700px]  relative"
           :class="myClass"
        >
          
          <button class="absolute top-3 right-3 text-gray-500 hover:text-gray-800" @click="closeModal">
            ✕
          </button>
  
          <slot></slot>
        </div>
      </div>
    </Teleport>
  </template>
  
  <script setup>

  
  const props = defineProps({
    isOpen: Boolean,
    myClass: {
      type: String,
      default: ""
    } 
  });
  
  const emit = defineEmits(["close"]);
  
  const closeModal = () => {
    emit("close");
  };
  
  
  </script>
  
  