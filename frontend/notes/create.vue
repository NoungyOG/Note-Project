<template>
  <div class="space-y-6">
    <div>
      <label for="title" class="block text-sm font-medium text-purple-700">หัวข้อบันทึก</label>
      <input
        type="text"
        id="title"
        v-model="noteForm.title"
        required
        class="mt-1 block w-full border border-purple-200 rounded-xl shadow-inner p-3 focus:outline-none focus:ring-2 focus:ring-purple-400 bg-white/80 text-gray-800 placeholder-purple-300 transition duration-300 sm:text-sm"
      />
    </div>
    <div>
      <label for="content" class="block text-sm font-medium text-purple-700">เนื้อหา</label>
      <textarea
        id="content"
        v-model="noteForm.content"
        rows="5"
        class="mt-1 block w-full border border-purple-200 rounded-xl shadow-inner p-3 focus:outline-none focus:ring-2 focus:ring-purple-400 bg-white/80 text-gray-800 placeholder-purple-300 transition duration-300 sm:text-sm resize-none"
      ></textarea>
    </div>
    <div>
      <label for="note_date" class="block text-sm font-medium text-purple-700">วันที่เกี่ยวข้อง (สำหรับปฏิทิน)</label>
      <input
        type="date"
        id="note_date"
        v-model="noteForm.note_date"
        class="mt-1 block w-full border border-purple-200 rounded-xl shadow-inner p-3 focus:outline-none focus:ring-2 focus:ring-purple-400 bg-white/80 text-gray-800 placeholder-purple-300 transition duration-300 sm:text-sm"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from '#imports'; // เพิ่ม useRoute หากต้องการตั้งค่าเริ่มต้นจาก query

const noteForm = ref({
  title: '',
  content: '',
  note_date: ''
});

const route = useRoute();
onMounted(() => {
  if (route.query.date) {
    noteForm.value.note_date = route.query.date; // ตั้งค่าเริ่มต้นจาก query ถ้ามี
  }
});

// สมมติฟังก์ชัน createNote (กรุณาเพิ่มตามบริบท)
const createNote = async () => {
  // ใส่ logic ส่ง noteForm.value ไป Backend
  // ตัวอย่าง:
  // await $fetch(`${apiBase}/notes`, {
  //   method: 'POST',
  //   headers: { 'Authorization': `Bearer ${token.value}` },
  //   body: JSON.stringify(noteForm.value)
  // });
};
</script>