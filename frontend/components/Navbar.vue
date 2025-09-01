<template>
  <nav class="bg-gradient-to-r from-purple-400 via-indigo-400 to-blue-300 backdrop-blur-md text-white px-4 py-4 sm:px-6 sm:py-6 flex flex-col sm:flex-row justify-between items-center shadow-2xl transform transition-all duration-300 hover:shadow-3xl">
    <NuxtLink to="/" class="text-2xl sm:text-3xl font-extrabold tracking-wide hover:text-white/80 transition-transform transform hover:scale-105 mb-4 sm:mb-0">
      Notes App
    </NuxtLink>
    <div class="flex flex-col sm:flex-row space-y-4 sm:space-y-0 sm:space-x-4 sm:space-x-8 text-base sm:text-lg font-semibold w-full sm:w-auto">
      <NuxtLink to="/login" class="hover:text-white/80 transition-all hover:underline underline-offset-8 decoration-2 text-center sm:text-left">Login</NuxtLink>
      <NuxtLink to="/register" class="hover:text-white/80 transition-all hover:underline underline-offset-8 decoration-2 text-center sm:text-left">Register</NuxtLink>
      <NuxtLink to="/dashboard" class="hover:text-white/80 transition-all hover:underline underline-offset-8 decoration-2 text-center sm:text-left">Dashboard</NuxtLink>
    </div>
  </nav>
</template>

<script setup>
// ไม่ต้องใช้ export default เพราะ <script setup> จะอัตโนมัติเป็น component
</script>