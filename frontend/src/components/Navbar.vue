<script setup>
import { RouterLink } from 'vue-router';
import { inject, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';

const isLoggedIn = inject('isLoggedIn');
const logout  = inject("logout")
const router = useRouter()
const route = useRoute()

const handleLogout = () => {
    console.log("In logout")
    logout()
    router.push("/login")
}

const sidebarActivated = inject("sidebarActivated")

const handleSidebarClick = () => {
    sidebarActivated.value = !sidebarActivated.value
}
</script>


<template>
<nav class="bg-black fixed top-0 left-0 z-50  h-16 w-full "  >
    
    <button 
        v-if="isLoggedIn"
    class=" w-fit fixed left-4 top-5  "  @click="handleSidebarClick"><i class="text-white pi pi-folder text-xl "
               
            ></i></button>

        
    <div class="max-w-[1200px] px-8 mx-auto flex items-center gap-4 z-100 ">
        <ul class="text-white flex items-center gap-4 h-16  w-full ">
            <RouterLink to="/"
                class=" ml-8"
                :class="{ 'text-white font-semibold': route.path === '/',
                          'text-gray-300': route.path !== '/' }"
            >Home</RouterLink>

            <RouterLink to="/login" class="ml-auto hidden sm:block " v-if="!isLoggedIn"
                :class="{ 'text-white font-semibold': route.path === '/login',
                          'text-gray-300': route.path !== '/login' }"
            >Login</RouterLink>
            <RouterLink to="/register" class="hidden sm:block" v-if="!isLoggedIn"
                  :class="{ 'text-white font-semibold': route.path === '/register',
                          'text-gray-300': route.path !== '/register' }"
            
            >Register</RouterLink>

        </ul>
        
        <button v-if="isLoggedIn" class="text-white  "
            @click="handleLogout"
        >Logout</button>
        
  
    </div>
</nav>
</template>