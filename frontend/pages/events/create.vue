<template>
  <div class="min-h-screen bg-gradient-to-br from-purple-50 to-indigo-100 p-6 flex items-center justify-center">
    <div class="w-full max-w-md bg-white/95 backdrop-blur-md p-8 rounded-2xl shadow-2xl transform transition-all duration-300 hover:shadow-3xl">
      <h1 class="text-3xl sm:text-4xl font-extrabold text-purple-800 mb-6 text-center drop-shadow-md">สร้างกิจกรรมใหม่</h1>
      <form @submit.prevent="createEvent" class="space-y-6">
        <div class="mb-4">
          <label for="title" class="block text-purple-700 text-sm font-semibold mb-2">ชื่องาน:</label>
          <input
            type="text"
            id="title"
            v-model="event.title"
            class="w-full px-4 py-2 border border-purple-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-400 bg-white/80 text-gray-800 placeholder-purple-300 transition duration-300 shadow-inner"
            required
          />
        </div>
        <div class="mb-4">
          <label for="description" class="block text-purple-700 text-sm font-semibold mb-2">รายละเอียด:</label>
          <textarea
            id="description"
            v-model="event.description"
            class="w-full px-4 py-2 border border-purple-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-400 bg-white/80 text-gray-800 placeholder-purple-300 transition duration-300 shadow-inner h-32 resize-none"
          ></textarea>
        </div>
        <div class="mb-4">
          <label for="start_date" class="block text-purple-700 text-sm font-semibold mb-2">วันที่เริ่มต้น:</label>
          <input
            type="date"
            id="start_date"
            v-model="event.start_date"
            class="w-full px-4 py-2 border border-purple-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-400 bg-white/80 text-gray-800 placeholder-purple-300 transition duration-300 shadow-inner"
            required
          />
        </div>
        <div class="mb-6">
          <label for="end_date" class="block text-purple-700 text-sm font-semibold mb-2">วันที่สิ้นสุด (ไม่บังคับ):</label>
          <input
            type="date"
            id="end_date"
            v-model="event.end_date"
            class="w-full px-4 py-2 border border-purple-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-400 bg-white/80 text-gray-800 placeholder-purple-300 transition duration-300 shadow-inner"
          />
        </div>
        <div class="flex items-center justify-between space-x-4">
          <button
            type="submit"
            class="w-full bg-purple-600 hover:bg-purple-700 text-white font-bold py-3 px-6 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 transition duration-300 transform hover:-translate-y-1 shadow-md hover:shadow-lg"
          >
            สร้างกิจกรรม
          </button>
          <button
            type="button"
            @click="navigateTo('/dashboard')"
            class="w-full bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-3 px-6 rounded-xl focus:outline-none focus:ring-2 focus:ring-gray-400 transition duration-300 transform hover:-translate-y-1 shadow-md"
          >
            ยกเลิก
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useCookie, useRuntimeConfig, navigateTo, useRoute } from '#imports';

const token = useCookie('token');
const config = useRuntimeConfig();
const apiBase = config.public.apiBase;

const event = ref({
  title: '',
  description: '',
  start_date: '',
  end_date: ''
});

const route = useRoute();
if (route.query.date) {
  event.value.start_date = route.query.date;
}

const createEvent = async () => {
  if (!token.value) {
    alert('โปรดเข้าสู่ระบบเพื่อสร้างกิจกรรม');
    navigateTo('/login');
    return;
  }
  try {
    const payload = { ...event.value };
    payload.start_date = new Date(payload.start_date).toISOString().split('T')[0]; // Format to YYYY-MM-DD
    if (payload.end_date) {
      payload.end_date = new Date(payload.end_date).toISOString().split('T')[0]; // Format to YYYY-MM-DD
    } else {
      payload.end_date = null; // Set to null if empty for backend to handle
    }

    await $fetch(`${apiBase}/events`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token.value}`
      },
      body: JSON.stringify(payload)
    });
    alert('สร้างกิจกรรมสำเร็จ!');
    navigateTo('/dashboard');
  } catch (error) {
    console.error('Error creating event:', error);
    alert('ไม่สามารถสร้างกิจกรรมได้: ' + (error.response?._data?.message || error.message));
  }
};
</script>