<template>
    <div class="mt-32 space-y-6 px-4">
        <h1 class="text-3xl font-bold text-gray-800">Manage Users</h1>

        <div>
            <input type="text" placeholder="Search user..."
                v-model="searchInput"
                class="w-full max-w-md px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>

        <div class="overflow-x-auto">
            <table class="w-full table-auto border-collapse rounded-lg shadow-md bg-white">
                <thead>
                    <tr class="bg-gray-100 text-left text-sm font-semibold text-gray-700">
                        <th class="px-6 py-4">Username</th>
                        <th class="px-6 py-4">Email</th>
                        <th class="px-6 py-4">Role</th>
                        <th class="px-6 py-4">Last Login</th>
                        <th class="px-6 py-4">Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="user in filteredUsers" :key="user.username" class="border-b hover:bg-gray-50 transition">
                        <td class="px-6 py-4 text-gray-800">{{ user.username }}</td>
                        <td class="px-6 py-4 text-gray-600">{{ user.email }}</td>
                        <td class="px-6 py-4">
                            <span
                                :class="user.role === 'admin' ? 'bg-red-100 text-red-600' : 'bg-blue-100 text-blue-600'"
                                class="px-2 py-1 text-xs rounded-full font-medium">
                                {{ user.role }}
                            </span>
                        </td>
                        <td class="px-6 py-4 text-sm text-gray-500">{{ new Date(user.last_login).toLocaleString() }}
                        </td>
                        <td class="px-6 py-4 space-x-2">
                            <button
                                class="px-3 py-1 text-sm text-white bg-gray-500 rounded hover:bg-gray-600"
                                    @click="handleEditModal(user)"
                                >Edit</button>
                            <button class="px-3 py-1 text-sm text-white bg-red-500 rounded hover:bg-red-600"
                                @click="handleDelete(user.id)">Delete</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>

    <Modal :isOpen="openEditModal" @close="openEditModal=false"
        myClass="bg-white min-w-[450px]"
    >
    <div class="p-6 max-w-md mx-auto">
        <div class="flex justify-between items-center mb-4">
            <h3 class="text-xl font-medium">Edit User Role</h3>
        </div>
        
        
        <div class="w-full h-8  grid grid-cols-2 mb-8 bg-">
            <div class="">
                <p class="text-gray-800">Username</p>
                <p>{{ editUser.username }}</p>
            </div>
            <div class="">
                <p class="text-gray-800">Email</p>
                <p>{{ editUser.email }}</p>
            </div>
        </div>
        
        <div class="mb-6 mt-4">
            <label class="block text-md mb-2 font-semibold">Role</label>
            <div class="flex space-x-3">
                <button  @click="selectedRole='admin'"
                    :class="[
                        'px-4 py-2 rounded-md text-sm font-medium',
                        selectedRole === 'admin' 
                            ? 'bg-red-500 text-white' 
                            : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    ]"
                >
                    Admin
                </button>
                <button  @click="selectedRole='user'"
                    :class="[
                        'px-4 py-2 rounded-md text-sm font-medium',
                        selectedRole === 'user' 
                            ? 'bg-blue-500 text-white' 
                            : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    ]"
                >
                    User
                </button>
            </div>
        </div>
        
        <div class="flex justify-end space-x-3">
            <button 
                class="px-4 py-2 bg-gray-100 text-gray-700 rounded-md text-sm font-medium hover:bg-gray-200"
                @click="openEditModal=false"

            >
                Cancel
            </button>
            <button 
                class="px-4 py-2 bg-blue-600 text-white rounded-md text-sm font-medium hover:bg-blue-700"
                @click="handleEditSave"
            >
                Save Changes
            </button>
        </div>
    </div>
    </Modal>
</template>

<script setup>

import { onMounted, ref, computed } from 'vue';
import Modal from '../components/Modal.vue';
import axios from 'axios';
import api from '../api';

const users = ref([])
const searchInput = ref("")

const selectedRole = ref("user")
const openEditModal = ref(false)

const editUser = ref(null)

const filteredUsers = computed(() => {
    const search = searchInput.value.toLowerCase().trim()

    if (!search) return users.value

    return users.value.filter(user =>
    user.username.toLowerCase().includes(search))
})
const fetchUsers = async () => {
    const res = await api.get("/users/")
    users.value = res.data
    console.log(res.data)
}

onMounted(async () => {
    await fetchUsers()
})

const handleEditModal = (user) => {
    openEditModal.value = true
    editUser.value = user
}

const handleDelete = async (userId) => {
    console.log("Want to delete user with id ", userId)
    const answer = confirm("Are you are you want to delete user?")
    if (!answer) return;

    try {
        await api.delete(`/users/${userId}/`)
        await fetchUsers()
    } catch (error) {

    }
}

const handleEditSave = async () => {
    if (!editUser.value) return;

    if (editUser.value.role === 'admin' && selectedRole.value !== 'admin') {
        const confirmChange = confirm("Are you sure you want to remove admin rights from this user?");
        if (!confirmChange) return;
    }

    try {
        await api.patch(`/users/${editUser.value.id}/`, {
            role: selectedRole.value,
        });
        await fetchUsers();
        openEditModal.value = false;
    } catch (error) {
        console.error("Error updating user role:", error);
        alert("Failed to update role.");
    }
}

</script>