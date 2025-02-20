

<script setup>

import { computed, inject, onBeforeMount, onMounted, ref } from 'vue';

import Modal from '../components/Modal.vue';

import axios from 'axios';
import ThreeModel from '../components/ThreeModel.vue';
import { useRouter } from 'vue-router';

const router = useRouter()

const isLoggedIn = inject('isLoggedIn');
const user = inject('user');
const accessToken = inject('accessToken');
const fetchModels = inject("fetchModels")

const isModalOpen = ref(false);

const openModal = () => {
  isModalOpen.value = true;
};

const closeModal = () => {
  isModalOpen.value = false;
};

const modelsData = ref([
    
])

const currentModel = inject("currentModel")

const handleClick = (v) => {
    currentModel.value = v
}

onMounted( async () => {
    if (isLoggedIn.value && user.value) {
        try {
            const response = await axios.get('http://localhost:8000/api/user/models/',{
            headers: {
                    Authorization: `Bearer ${accessToken.value}`
                }}

            );
            modelsData.value = response.data;
            currentModel.value = modelsData.value[0].file_name
            console.log(currentModel.value)
        } catch (error) {
            console.error("Failed to fetch models:", error);
        }
    }else{
      router.push("/login")
    }
})

const filteredModels = computed(() => {
    return modelsData.value
})

const modelUrl = computed(() => {
  return `http://localhost/models/${user.value.username}/${currentModel.value}`;
});

const generateReport = async () => {
  try {
        const response = await axios.get('http://localhost:8000/api/user/generate-pdf', {
          responseType: 'blob',  
        });

        const blob = new Blob([response.data], { type: 'application/pdf' });

        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = 'generated-file.pdf'; 
        link.click(); 
      } catch (error) {
        console.error('Error fetching PDF:', error);
      }
}

const addModel = async (event) => {
    console.log("Here")
    console.log("in add model")
  const file = event.target.files[0]; 
  if (!file) {
    alert('Please select a valid file.');
    return;
  }

  
  const formData = new FormData();
  formData.append('model_file', file);

  try {
    const response = await axios.post('http://localhost:8000/api/user/upload-model/', formData, {
      headers: {
        Authorization: `Bearer ${accessToken.value}`,
        'Content-Type': 'multipart/form-data',
      },
    });

    modelsData.value.push(response.data);
    console.log('Model added:', response.data);
    await fetchModels()
  } catch (error) {
    console.error('Failed to add model:', error);
  }
};


</script>

<template>
    <p v-if="user && isLoggedIn" class="p-4">Welcome, {{ user.username }}</p>
    <p v-else>Please log in</p>

    <div v-if="user && isLoggedIn" >

        
      <h2 class=" text-center">{{ currentModel }}</h2>
        <div class="flex px-8 flex-wrap justify-center items-start ">
            
                   
            <div class=" my-8 mx-auto w-[80%] max-w-[700px] min-w-[300px] border
              relative z-10 "  v-if="currentModel">
                <ThreeModel  :currentmodel="modelUrl"/> 
            </div>

        </div>

       
        <div class=" flex items-center justify-center gap-4">
          <button class="bg-gray-200 hover:bg-gray-300 px-3 py-2 rounded-md"
            @click="generateReport"
          >Generate Defect Report</button>
          <button class="bg-gray-200 hover:bg-gray-300 px-3 py-2 rounded-md">Display Model Defects</button>
        </div>
        <div class="mx-auto flex flex-col justify-center items-center mt-4 ">


            <div>
              <label for="file"><i class=" pi pi-folder-plus cursor-pointer text-2xl"></i></label>
              <input
                type="file"
                accept=".obj"
                class="border rounded-md px-4 py-2 w-64 mb-2  "
                id="file"
                @change="addModel"
              />
            </div>
            

    </div>

    </div>
  

    <Modal :isOpen="isModalOpen" @close="closeModal">
      
    </Modal>

</template>