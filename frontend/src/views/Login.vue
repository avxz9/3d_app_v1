<template>
  <form @submit.prevent="loginUser">
    <div class="max-w-[600px] w-[95%] mx-auto border text-center py-5 mt-8 flex flex-col gap-4">
      <h1 class="text-2xl">Login</h1>
      <input
        type="text"
        v-model="username"
        placeholder="username"
        class="w-[80%] border mx-auto py-2 px-2 rounded bg-gray-200/40"
      />
      <input
        v-model="password"
        type="password"
        placeholder="Pass123"
        class="w-[80%] border mx-auto py-2 px-2 rounded bg-gray-200/40"
      />
      <button type="submit" class="bg-black w-fit px-4 py-2 mx-auto text-white rounded">Login</button>
    </div>
  </form>
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
    router.push("/")
  }
  catch(err ){
    
  }
}
 
</script>
