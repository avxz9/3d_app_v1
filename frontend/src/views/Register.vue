<template>
 
 <form
  @submit.prevent="register"
 >

    <div class="max-w-[600px] w-[95%] mx-auto border text-center py-5  mt-8 flex flex-col gap-4">

      
      <h1 class="text-2xl">Register</h1>
      
      <input type="text"  v-model="form.username" placeholder="username" class="w-[80%] border mx-auto py-2 px-2 rounded bg-gray-200/40"/>
      <input type="email" v-model="form.email" placeholder="email@email.com" class="w-[80%] border mx-auto py-2 px-2 rounded bg-gray-200/40"/>
      <input type="password" v-model="form.pass" placeholder="Pass123" class="w-[80%] border mx-auto py-2 px-2 rounded bg-gray-200/40"/>
      <input type="password" v-model="form.repass" placeholder="Pass123" class="w-[80%] border mx-auto py-2 px-2 rounded bg-gray-200/40"/>

      <button type="submit" class="bg-black w-fit px-4 py-2 mx-auto text-white rounded">Register</button>
<!-- 
      <form @submit.prevent="login">
        <input type="text" v-model="username" placeholder="Username" required />
        <input type="password" v-model="password" placeholder="Password" required />
        <button type="submit">Login</button>
      </form> -->
    </div>
  </form>
   
</template>
  
<script setup >
import axios from 'axios';
import { reactive} from 'vue';

import { useRouter } from 'vue-router';
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
        const response = await axios.post('http://localhost:8000/api/register/', {
          username: form.username,
          password: form.pass,
          email: form.email
        });

        form.username = ""
        form.pass = ""
        form.repass=""
        form.email=""


        alert("Succesfully registered ")
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