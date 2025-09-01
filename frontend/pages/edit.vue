<template>
  <div class="container mx-auto p-6 bg-gradient-to-br from-white via-green-50 to-blue-50 min-h-screen">
    <h1 class="text-4xl font-extrabold text-green-700 mb-6">
      {{ isEvent ? (noteId ? 'Edit Event' : 'Add Event') : (noteId ? 'Edit Note' : 'Add Note') }}
    </h1>
    <form @submit.prevent="saveItem" class="space-y-6">
      <div>
        <label class="block text-lg text-blue-700 mb-2">Title</label>
        <input
          v-model="item.title"
          type="text"
          class="border border-cyan-200 p-3 w-full rounded-xl focus:outline-none focus:ring-2 focus:ring-cyan-400"
          required
        >
      </div>
      <div>
        <label class="block text-lg text-blue-700 mb-2">Content</label>
        <textarea
          v-model="item.content"
          class="border border-cyan-200 p-3 w-full rounded-xl focus:outline-none focus:ring-2 focus:ring-cyan-400"
          rows="4"
          required
        ></textarea>
      </div>
      <div v-if="isEvent">
        <label class="block text-lg text-blue-700 mb-2">Start Date</label>
        <input
          v-model="item.start_date"
          type="datetime-local"
          class="border border-cyan-200 p-3 w-full rounded-xl focus:outline-none focus:ring-2 focus:ring-green-400"
        >
        <label class="block text-lg text-blue-700 mb-2 mt-2">End Date</label>
        <input
          v-model="item.end_date"
          type="datetime-local"
          class="border border-cyan-200 p-3 w-full rounded-xl focus:outline-none focus:ring-2 focus:ring-green-400"
        >
        <label class="block text-lg text-blue-700 mb-2 mt-2 items-center space-x-2">
          <span>All Day</span>
          <input
            v-model="item.all_day"
            type="checkbox"
            class="h-5 w-5 text-green-600 focus:ring-cyan-400 border-cyan-300 rounded"
          >
        </label>
      </div>
      <button
        type="submit"
        class="bg-gradient-to-r from-green-500 via-cyan-500 to-blue-500 text-white px-6 py-3 rounded-full hover:from-green-600 hover:via-cyan-600 hover:to-blue-600 transition duration-300 shadow-md"
      >
        Save
      </button>
      <button
        @click="navigateTo('/dashboard')"
        class="ml-4 bg-gray-400 text-white px-6 py-3 rounded-full hover:bg-gray-500 transition duration-300"
      >
        Cancel
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useCookie } from '#imports';
import { useRoute } from 'vue-router';
import { navigateTo } from '#app/composables/router';

const token = useCookie('token');
const route = useRoute();
const item = ref({ title: '', content: '', start_date: new Date().toISOString().slice(0, 16), end_date: '', all_day: false });
const noteId = ref(route.query.id);
const isEvent = ref(route.query.type === 'event');

const isAuthenticated = computed(() => token && typeof token.value !== 'undefined' && token.value !== null);

const fetchItem = async () => {
  if (isAuthenticated.value && noteId.value) {
    try {
      const endpoint = isEvent.value ? 'events' : 'notes';
      const response = await $fetch(`http://localhost:5000/api/${endpoint}/${noteId.value}`, {
        headers: { Authorization: `Bearer ${token.value}` }
      });
      item.value = response;
      if (isEvent.value && !item.value.start_date) item.value.start_date = new Date().toISOString().slice(0, 16);
    } catch (error) {
      console.error(`Error fetching ${isEvent.value ? 'event' : 'note'}:`, error);
    }
  }
};

const saveItem = async () => {
  if (isAuthenticated.value) {
    try {
      const endpoint = isEvent.value ? 'events' : 'notes';
      const url = noteId.value ? `http://localhost:5000/api/${endpoint}/${noteId.value}` : `http://localhost:5000/api/${endpoint}`;
      const method = noteId.value ? 'PUT' : 'POST';
      await $fetch(url, {
        method: method,
        headers: { Authorization: `Bearer ${token.value}`, 'Content-Type': 'application/json' },
        body: JSON.stringify(item.value)
      });
      navigateTo('/dashboard');
    } catch (error) {
      console.error(`Error saving ${isEvent.value ? 'event' : 'note'}:`, error);
    }
  }
};

onMounted(() => {
  fetchItem();
});
</script>