<template>
  <div class="min-h-screen bg-gradient-to-br from-purple-50 to-indigo-100 p-6 flex items-center justify-center">
    <div class="w-full max-w-md bg-white/95 backdrop-blur-md p-8 rounded-2xl shadow-2xl transform transition-all duration-300 hover:shadow-3xl">
      <h1 class="text-3xl sm:text-4xl font-extrabold text-purple-800 mb-6 text-center drop-shadow-md">แก้ไขกิจกรรม</h1>
      <form v-if="event.id" @submit.prevent="updateEvent" class="space-y-6">
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
            บันทึกการแก้ไข
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
      <p v-else class="text-purple-600 text-center italic animate-pulse">กำลังโหลดกิจกรรม...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useCookie, useRuntimeConfig, useRoute, navigateTo } from '#imports';

const token = useCookie('token');
const config = useRuntimeConfig();
const apiBase = config.public.apiBase;
const route = useRoute();
const event = ref({});

const fetchEvent = async () => {
  if (!token.value) {
    alert('โปรดเข้าสู่ระบบเพื่อแก้ไขกิจกรรม');
    navigateTo('/login');
    return;
  }
  const eventId = route.params.id;
  if (!eventId) {
    alert('ไม่พบกิจกรรมที่ต้องการแก้ไข');
    navigateTo('/dashboard');
    return;
  }
  try {
    const response = await $fetch(`${apiBase}/events/${eventId}`, {
      headers: { Authorization: `Bearer ${token.value}` }
    });
    event.value = response;
    if (event.value.start_date) {
      event.value.start_date = new Date(event.value.start_date).toISOString().split('T')[0];
    }
    if (event.value.end_date) {
      event.value.end_date = new Date(event.value.end_date).toISOString().split('T')[0];
    }
  } catch (error) {
    console.error('Error fetching event:', error);
    alert('ไม่สามารถดึงข้อมูลกิจกรรมได้: ' + (error.response?._data?.message || error.message));
    navigateTo('/dashboard');
  }
};

const updateEvent = async () => {
  if (!token.value) {
    alert('โปรดเข้าสู่ระบบเพื่อแก้ไขกิจกรรม');
    navigateTo('/login');
    return;
  }
  try {
    const payload = { ...event.value };
    delete payload._id; // _id is in URL, not in body for PUT
    delete payload.user_id;

    payload.start_date = new Date(payload.start_date).toISOString().split('T')[0]; // Format to YYYY-MM-DD
    if (payload.end_date) {
      payload.end_date = new Date(payload.end_date).toISOString().split('T')[0]; // Format to YYYY-MM-DD
    } else {
      payload.end_date = null; // Set to null if empty for backend to handle
    }

    await $fetch(`${apiBase}/events/${event.value.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token.value}`
      },
      body: JSON.stringify(payload)
    });
    alert('บันทึกการแก้ไขสำเร็จ!');
    navigateTo('/dashboard');
  } catch (error) {
    console.error('Error updating event:', error);
    alert('ไม่สามารถบันทึกการแก้ไขได้: ' + (error.response?._data?.message || error.message));
  }
};

onMounted(() => {
  fetchEvent();
});
</script>