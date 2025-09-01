<template>
  <div class="min-h-screen bg-gradient-to-br from-purple-50 to-indigo-100 p-6 flex items-center justify-center">
    <div class="w-full max-w-md bg-white/95 backdrop-blur-md p-8 rounded-2xl shadow-2xl transform transition-all duration-300 hover:shadow-3xl">
      <h1 class="text-3xl sm:text-4xl font-extrabold text-purple-800 mb-6 text-center drop-shadow-md">แก้ไขบันทึก</h1>
      <form v-if="note.id" @submit.prevent="updateNote" class="space-y-6">
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
      <p v-else class="text-purple-600 text-center italic animate-pulse">กำลังโหลดบันทึก...</p>
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
const note = ref({});

const fetchNote = async () => {
  if (!token.value) {
    alert('โปรดเข้าสู่ระบบเพื่อแก้ไขบันทึก');
    navigateTo('/login');
    return;
  }
  const noteId = route.params.id;
  if (!noteId) {
    alert('ไม่พบบันทึกที่ต้องการแก้ไข');
    navigateTo('/dashboard');
    return;
  }
  try {
    const response = await $fetch(`${apiBase}/notes/${noteId}`, {
      headers: { Authorization: `Bearer ${token.value}` }
    });
    note.value = response;
    if (note.value.note_date) {
      note.value.note_date = new Date(note.value.note_date).toISOString().split('T')[0];
    }
  } catch (error) {
    console.error('Error fetching note:', error);
    alert('ไม่สามารถดึงข้อมูลบันทึกได้: ' + (error.response?._data?.msg || error.message));
    navigateTo('/dashboard');
  }
};

const updateNote = async () => {
  if (!token.value) {
    alert('โปรดเข้าสู่ระบบเพื่อแก้ไขบันทึก');
    navigateTo('/login');
    return;
  }
  try {
    const payload = { ...note.value };
    delete payload.id;
    delete payload.user_id;

    if (payload.note_date) {
      payload.note_date = new Date(payload.note_date).toISOString().split('T')[0];
    } else {
      payload.note_date = null;
    }

    await $fetch(`${apiBase}/notes/${route.params.id}`, {
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
    console.error('Error updating note:', error);
    alert('ไม่สามารถบันทึกการแก้ไขได้: ' + (error.response?._data?.msg || error.message));
  }
};

onMounted(() => {
  fetchNote();
});
</script>