<template>
  <div class="container mx-auto p-6 bg-gradient-to-br from-white via-purple-50 to-indigo-50 min-h-screen flex items-center justify-center">
    <div class="bg-white/90 p-8 rounded-2xl shadow-xl w-full max-w-md transform transition-all duration-300 hover:shadow-2xl">
      <h1 class="text-4xl font-extrabold text-indigo-800 mb-6 text-center">Register</h1>
      <form @submit.prevent="handleRegister" class="mt-6 space-y-6">
        <div>
          <label class="block text-lg text-purple-800 mb-2">Username</label>
          <input v-model="username" type="text" class="border border-indigo-200 p-3 w-full rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-300 focus:border-transparent transition duration-300 placeholder-purple-400" required>
        </div>
        <div>
          <label class="block text-lg text-purple-800 mb-2">Password</label>
          <input v-model="password" type="password" class="border border-indigo-200 p-3 w-full rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-300 focus:border-transparent transition duration-300 placeholder-purple-400" required>
        </div>
        <button type="submit" class="bg-gradient-to-r from-indigo-500 to-purple-500 text-white px-6 py-3 w-full rounded-full hover:from-indigo-600 hover:to-purple-600 transition duration-300 shadow-md hover:shadow-lg">Register</button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  setup() {
    const username = ref('');
    const password = ref('');

    const handleRegister = async () => {
      const response = await $fetch('http://localhost:5000/api/register', {
        method: 'POST',
        body: { username: username.value, password: password.value }
      });
      if (response.msg === 'User registered successfully') {
        navigateTo('/login');
      } else {
        alert('Registration failed');
      }
    };

    return { username, password, handleRegister };
  }
}
</script>