<template>
  <div class="bg-gradient-to-br from-purple-100 via-indigo-100 to-white p-6 rounded-2xl shadow-md hover:shadow-xl transition-all duration-300 transform hover:-translate-y-2">
    <div v-if="!internalIsEditing">
      <h3 class="font-bold text-xl text-indigo-800 line-clamp-2">{{ note.title }}</h3>
      <p class="text-md text-purple-600 mt-2 line-clamp-3">{{ note.content }}</p>
      <p class="text-lg text-right text-purple-400 mt-3 font-medium">
        สร้างเมื่อ: {{ formatDate(note.created_at) }}
        <span v-if="note.note_date"> | วันที่เกี่ยวข้อง: {{ formatDate(note.note_date) }}</span>
      </p>
      <div class="flex justify-end gap-4 mt-4">
        <button
          @click="toggleEditMode"
          class="bg-gradient-to-r from-indigo-400 to-purple-400 text-white px-4 py-2 rounded-full hover:from-indigo-500 hover:to-purple-500 transition duration-300 font-medium shadow-sm hover:shadow-md"
        >
          แก้ไข
        </button>
        <button
          @click="confirmDelete"
          class="bg-red-200 text-red-700 px-4 py-2 rounded-full hover:bg-red-300 transition duration-300 font-medium shadow-sm hover:shadow-md"
        >
          ลบ
        </button>
      </div>
    </div>

    <div v-else>
      <input
        v-model="editTitle"
        placeholder="หัวข้อ"
        class="mb-4 p-3 border border-purple-200 rounded-xl w-full focus:outline-none focus:ring-2 focus:ring-purple-400 bg-white/80 text-gray-800 placeholder-purple-300 transition duration-300 shadow-inner"
        required
      />
      <textarea
        v-model="editContent"
        placeholder="เนื้อหา"
        rows="5"
        class="mb-4 p-3 border border-purple-200 rounded-xl w-full focus:outline-none focus:ring-2 focus:ring-purple-400 bg-white/80 text-gray-800 placeholder-purple-300 transition duration-300 shadow-inner resize-y"
      ></textarea>
      <div>
        <label for="edit_note_date" class="block text-sm font-medium text-purple-700">วันที่เกี่ยวข้อง (สำหรับปฏิทิน)</label>
        <input
          type="date"
          id="edit_note_date"
          v-model="editNoteDate"
          class="mt-1 block w-full border border-purple-200 rounded-xl shadow-inner p-3 focus:outline-none focus:ring-2 focus:ring-purple-400 bg-white/80 text-gray-800 placeholder-purple-300 transition duration-300"
        />
      </div>
      <div class="flex justify-end gap-4 mt-4">
        <button
          @click="saveEdit"
          class="bg-gradient-to-r from-indigo-500 to-purple-500 text-white px-5 py-2 rounded-full hover:from-indigo-600 hover:to-purple-600 transition duration-300 font-semibold shadow-md hover:shadow-lg"
        >
          บันทึก
        </button>
        <button
          @click="cancelEdit"
          class="bg-gray-200 text-indigo-700 px-5 py-2 rounded-full hover:bg-gray-300 transition duration-300 font-semibold shadow-md hover:shadow-lg"
        >
          ยกเลิก
        </button>
      </div>
      <p v-if="errorMsg" class="text-red-500 text-sm mt-3 text-center">{{ errorMsg }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import { useCookie, useRuntimeConfig } from '#imports';
import { navigateTo } from '#imports';

const props = defineProps({
  note: {
    type: Object,
    required: true,
  },
});
const emit = defineEmits(['delete', 'update:note', 'refreshDashboard']);

const token = useCookie('token');
const config = useRuntimeConfig();
const apiBase = config.public.apiBase || 'http://localhost:5000/api';

const internalIsEditing = ref(false);
const editTitle = ref(props.note.title);
const editContent = ref(props.note.content);
const editNoteDate = ref(props.note.note_date ? new Date(props.note.note_date).toISOString().split('T')[0] : '');
const errorMsg = ref('');

watch(() => props.note, (newNote) => {
  editTitle.value = newNote.title || '';
  editContent.value = newNote.content || '';
  editNoteDate.value = newNote.note_date ? new Date(newNote.note_date).toISOString().split('T')[0] : '';
}, { deep: true, immediate: true });

const toggleEditMode = () => {
  internalIsEditing.value = !internalIsEditing.value;
  errorMsg.value = '';
};

const saveEdit = async () => {
  errorMsg.value = '';
  if (!editTitle.value.trim() || !editContent.value.trim()) {
    errorMsg.value = 'Title and Content cannot be empty.';
    return;
  }
  if (!token.value) {
    errorMsg.value = 'No authentication token found. Please log in.';
    navigateTo('/login');
    return;
  }
  const noteIdToUse = props.note._id || props.note.id;
  if (!noteIdToUse) {
    errorMsg.value = 'Note ID is missing. Cannot update.';
    console.error('Note ID is undefined, cannot update:', props.note);
    return;
  }

  try {
    const payload = {
      title: editTitle.value,
      content: editContent.value,
      note_date: editNoteDate.value || null
    };
    
    const updatedNote = await $fetch(`${apiBase}/notes/${noteIdToUse}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token.value}`
      },
      body: JSON.stringify(payload)
    });

    alert('บันทึกสำเร็จ!');
    internalIsEditing.value = false;
    
    emit('update:note', {
      ...props.note,
      title: updatedNote.title,
      content: updatedNote.content,
      note_date: updatedNote.note_date,
      updated_at: updatedNote.updated_at
    });

    emit('refreshDashboard');
  } catch (err) {
    console.error('Error updating note:', err);
    if (err.response?.status === 401) {
      token.value = null;
      navigateTo('/login');
    }
    errorMsg.value = `อัปเดตล้มเหลว: ${err.response?._data?.msg || err.message || 'Unknown error'}`;
  }
};

const confirmDelete = () => {
  const noteIdToUse = props.note._id || props.note.id;
  if (!noteIdToUse) {
    errorMsg.value = 'Note ID is missing. Cannot delete.';
    console.error('Note ID is undefined, cannot delete:', props.note);
    return;
  }
  if (confirm('คุณแน่ใจหรือไม่ที่จะลบบันทึกนี้?')) {
    emit('delete', noteIdToUse);
  }
};

const cancelEdit = () => {
  editTitle.value = props.note.title || '';
  editContent.value = props.note.content || '';
  editNoteDate.value = props.note.note_date ? new Date(props.note.note_date).toISOString().split('T')[0] : '';
  internalIsEditing.value = false;
  errorMsg.value = '';
};

const formatDate = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleString('th-TH', {
    timeZone: 'Asia/Bangkok',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};
</script>