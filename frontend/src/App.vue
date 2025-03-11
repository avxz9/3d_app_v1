<template>
  <div id="app">
    <Navbar />
    
    <Sidebar v-if="sidebarActivated" />

    <main 
      :class="[' px-4 sm:px-2 font-sans min-h-[calc(100vh-4rem)] z-10 max-w-[1200px] mx-auto mt-[4.0rem]', 
        { 'ml-[250px]': sidebarActivated }]">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { provide, ref, computed, onMounted, watchEffect } from 'vue';
import { useRouter } from 'vue-router';
import Navbar from './components/Navbar.vue';
import Sidebar from './components/Sidebar.vue';
import { api } from './api.js';

const router = useRouter();


const accessToken = ref(localStorage.getItem('accessToken'));
const user = ref(localStorage.getItem('user') ? JSON.parse(localStorage.getItem('user')) : null);
const isLoggedIn = computed(() => !!accessToken.value);


const sidebarActivated = ref(false);


const currentModel = ref(null);
const modelsData = ref([]);
const currentModelData = ref(null);


const fetchUser = async () => {
  if (!accessToken.value) return;

  try {
    const response = await api.get('/auth/profile/', {
      headers: { Authorization: `Bearer ${accessToken.value}` },
    });
    user.value = response.data;
    localStorage.setItem('user', JSON.stringify(response.data));
  } catch (error) {
    console.error('Failed to fetch user data:', error);
    logout(); 
  }
};

const fetchModels = async () => {
  console.log("Models fetched")
  try {
    const response = await api.get('/model-files/', {
      headers: { Authorization: `Bearer ${accessToken.value}` },
    });

    modelsData.value = response.data || [];
    
    if (modelsData.value.length > 0) {
      currentModelData.value = modelsData.value[0];
      currentModel.value = modelsData.value[0].file_name;
    }
    
  } catch (error) {
    console.error('Error fetching models:', error);
  }
};

const login = async (username, password) => {
  try {
    const response = await api.post('/auth/login/', { username, password });
    const { access, refresh } = response.data;

    localStorage.setItem('accessToken', access);
    localStorage.setItem('refreshToken', refresh);
    accessToken.value = access;

    await fetchUser();
    await fetchModels();
  } catch (error) {
    alert('Invalid login credentials');
    console.error('Login failed:', error);
  }
};


const logout = () => {
  localStorage.clear();
  accessToken.value = null;
  user.value = null;
  modelsData.value = [];
  currentModel.value = null;
  router.push('/login');
};

onMounted(() => {

  if (accessToken.value) {
    fetchUser();
    fetchModels();
  }
});

watchEffect(() => {
  if (isLoggedIn.value) fetchModels();
});

provide('user', user);
provide('login', login);
provide('logout', logout);
provide('accessToken', accessToken);
provide('isLoggedIn', isLoggedIn);
provide('fetchModels', fetchModels);
provide('sidebarActivated', sidebarActivated);
provide('models', modelsData);
provide('currentModel', currentModel);
provide('currentModelData', currentModelData);
</script>
