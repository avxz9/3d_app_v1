<template>
  <div id="app">
    <Navbar />
    
    <Sidebar v-if="sidebarActivated && user" />

    <main 
      :class="[
        'font-sans min-h-[calc(100vh-4rem)] z-10',
       ( route.name === 'login' || route.name === 'register') ? '' : 'px-4 max-w-[1200px] mx-auto mt-[4.0rem]',
        sidebarActivated && user && route.name !== 'login' ? 'lg:ml-[16rem]' : ''
      ]"
    >
      <router-view />
      </main>
  </div>
</template>


<script setup>
import { provide, ref, computed, onMounted, watchEffect } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import Navbar from './components/Navbar.vue';
import Sidebar from './components/Sidebar.vue';
import { api } from './api.js';

const router = useRouter();
const route = useRoute();
const userRole = ref(null); 

const safeParse = (key) => {
  try {
    const item = localStorage.getItem(key);
    return item ? JSON.parse(item) : null;
  } catch (error) {
    console.error(`Error parsing ${key}:`, error);
    return null;
  }
};

const accessToken = ref(localStorage.getItem('accessToken'));
const user = ref(safeParse('user'));
const isLoggedIn = computed(() => {
  const token = localStorage.getItem('accessToken');
  const storedUser = safeParse('user');
  return !!token && !!storedUser;
});

const sidebarActivated = ref(false);

const currentModel = ref(null);
const modelsData = ref([]);
const currentModelData = ref(null);



const fetchUser = async () => {
  if (!accessToken.value) return;

  try {
    const response = await api.get('/auth/profile/');
    
    const userData = response.data;
    userRole.value = userData.role 
    console.log(userRole.value, " is my roole")
    user.value = userData;
    localStorage.setItem('user', JSON.stringify(userData));
    console.log("UserData = " ,userData)
    return userData;
  } catch (error) {
    console.error('Failed to fetch user data:', error);
    logout(); 
    return null;
  }
};

const fetchModels = async () => {
  if (!accessToken.value) return [];

  try {
    const response = await api.get('/model-files/');

    const models = response.data || [];
    modelsData.value = models;
    
    if (models.length > 0) {
      currentModelData.value = models[0];
      currentModel.value = models[0].file_name;
    }
    
    return models;
  } catch (error) {
    console.error('Error fetching models:', error);
    return [];
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
  localStorage.removeItem('accessToken');
  localStorage.removeItem('refreshToken');
  localStorage.removeItem('user');
  
  accessToken.value = null;
  user.value = null;
  userRole.value = null
  modelsData.value = [];
  currentModel.value = null;
  isLoggedIn.value = false
  router.push('/login');
};

onMounted(async () => {
  if (accessToken.value) {
    await fetchUser();
    await fetchModels();
  }
});

watchEffect(() => {
  const storedUser = safeParse('user');
  const storedToken = localStorage.getItem('accessToken');
  
  if (storedUser && storedToken) {
    user.value = storedUser;
  }
});

// Provides
provide('user', user);
provide('userRole', userRole);
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