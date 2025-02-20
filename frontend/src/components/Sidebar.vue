<template>
    <div
        class="top-19 left-0 h-[calc(100vh-3.5rem)] hidden sm:w-64 border-r-[1px] shadow-md  fixed 
            z-10  sm:flex flex-col gap-3 px-4 py-4 overflow-y-auto"
    
            >
            <div class="hidden">
              <label for="file"><i class=" pi pi-folder-plus cursor-pointer text-2xl font-[100] text-white"></i></label>
              <input
                    type="file"
                    accept=".obj"
                    class="border rounded-md px-4 py-2 w-64 mb-2 hidden "
                    id="file"
                />
            </div>
        
    

        <template v-if="isLoggedIn">
            <h2 class="text-center bold text-xl">My Models </h2>
            <button v-for="(item,index) in models" :class="[`text-black border  
                rounded-md  bg-gray-200  hover:bg-gray-400  px-4 py-1 flex items-center justify-center`,
                currentIndex === index && 'bg-gray-400']"
                    @click="handleChange(item, index)" >
                <div class="w-[90%] mx-auto truncate ">{{ item.file_name }}</div>
                <div class="text-2xl hover:text-red-600 " @click.stop="handleDelete(item,index)">&times;</div>
            </button>
        </template>
    </div>
</template>


<script setup>

    import {inject, ref, computed} from "vue"

    const arr = "ipsum dolor, sit amet consectetur adipisicing elit. Natus distinctio aspernatur this is a new word that im adding".split(" ")
    console.log(arr)

    const models = inject("models")
    const currentModel = inject("currentModel")
    const isLoggedIn = inject("isLoggedIn")
    const currentIndex = ref(0)

    console.log("Models: ", models.value)


    const handleDelete = (item, index) => {
        // TODO: Handle this in backend

        const answer = confirm("Are you sure you want to delete this model?")

        if(answer)
            models.value.splice(index, 1)

        console.log("Delete model")
    }

    const handleChange = (item, index) => {
        console.log(item.file_name)
        currentModel.value = item.file_name
        currentIndex.value = index
        console.log(first)
    }

    const modelUrl = computed(() => {
        console.log(currentModel.value)
  return `http://localhost/models/${user.value.username}/${currentModel.value}`;
});
</script>