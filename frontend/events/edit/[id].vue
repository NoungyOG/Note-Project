<template>
    <div class="container mx-auto p-6 bg-gradient-to-br from-white via-purple-50 to-indigo-50 min-h-screen">
      <h1 class="text-3xl font-bold text-indigo-800 mb-6">แก้ไขกิจกรรม</h1>
      <p v-if="loading">กำลังโหลดข้อมูลกิจกรรม...</p>
      <p v-else-if="error">{{ error }}</p>
      <EventForm v-else :initial-event="event" @submit="handleUpdateEvent" @cancel="navigateToDashboard" @delete="handleDeleteEvent" />
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
  
  const event = ref(null);
  const loading = ref(true);
  const error = ref(null);
  
  onMounted(async () => {
    if (!token.value) {
      navigateTo('/login');
      return;
    }
    const eventId = route.params.id;
    if (!eventId) {
      error.value = 'ไม่พบ ID กิจกรรม';
      loading.value = false;
      return;
    }
  
    try {
      const response = await $fetch(`${apiBase}/events/${eventId}`, {
        headers: { Authorization: `Bearer ${token.value}` }
      });
      // แปลงวันที่ที่ได้รับจาก backend (ISO string) เป็น Date object สำหรับ form
      event.value = {
        ...response,
        start_date: response.start_date ? new Date(response.start_date) : null,
        end_date: response.end_date ? new Date(response.end_date) : null
      };
    } catch (err) {
      console.error('Error fetching event:', err);
      if (err.response?.status === 401) {
        token.value = null;
        navigateTo('/login');
      }
      error.value = 'ไม่สามารถโหลดข้อมูลกิจกรรมได้: ' + (err.response?._data?.msg || err.message);
    } finally {
      loading.value = false;
    }
  });
  
  const handleUpdateEvent = async (eventData) => {
    try {
      const eventId = route.params.id;
      const payload = {
        ...eventData,
        start_date: eventData.start_date.toISOString(), // แปลง Date object เป็น ISO string ก่อนส่ง
        end_date: eventData.end_date ? eventData.end_date.toISOString() : null, // แปลงเป็น ISO string หรือ null
      };
  
      await $fetch(`${apiBase}/events/${eventId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token.value}`
        },
        body: payload
      });
      alert('อัปเดตกิจกรรมสำเร็จ!');
      navigateTo('/dashboard');
    } catch (err) {
      console.error('Error updating event:', err);
      if (err.response?.status === 401) {
        token.value = null;
        navigateTo('/login');
      }
      alert('ไม่สามารถอัปเดตกิจกรรมได้: ' + (err.response?._data?.msg || err.message));
    }
  };
  
  const handleDeleteEvent = async () => {
    if (!confirm('คุณแน่ใจหรือไม่ที่จะลบกิจกรรมนี้?')) {
      return;
    }
    try {
      const eventId = route.params.id;
      await $fetch(`${apiBase}/events/${eventId}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token.value}` }
      });
      alert('ลบกิจกรรมสำเร็จ!');
      navigateTo('/dashboard');
    } catch (err) {
      console.error('Error deleting event:', err);
      if (err.response?.status === 401) {
        token.value = null;
        navigateTo('/login');
      }
      alert('ไม่สามารถลบกิจกรรมได้: ' + (err.response?._data?.msg || err.message));
    }
  };
  
  const navigateToDashboard = () => {
    navigateTo('/dashboard');
  };
  </script>