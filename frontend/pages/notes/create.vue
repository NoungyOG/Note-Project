<template>
  <div class="min-h-screen bg-gradient-to-br from-purple-50 to-indigo-100 p-6 flex items-center justify-center">
    <div class="w-full max-w-md bg-white/95 backdrop-blur-md p-8 rounded-2xl shadow-2xl transform transition-all duration-300 hover:shadow-3xl">
      <h1 class="text-3xl sm:text-4xl font-extrabold text-purple-800 mb-6 text-center drop-shadow-md">สร้างบันทึกใหม่</h1>
      <form @submit.prevent="createNote" class="space-y-6">
        <div class="mb-4">
          <label for="title" class="block text-purple-700 text-sm font-semibold mb-2">ชื่อบันทึก:</label>
          <input
            type="text"
            id="title"
            v-model="note.title"
            class="w-full px-4 py-2 border border-purple-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-400 bg-white/80 text-gray-800 placeholder-purple-300 transition duration-300 shadow-inner"
            required
          />
        </div>
        <div class="mb-4">
          <label for="content" class="block text-purple-700 text-sm font-semibold mb-2">เนื้อหา:</label>
          <textarea
            id="content"
            v-model="note.content"
            class="w-full px-4 py-2 border border-purple-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-400 bg-white/80 text-gray-800 placeholder-purple-300 transition duration-300 shadow-inner h-32 resize-none"
          ></textarea>
        </div>
        <div class="mb-6">
          <label for="note_date" class="block text-purple-700 text-sm font-semibold mb-2">วันที่เกี่ยวข้อง (สำหรับปฏิทิน - ไม่บังคับ):</label>
          <input
            type="date"
            id="note_date"
            v-model="note.note_date"
            class="w-full px-4 py-2 border border-purple-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-400 bg-white/80 text-gray-800 placeholder-purple-300 transition duration-300 shadow-inner"
          />
        </div>
        <div class="flex items-center justify-between space-x-4">
          <button
            type="submit"
            class="w-full bg-purple-600 hover:bg-purple-700 text-white font-bold py-3 px-6 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 transition duration-300 transform hover:-translate-y-1 shadow-md hover:shadow-lg"
          >
            บันทึก
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

const note = ref({
  title: '',
  content: '',
  note_date: '' // Initialize for date input
});

const route = useRoute();
// Pre-fill date if passed from calendar
if (route.query.date) {
  note.value.note_date = route.query.date;
}

const createNote = async () => {
  if (!token.value) {
    alert('โปรดเข้าสู่ระบบเพื่อสร้างบันทึก');
    navigateTo('/login');
    return;
  }
  try {
    const payload = { ...note.value };
    if (payload.note_date) {
      payload.note_date = new Date(payload.note_date).toISOString().split('T')[0]; // Format to YYYY-MM-DD for backend
    } else {
      delete payload.note_date; // Remove if empty so backend treats it as null/none
    }

    await $fetch(`${apiBase}/notes`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token.value}`
      },
      body: JSON.stringify(payload)
    });
    alert('สร้างบันทึกสำเร็จ!');
    navigateTo('/dashboard');
  } catch (error) {
    console.error('Error creating note:', error);
    alert('ไม่สามารถสร้างบันทึกได้: ' + (error.response?._data?.msg || error.message));
  }
};
</script>