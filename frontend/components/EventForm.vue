<template>
    <form @submit.prevent="handleSubmit" class="bg-white p-8 rounded-lg shadow-xl space-y-6">
      <div>
        <label for="title" class="block text-sm font-medium text-gray-700">ชื่อกิจกรรม</label>
        <input type="text" id="title" v-model="eventForm.title" required
               class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-3 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
      </div>
  
      <div>
        <label for="description" class="block text-sm font-medium text-gray-700">รายละเอียด</label>
        <textarea id="description" v-model="eventForm.description" rows="3"
                  class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-3 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"></textarea>
      </div>
  
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label for="start_date" class="block text-sm font-medium text-gray-700">วันที่เริ่มต้น</label>
          <input type="datetime-local" id="start_date" v-model="startDateTimeLocal" required
                 class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-3 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
        </div>
        <div>
          <label for="end_date" class="block text-sm font-medium text-gray-700">วันที่สิ้นสุด (ไม่บังคับ)</label>
          <input type="datetime-local" id="end_date" v-model="endDateTimeLocal"
                 class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-3 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
        </div>
      </div>
  
      <div>
        <label for="category" class="block text-sm font-medium text-gray-700">หมวดหมู่</label>
        <input type="text" id="category" v-model="eventForm.category"
               class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-3 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
      </div>
  
      <div>
        <label for="location" class="block text-sm font-medium text-gray-700">สถานที่</label>
        <input type="text" id="location" v-model="eventForm.location"
               class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-3 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
      </div>
  
      <div class="flex items-center">
        <input id="all_day" type="checkbox" v-model="eventForm.all_day"
               class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded">
        <label for="all_day" class="ml-2 block text-sm text-gray-900">กิจกรรมทั้งวัน</label>
      </div>
  
      <div class="flex justify-between items-center mt-6">
        <div class="space-x-4">
          <button type="submit"
                  class="bg-indigo-600 text-white px-6 py-3 rounded-md hover:bg-indigo-700 transition duration-300 shadow-md">
            {{ initialEvent ? 'บันทึกการแก้ไข' : 'สร้างกิจกรรม' }}
          </button>
          <button type="button" @click="$emit('cancel')"
                  class="bg-gray-300 text-gray-800 px-6 py-3 rounded-md hover:bg-gray-400 transition duration-300 shadow-md">
            ยกเลิก
          </button>
        </div>
        <button v-if="initialEvent" type="button" @click="$emit('delete')"
                class="bg-red-500 text-white px-6 py-3 rounded-md hover:bg-red-600 transition duration-300 shadow-md">
          ลบกิจกรรม
        </button>
      </div>
    </form>
  </template>
  
  <script setup>
  import { ref, watch, computed } from 'vue';
  
  const props = defineProps({
    initialEvent: {
      type: Object,
      default: null // สำหรับแก้ไขกิจกรรม, จะมีค่า event data เข้ามา
    },
    initialDate: {
      type: String,
      default: '' // สำหรับสร้างกิจกรรมใหม่จากวันที่ในปฏิทิน (YYYY-MM-DD)
    }
  });
  
  const emit = defineEmits(['submit', 'cancel', 'delete']);
  
  const eventForm = ref({
    title: '',
    description: '',
    start_date: new Date(), // เริ่มต้นด้วย Date object ปัจจุบัน
    end_date: null,
    all_day: false,
    category: '',
    location: ''
  });
  
  // Helper function to format Date object to 'YYYY-MM-DDTHH:MM' string for input type="datetime-local"
  const formatDateToLocal = (date) => {
    if (!date) return '';
    const d = new Date(date);
    // Get components in local timezone
    const year = d.getFullYear();
    const month = (d.getMonth() + 1).toString().padStart(2, '0');
    const day = d.getDate().toString().padStart(2, '0');
    const hours = d.getHours().toString().padStart(2, '0');
    const minutes = d.getMinutes().toString().padStart(2, '0');
    return `${year}-${month}-${day}T${hours}:${minutes}`;
  };
  
  // Computed properties to bind to datetime-local inputs
  const startDateTimeLocal = computed({
    get: () => formatDateToLocal(eventForm.value.start_date),
    set: (value) => {
      // Convert input string back to Date object
      eventForm.value.start_date = value ? new Date(value) : null;
    }
  });
  
  const endDateTimeLocal = computed({
    get: () => formatDateToLocal(eventForm.value.end_date),
    set: (value) => {
      eventForm.value.end_date = value ? new Date(value) : null;
    }
  });
  
  // Watch initialEvent prop to populate form for editing
  watch(() => props.initialEvent, (newEvent) => {
    if (newEvent) {
      eventForm.value = {
        title: newEvent.title || '',
        description: newEvent.description || '',
        start_date: newEvent.start_date ? new Date(newEvent.start_date) : new Date(),
        end_date: newEvent.end_date ? new Date(newEvent.end_date) : null,
        all_day: newEvent.all_day || false,
        category: newEvent.category || '',
        location: newEvent.location || ''
      };
    }
  }, { immediate: true });
  
  // Watch initialDate prop to pre-fill start_date for creation
  watch(() => props.initialDate, (newDate) => {
    if (newDate && !props.initialEvent) { // Only set if creating a new event and initialEvent is not provided
      const dateObj = new Date(newDate + 'T00:00:00'); // Set to midnight of the selected day
      eventForm.value.start_date = dateObj;
      // Clear end date by default when creating a new event from a day click
      eventForm.value.end_date = null;
    }
  }, { immediate: true });
  
  const handleSubmit = () => {
    // Emit the form data with Date objects (Nuxt's $fetch will convert to ISO string automatically)
    // Or explicitly convert to ISO string here before emitting if you prefer
    const submittedData = {
      ...eventForm.value,
      start_date: eventForm.value.start_date, // ส่ง Date object ไป
      end_date: eventForm.value.end_date // ส่ง Date object หรือ null ไป
    };
    emit('submit', submittedData);
  };
  </script>