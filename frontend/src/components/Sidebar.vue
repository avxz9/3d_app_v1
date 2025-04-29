<template>
  <div
    class="top-16 left-0 h-[calc(100vh-3.5rem)] sm:w-[16rem] border-r shadow-lg fixed 
           z-10 sm:flex flex-col gap-3 px-4 py-4 overflow-y-auto bg-white"
  >

    <div class="flex items-center justify-center mb-6 mt-2">
      <span class="text-xl font-bold text-blue-600">{{ APP_NAME }}</span>
    </div>

    <ul class="space-y-1">
      <li
        v-for="links in sidebarLinks"
        :key="links.label"
        class="py-1"
      >
        <RouterLink
          :to="links.path"
          class=" flex items-center px-3 py-3 rounded-lg text-gray-700 hover:text-blue-600 hover:bg-blue-50 transition-colors"
        >
          <i class="pi text-md mr-3" :class="links.style"></i>
          <span class="text-md font-medium">{{ links.label }}</span>
        </RouterLink>
      </li>
    </ul>

    <div class="mt-auto px-3 pt-6 border-t">
      <div class="flex items-center gap-3">
        <img
          src="https://api.dicebear.com/6.x/initials/svg?seed=U"
          alt="User avatar"
          class="w-8 h-8 rounded-full"
        />
        <div>
          <p class="text-sm font-semibold text-gray-700">{{ user.username }}</p>
          <a class="text-xs text-gray-500 hover:text-red-500 cursor-pointer"
            @click="handleLogout"
          >Logout</a>
        </div>
      </div>
    </div>
  </div>
</template>

  
  <script setup>
  import { inject, ref, computed } from "vue";
  import { api } from "../api";
  import { APP_NAME } from "../constants/appInfo";

  const sidebarLinks = [
    {path: "/dashboard", label: "Dashboard", style: "pi-home"},
    {path: "/models", label: "My Models", style: "pi-box"},
    {path: "/analyses", label: "My Analyses", style: "pi-chart-line"},
    {path: "/reports", label: "My Reports", style: "pi-file"},
  ]
  const logout = inject("logout")
  const user = inject("user")


  const handleLogout = async () => {
    await logout()
    router.push("/login");
}


  
  
  </script>
  