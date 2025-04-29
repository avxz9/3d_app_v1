<template>
    <div class="mt-32 space-y-6 px-4">
        <h1 class="text-3xl font-bold text-gray-800">Manage User Models</h1>

        <div>
            <input type="text" placeholder="Search Models..."
                v-model="searchInput"
                class="w-full max-w-md px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>

        <div class="overflow-x-auto">
            <table class="w-full table-auto border-collapse rounded-lg shadow-md bg-white">
                <thead>
                    <tr class="bg-gray-100 text-left text-sm font-semibold text-gray-700">
                        <th class="px-6 py-4">Model name</th>
                        <th class="px-6 py-4">User</th>
                        
                        <th class="px-6 py-4">Last Update</th>
                        <th class="px-6 py-4">Status</th>
                        <th class="px-6 py-4">Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="model in filteredModels" :key="model.id" class="border-b hover:bg-gray-50 transition">
                        <td class="px-6 py-4 text-gray-800">{{ model.file_name}}</td>
                        <td class="px-6 py-4 text-gray-600">{{ model.user  }}</td>
                        <td class="px-6 py-4 text-gray-600">12/12/12</td>
                  
                        <td class="px-6 py-4 text-sm text-gray-500">
                            Analyzed
                        </td>
                        <td class="px-6 py-4 space-x-2">
                            <button
                                class="px-3 py-1 text-sm text-white bg-gray-500 rounded hover:bg-gray-600"
                                    @click="handleShow(model.id)"
                                >Show</button>
                            <button class="px-3 py-1 text-sm text-white bg-red-500 rounded hover:bg-red-600"
                                @click="">Delete</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>

</template>

<script setup>

import { onMounted, ref, computed } from 'vue';
import api from '../api';
import { useRouter } from 'vue-router';

const models = ref([])
const router = useRouter()
const searchInput = ref("")

const filteredModels = computed(() => {
    console.log(models.value)
    const search = searchInput.value.toLowerCase().trim()

    if (!search) return models.value

    return models.value.filter(model =>
    model.file_name.toLowerCase().includes(search))
})


const handleShow = (id) => {
    router.push(`/models/${id}`);
}
onMounted(async () => {
    const res = await api.get("/model-files/all_models/")
    console.log(res.data)
    models.value = res.data
})

</script>