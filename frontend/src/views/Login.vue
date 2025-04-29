<template>
  <div class="h-[calc(100vh-4rem)]  mt-16 w-full flex flex-col md:flex-row py-12 md:py-0">
    <div class="hidden md:flex md:w-1/2 bg-gray-900 items-center justify-center">
      <img
        src="https://images.unsplash.com/photo-1634848577969-bc28ee71ffc1?q=80&w=1528&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        alt="Login visual"
        class="w-full h-full object-cover object-top"
      />
    </div>
    <div class="w-full md:w-1/2 flex items-center justify-center bg-white px-6 py-12">
      <form @submit.prevent="loginUser" class="w-full max-w-md space-y-6 text-center">
        <h1 class="text-3xl text-gray-800 font-bold">Login</h1>

        <input
          type="text"
          v-model="username"
          placeholder="Username"
          class="w-full border border-gray-300 bg-gray-100 py-2 px-4 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

        <input
          v-model="password"
          type="password"
          placeholder="Password"
          class="w-full border border-gray-300 bg-gray-100 py-2 px-4 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

        <button
          type="submit"
          class="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded transition"
        >
          Login
        </button>

        <p class="text-sm text-gray-600 mt-4">
          Don't have an account?
          <router-link to="/register" class="text-blue-600 hover:underline">
            Register here
          </router-link>
        </p>
      </form>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted, inject } from 'vue';
import { useRouter } from 'vue-router';

const isLoggedIn  = inject('isLoggedIn');
const router = useRouter();

const username = ref('');
const password = ref('');
const error = ref(null);

const login = inject("login")

onMounted( () => {
  if(isLoggedIn.value)
    router.push("/")
} )
 
const loginUser = async () => {
  try{
    await login(username.value, password.value);
    router.push("/dashboard")
  }
  catch(err ){
    
  }
}
 
</script>
