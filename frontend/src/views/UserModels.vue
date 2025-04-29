<template>
    <div class="mt-32 space-y-6 px-4">
      <h1 class="text-3xl font-bold text-gray-800">Manage Models</h1>
  
      <div class="flex flex-col md:flex-row   justify-between items-start md:items-center gap-4">
        <input
          type="text"
          placeholder="Search Models..."
          v-model="searchInput"
          class="w-full max-w-md px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          @click="activeModal='uploadModel'"
          class="md:ml-4 px-4 py-2 text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition"
        >
          + Add Model
        </button>
      </div>
  
      <form v-if="showForm" @submit.prevent="uploadModel" class="bg-white p-4 rounded-lg shadow space-y-4">
        <label class="block text-sm font-medium text-gray-700">Select a model file (.stl)</label>
        <input
          type="file"
          @change="handleFileChange"
          class="block w-full text-sm text-gray-700 file:mr-4 file:py-2 file:px-4 file:rounded file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
        />
        <button
          type="submit"
          class="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
          :disabled="!selectedFile || loading"
        >
          {{ loading ? 'Uploading...' : 'Upload Model' }}
        </button>
      </form>
  
      <div
        v-if="filteredModels.length === 0"
        class="text-center text-gray-500 bg-white shadow rounded-lg p-10 mt-10"
      >
        <i class="pi pi-database text-4xl text-blue-300 mb-4"></i>
        <p class="text-lg font-semibold">No models found</p>
        <p class="text-sm mt-1">Try uploading a model or adjust your search.</p>
      </div>
  
      <div class="overflow-x-auto" v-else>
        <table class="w-full table-auto border-collapse rounded-lg shadow-md bg-white">
          <thead>
            <tr class="bg-gray-100 text-left text-sm font-semibold text-gray-700">
              <th class="px-6 py-4">Model name</th>
              
              <th class="px-6 py-4 hidden md:table-cell">Uploaded</th>
              <th class="px-6 py-4  hidden md:table-cell">Status</th>
              <th class="px-6 py-4">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="model in filteredModels"
              :key="model.id"
              class="border-b hover:bg-gray-50 transition"
            >
              <td class="px-6 py-4 text-gray-800">{{ model.file_name }}</td>
              <td class="px-6 py-4 text-gray-600  hidden md:table-cell">{{ new Date(model.uploaded_at).toLocaleString() }}</td>
              <td class="px-6 py-4 text-sm text-gray-500  hidden md:table-cell">Analyzed</td>
              <td class="px-6 py-4 space-x-2">
                <button
                  class="px-3 py-1 text-sm text-white bg-gray-500 rounded hover:bg-gray-600"
                  @click="handleShow(model.id)"
                >
                  Show
                </button>
                <button
                  class="px-3 py-1 text-sm text-white bg-red-500 rounded hover:bg-red-600"
                >
                  Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <Modal 
  :isOpen="activeModal === 'uploadModel'" 
  @close="closeModal" 
  myClass="bg-white w-[90%] max-w-[370px] p-6 rounded-lg shadow-lg"
>
  <h2 class="text-xl font-semibold mb-4">Upload 3D Model</h2>

  <div class="mb-5">
    <p class="text-sm text-gray-600 mb-3">Select a 3D model file to upload</p>
    
    <label class="block cursor-pointer">
      <span class="sr-only  ">Choose file</span>
      <input 
        type="file" 
        accept=".ply,.obj,.stl" 
        class="block w-full text-sm text-gray-500
               file:mr-4 file:py-2 file:px-4
               file:rounded-md file:border-0
               file:bg-blue-50 file:text-blue-700
               hover:file:bg-blue-100"
        @change="handleFileChange" 
      />
    </label>
  </div>
  
  <div v-if="selectedFile" class="mb-4 p-3 bg-gray-50 rounded-md">
    <div class="flex items-center">
      <div class="text-sm truncate">
        Selected file: <span class="font-medium">{{ selectedFile.name }}</span>
      </div>
    </div>
  </div>

  <div class="flex justify-end gap-3 mt-6">
    <button 
      @click="closeModal" 
      class="px-4 py-2 text-sm text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-md"
    >
      Cancel
    </button>
    <button 
      :disabled="!selectedFile"
      :class="{ 'opacity-50 cursor-not-allowed': !selectedFile }"
      @click="uploadModel" 
      class="px-4 py-2 text-sm text-white bg-blue-600 hover:bg-blue-700 rounded-md"
    >
      Upload
    </button>
  </div>
</Modal>

  </template>
  
  
  <script setup>
  import { onMounted, ref, computed } from 'vue';
  import api from '../api';
  import { useRouter } from 'vue-router';
  import { useToast } from 'vue-toastification';
  import Modal from '../components/Modal.vue';

  const toast = useToast()
  const router = useRouter();
  const models = ref([]);
  const searchInput = ref("");
  const showForm = ref(false);
  const selectedFile = ref(null);
  const loading = ref(false);
  const activeModal = ref(null)
  
  const closeModal = () => {
    activeModal.value = null
  }

  const filteredModels = computed(() => {
    const search = searchInput.value.toLowerCase().trim();
    if (!search) return models.value;
    return models.value.filter(model =>
      model.file_name.toLowerCase().includes(search)
    );
  });
  
  const handleShow = (id) => {

    router.push(`/models/${id}`);
  };
  
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) selectedFile.value = file
  };
  
  const uploadModel = async () => {
    if (!selectedFile.value) return;
  
    console.log(selectedFile.value)
    loading.value = true;
  
    const formData = new FormData();
    formData.append("model_file", selectedFile.value);
  
    try {
      const res = await api.post("/model-files/", formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });
      models.value.push(res.data); 
      selectedFile.value = null;
      activeModal.value = null
      toast.success("Model loaded successfully.")
    } catch (err) {
      alert("Error uploading file");
      console.error(err);
    } finally {
      loading.value = false;
    }
  };
  
  onMounted(async () => {
    const res = await api.get("/model-files/");
    models.value = res.data;
  });
  </script>
  