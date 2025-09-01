<template>
    <div class="container mx-auto p-6 bg-gradient-to-br from-white via-purple-50 to-indigo-50 min-h-screen">
      <h1 class="text-3xl font-bold text-indigo-800 mb-6">สร้างกิจกรรมใหม่</h1>
      <EventForm :initial-date="selectedDate" @submit="handleCreateEvent" @cancel="navigateToDashboard" />
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import { useRoute, navigateTo, useCookie, useRuntimeConfig } from '#imports';
  import EventForm from '~/components/EventForm.vue';
  
  const route = useRoute();
  const token = useCookie('token');
  const config = useRuntimeConfig();
  const apiBase = config.public.apiBase;
  
  const selectedDate = ref('');
  
  onMounted(() => {
    if (!token.value) {
      navigateTo('/login');
      return;
    }
    // ดึงวันที่จาก query parameter (เช่น ?date=2025-06-23)
    if (route.query.date) {
      selectedDate.value = route.query.date;
    }
  });
  
  const handleCreateEvent = async (eventData) => {
    try {
      // ต้องแน่ใจว่า eventData.start_date และ eventData.end_date เป็น ISO strings
      // ถ้ามาจาก date picker อาจจะเป็น Date object หรือ string อื่นๆ ให้แปลงก่อนส่ง
      const payload = {
        ...eventData,
        start_date: eventData.start_date.toISOString(),
        end_date: eventData.end_date ? eventData.end_date.toISOString() : null,
      };
  
      await $fetch(`${apiBase}/events`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token.value}`
        },
        body: payload
      });
      alert('สร้างกิจกรรมสำเร็จ!');
      navigateTo('/dashboard'); // หรือไปหน้าหลัก
    } catch (error) {
      console.error('Error creating event:', error);
      if (error.response?.status === 401) {
        token.value = null;
        navigateTo('/login');
      }
      alert('ไม่สามารถสร้างกิจกรรมได้: ' + (error.response?._data?.msg || error.message));
    }
  };
  
  const navigateToDashboard = () => {
    navigateTo('/dashboard');
  };
  </script>