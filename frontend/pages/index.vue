<template>
  <div class="min-h-screen w-full bg-gradient-to-br from-green-900 via-cyan-800 to-green-700 flex items-center justify-center relative overflow-hidden">
    <div class="absolute inset-0 bg-cover bg-center opacity-30 blur-sm" style="background-image: url('https://t3.ftcdn.net/jpg/02/49/68/72/360_F_249687268_Yl4AswCdwBQS7NA6hczKq0pfnjQs02UP.jpg');"></div>

    <div class="text-center z-10 p-6 max-w-4xl w-full">
      <h1 class="text-6xl md:text-7xl font-extrabold text-black mb-6 flex items-center justify-center gap-6 drop-shadow-lg">
        <i class="fas fa-book text-5xl text-yellow-300"> Simple Notes App</i>
      </h1>

      <p class="text-xl md:text-2xl text-white mb-10 leading-relaxed max-w-2xl mx-auto drop-shadow-md">
        Welcome to Simple Notes App, งานครูบิ้วว
      </p>

      <div v-if="!isLoggedIn" class="mt-10 flex justify-center gap-6">
        <NuxtLink to="/login" class="flex items-center gap-3 bg-gradient-to-r from-red-500 to-pink-600 text-white px-8 py-4 rounded-xl shadow-xl hover:from-blue-600 hover:to-purple-700 transition duration-300 transform hover:scale-105">
          <i class="fas fa-sign-in-alt text-xl"></i> Login
        </NuxtLink>
        <NuxtLink to="/register" class="flex items-center gap-3 bg-gradient-to-r from-green-500 to-teal-600 text-white px-8 py-4 rounded-xl shadow-xl hover:from-green-600 hover:to-teal-700 transition duration-300 transform hover:scale-105">
          <i class="fas fa-user-plus text-xl"></i> Register
        </NuxtLink>
      </div>
      <div v-else class="mt-10">
        <NuxtLink to="/dashboard" class="flex items-center gap-3 bg-gradient-to-r from-indigo-500 to-purple-600 text-white px-8 py-4 rounded-xl shadow-xl hover:from-indigo-600 hover:to-purple-700 transition duration-300 transform hover:scale-105">
          <i class="fas fa-tachometer-alt text-xl"></i> Go to Dashboard
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script>
import { useState, useCookie } from '#imports';

export default {
  setup() {
    const token = useCookie('token');
    const isLoggedIn = useState('isLoggedIn', () => !!token.value);

    return { isLoggedIn };
  }
}
</script>

<style scoped>
.animate-float {
  animation: float 6s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-20px); }
}

.drop-shadow-lg {
  filter: drop-shadow(0 4px 6px rgba(0, 0, 0, 0.4));
}

.drop-shadow-md {
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
}
</style>