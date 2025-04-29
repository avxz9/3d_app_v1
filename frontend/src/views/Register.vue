<template>
  <div class="h-[calc(100vh-4rem)] w-full flex flex-col md:flex-row py-12 md:py-0 mt-16">
    <div class="hidden md:flex md:w-1/2 bg-gray-900 justify-center items-start">
      <img
          src="https://images.unsplash.com/photo-1634848577969-bc28ee71ffc1?q=80&w=1528&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        alt="Register visual"
        class="w-full h-full object-cover object-top"
      />
    </div>

    <div class="w-full md:w-1/2 flex items-center justify-center bg-white px-6 py-12">
      <form @submit.prevent="register" class="w-full max-w-md space-y-5 text-center">
        <h1 class="text-3xl font-bold text-gray-800">Register</h1>

        <input
          type="text"
          v-model="form.username"
          placeholder="Username"
          class="w-full border border-gray-300 bg-gray-100 py-2 px-3 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

        <input
          type="email"
          v-model="form.email"
          placeholder="email@example.com"
          class="w-full border border-gray-300 bg-gray-100 py-2 px-3 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

        <input
          type="password"
          v-model="form.pass"
          placeholder="Password"
          class="w-full border border-gray-300 bg-gray-100 py-2 px-3 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

        <input
          type="password"
          v-model="form.repass"
          placeholder="Repeat Password"
          class="w-full border border-gray-300 bg-gray-100 py-2 px-3 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

        <button
          type="submit"
          class="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded transition"
        >
          Register
        </button>

        <p class="text-sm text-gray-600 mt-4">
          Already have an account?
          <router-link to="/login" class="text-blue-600 hover:underline">
            Log in here
          </router-link>
        </p>
      </form>
    </div>
  </div>
</template>

  
<script setup >

  import { reactive} from 'vue';
  import { api } from '../api';
  import { useToast } from 'vue-toastification';
  import { useRouter } from 'vue-router';

  const toast = useToast()
  const router = useRouter()

  const form = reactive({
    username: "",
    email: "",
    pass: "",
    repass: ""
  })


  const register = async () => {
    let valid = true;

    if(form.username === ""){
      alert("Empty username")
      valid = false
    }
    if(form.email === ""){
      alert("empty email")
      valid = false
    }
    if(form.pass === ""){
      alert("empty pass")
      valid = false
    }
    if(form.pass !== form.repass){
      alert("passwords dont match")
      valid = false
    }

    if(valid){
      try{
        const response = await api.post('/auth/register/', {
          username: form.username,
          password: form.pass,
          email: form.email
        });

        form.username = ""
        form.pass = ""
        form.repass=""
        form.email=""


        toast.success("Successfully registered!")
        router.push("/login")

        console.log("Here")
      }
      catch(err)
      {
        if (err.response && err.response.data)
          console.log(err.response.data)
      }
    

    }
  }

</script>