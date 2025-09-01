<template>
  <div class="min-h-screen w-full bg-gradient-to-br from-indigo-900 via-purple-800 to-indigo-700 flex items-center justify-center relative overflow-hidden">
    <!-- Blurred Background Image -->
    <div class="absolute inset-0 bg-cover bg-center opacity-30 blur-sm" style="background-image: url('https://images.unsplash.com/photo-1451187580459-43490279c0fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80');"></div>
    <!-- Floating Background Elements -->
    <div class="absolute top-10 left-10 w-32 h-32 bg-purple-300 rounded-full opacity-20 animate-float"></div>
    <div class="absolute bottom-10 right-10 w-40 h-40 bg-indigo-300 rounded-full opacity-20 animate-float delay-1000"></div>

    <div class="text-center z-10 p-6 max-w-4xl w-full">
      <!-- Header with Icon -->
      <h1 class="text-6xl md:text-7xl font-extrabold text-white mb-6 flex items-center justify-center gap-6 drop-shadow-lg">
        <i class="fas fa-book text-5xl text-yellow-300"></i> Simple Notes App
      </h1>

      <!-- Detailed Description -->
      <p class="text-xl md:text-2xl text-white mb-10 leading-relaxed max-w-2xl mx-auto drop-shadow-md">
        Welcome to Simple Notes App, your ultimate tool for organizing life! Effortlessly create, manage, and track your notes, events, and calendar entries with a sleek, secure, and intuitive interface. Whether you're planning your day or jotting down ideas, our app keeps everything in sync. Start your journey to productivity today—join us now!
      </p>

      <!-- Navigation Links -->
      <div v-if="!isLoggedIn" class="mt-10 flex justify-center gap-6">
        <NuxtLink to="/login" class="flex items-center gap-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white px-8 py-4 rounded-xl shadow-xl hover:from-blue-600 hover:to-purple-700 transition duration-300 transform hover:scale-105">
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
/* Animation for floating elements */
.animate-float {
  animation: float 6s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-20px); }
}

/* Ensure text stands out */
.drop-shadow-lg {
  filter: drop-shadow(0 4px 6px rgba(0, 0, 0, 0.4));
}

.drop-shadow-md {
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
}
</style>