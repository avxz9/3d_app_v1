<template>
  <div id="app">
    
    
    <Navbar />
    <Sidebar /> 
    <main class="sm:ml-64  p-4 min-h-[calc(100vh-3.5rem)] ">
      <router-view />
    </main>
  </div>
</template>

<script setup>
  import Sidebar from './components/Sidebar.vue';
  import { provide, reactive, ref, onMounted , computed,watch} from 'vue';
  import Navbar from './components/Navbar.vue';
  import { useRouter } from 'vue-router';
  import axios from 'axios';
  const accessToken = ref(localStorage.getItem('accessToken'));
    const user = ref(localStorage.getItem('user') ? JSON.parse(localStorage.getItem('user')) : null);
    const router = useRouter();

    const isLoggedIn = computed(() => !!accessToken.value);  

    const currentModel = ref(null)
    const modelsData = ref([])

    provide("models", modelsData)
    provide("currentModel",currentModel)
    const fetchUser = async () => {
      if (accessToken.value) {
        try {
          const response = await axios.get('http://localhost:8000/api/profile/', {
            headers: {
              Authorization: `Bearer ${accessToken.value}`,
            },
          });
          user.value = response.data;
          
        
          localStorage.setItem('user', JSON.stringify(response.data));
        } catch (error) {
          console.log("Failed to fetch user data", error);
        }
      }
    };


    const fetchModels = async () => {
      const response = await axios.get('http://localhost:8000/api/user/models/',{
            headers: {
                    
                     Authorization: `Bearer ${accessToken.value}`
                }}

            );
            modelsData.value = response.data;
            console.log("Here im adding the models: ")
            currentModel.value = modelsData.value[0].file_name

            console.log("Current model: ", currentModel.value)
            console.log(modelsData.value)
    }

    const login = async (username, password) => {
      try {
        const response = await axios.post('http://localhost:8000/api/login/', {
          username,
          password,
        });
        const { access, refresh } = response.data;

        localStorage.setItem('accessToken', access);
        localStorage.setItem('refreshToken', refresh);
        accessToken.value = access;
        await fetchUser(); 
        await fetchModels()
       
      } catch (error) {
        alert("Bad login credentials")
        console.log("Login failed", error);
      }
    };

    const logout = () => {
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      localStorage.removeItem('user');
      accessToken.value = null;
      user.value = null;
      modelsData.value = null
      router.push('/login');  
    };

    
    onMounted(() => {
      if (accessToken.value) {
        fetchUser();
        fetchModels()
      }
    });

    provide('user', user);
    provide('login', login);
    provide('logout', logout);
    provide('accessToken', accessToken);
    provide('isLoggedIn', isLoggedIn);
    provide("fetchModels", fetchModels)
</script>
