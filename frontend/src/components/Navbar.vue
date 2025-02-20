<script setup>
import { RouterLink } from 'vue-router';
import { inject, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const isLoggedIn = inject('isLoggedIn');
const logout  = inject("logout")
const router = useRouter()

const handleLogout = () => {
    console.log("In logout")
    logout()
    router.push("/login")
}


</script>


<template>
<nav class="bg-black sticky top-0 left-0 z-100 "  >
    <div class="max-w-[1000px] px-8 mx-auto flex items-center gap-4 z-100">
        <ul class="text-white flex items-center gap-4 h-16">
            <RouterLink to="/">Home</RouterLink>

            <RouterLink to="/login" class="ml-auto hidden md:block" v-if="!isLoggedIn">Login</RouterLink>
            <RouterLink to="/register" class="hidden md:block" v-if="!isLoggedIn">Register</RouterLink>

        </ul>
        
        <button v-if="isLoggedIn" class="text-white  "
            @click="handleLogout"
        >Logout</button>
        
         <div class="md:hidden">
            <i class="pi pi-bars text-white fixed right-8 top-5 text-2xl "></i>
        </div>
    </div>
</nav>
</template>