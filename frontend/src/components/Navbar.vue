<script setup>
import { RouterLink } from 'vue-router';
import { inject, onMounted, ref, onUnmounted, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';

const user = inject('user');
const logout = inject("logout")
const router = useRouter()
const route = useRoute()
const userRole = inject("userRole")
const sidebarActivated = inject("sidebarActivated")

const handleSidebarClick = () => {
  sidebarActivated.value = !sidebarActivated.value
}

const handleLogout = async () => {
  await logout(); 
  router.push("/login");
}

const adminMenuRef = ref(null);
const dropdownTriggerRef = ref(null);
const showAdminMenu = ref(false);

const toggleAdminMenu = () => {
  showAdminMenu.value = !showAdminMenu.value;
  
  if (showAdminMenu.value && adminMenuRef.value) {
    nextTick(() => {
      const firstItem = adminMenuRef.value.querySelector('a');
      if (firstItem) firstItem.focus();
    });
  }
}

const closeOnClickOutside = (event) => {
  if (adminMenuRef.value && 
      dropdownTriggerRef.value && 
      !adminMenuRef.value.contains(event.target) && 
      !dropdownTriggerRef.value.contains(event.target)) {
    showAdminMenu.value = false;
  }
}


watch(() => route.path, () => {
  showAdminMenu.value = false;
});

onMounted(() => {
  document.addEventListener('mousedown', closeOnClickOutside);
});

onUnmounted(() => {
  document.removeEventListener('mousedown', closeOnClickOutside);
});
</script>

<template>
  <nav class="bg-black fixed top-0 left-0 z-50 h-16 w-full shadow-md">
    <button 
      v-if="user" 
      class="w-fit fixed left-4 top-5" 
      @click="handleSidebarClick"
      aria-label="Toggle sidebar"
    >
      <i class="text-white pi pi-bars text-xl"></i>
    </button>

    <div class="max-w-[1200px] px-8 mx-auto flex items-center gap-4 z-100">
      <ul class="text-white flex items-center gap-4 h-16 w-full">
        <RouterLink
          to="/"
          class="ml-8 py-1 px-2 rounded transition-colors duration-200 hover:text-white"
          :class="{
            'text-white font-semibold': route.path === '/',
            'text-gray-300': route.path !== '/'
          }"
        >Home</RouterLink>

        <div class="relative ml-auto" v-if="userRole === 'admin'">
          <button
            ref="dropdownTriggerRef"
            @click="toggleAdminMenu"
            class="text-gray-300 hover:text-white flex items-center gap-2 transition py-1 px-3 rounded "
          >
            <i class="pi pi-cog"></i>
            <span>Admin</span>
            <i class="pi" :class="showAdminMenu ? 'pi-chevron-up' : 'pi-chevron-down'"></i>
          </button>

          <div
            v-show="showAdminMenu"
            ref="adminMenuRef"
            class="absolute right-0 mt-2 w-56 bg-white text-black rounded shadow-lg z-50 border border-gray-200 overflow-hidden transition-all duration-200"
        
          >
            <RouterLink
              to="/admin/users"
              class="px-4 py-3 text-sm hover:bg-gray-100 transition-colors flex items-center gap-2 border-b border-gray-100 focus:outline-none focus:bg-gray-100 focus:text-blue-600"
           
            >
              <i class="pi pi-users text-gray-600"></i>
              <span>Manage Users</span>
            </RouterLink>
            <RouterLink
              to="/admin/models"
              class=" px-4 py-3 text-sm hover:bg-gray-100 transition-colors flex items-center gap-2 focus:outline-none focus:bg-gray-100 focus:text-blue-600"
              role="menuitem"
            >
              <i class="pi pi-database text-gray-600"></i>
              <span>Manage User Models</span>
            </RouterLink>
          </div>
        </div>

        <RouterLink
          to="/login"
          class="hidden sm:block py-1 px-3 rounded transition-colors duration-200"
          v-if="!user"
          :class="{
            'text-white font-semibold': route.path === '/login',
            'text-gray-300': route.path !== '/login'
          }"
        >Login</RouterLink>

        <RouterLink
          to="/register"
          class="hidden sm:block py-1 px-3 rounded transition-colors duration-200"
          v-if="!user"
          :class="{
            'text-white font-semibold': route.path === '/register',
            'text-gray-300': route.path !== '/register'
          }"
        >Register</RouterLink>

        <button 
          v-if="user" 
          class="text-gray-300 hover:text-white ml-4 py-1 px-3 rounded transition-colors duration-200  flex items-center gap-1" 
          @click="handleLogout"
        >
          <span>Logout</span>
        </button>
      </ul>
    </div>
  </nav>
</template>