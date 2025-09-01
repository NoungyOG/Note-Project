<template>
  <!-- โค้ด template เดิม -->
  <div class="min-h-screen bg-gradient-to-br from-purple-50 to-indigo-100 p-6">
    <header class="bg-white/90 backdrop-blur-md shadow-lg p-6 rounded-2xl flex justify-between items-center mb-8 transform hover:scale-102 transition duration-300">
      <h1 class="text-3xl font-extrabold text-purple-800 drop-shadow-md">แดชบอร์ด</h1>
      <nav>
        <button @click="logout" class="bg-purple-600 hover:bg-purple-700 text-white font-bold py-3 px-6 rounded-xl shadow-md hover:shadow-xl transition duration-300 transform hover:-translate-y-1">
          ออกจากระบบ
        </button>
      </nav>
    </header>

    <main class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
      <section class="sm:col-span-2 lg:col-span-2 bg-white/95 backdrop-blur-md p-6 rounded-2xl shadow-xl transform hover:scale-101 transition duration-300">
        <h2 class="text-2xl font-bold text-purple-800 mb-6 flex justify-between items-center border-b-2 border-purple-200 pb-2">
          ปฏิทินและกิจกรรม
        </h2>
        <div class="calendar-container overflow-x-auto">
          <VCalendar
            expanded
            borderless
            :attributes="allAttributes"
            @dayclick="addCalendarItem"
            class="v-calendar-custom"
            locale="th-TH"
            :first-day-of-week="2"
          >
            <template #header-title="{ shortMonthLabel, yearLabel }">
              <span class="text-xl sm:text-2xl font-bold text-purple-800">{{ shortMonthLabel }} {{ yearLabel }}</span>
            </template>
            <template #weekdays="{ weekdays }">
              <div class="vc-weekdays text-sm sm:text-base uppercase font-semibold text-purple-700">
                <div v-for="weekday in weekdays" :key="weekday.id" class="vc-weekday">
                  {{ getThaiDayAbbr(weekday.id) }}
                </div>
              </div>
            </template>
            <template #day-content="{ day, attributes }">
              <div class="day-content flex flex-col items-center relative">
                <span class="day-label text-sm font-medium text-purple-700 bg-white/80 px-2 py-1 rounded-full shadow-inner" :class="{ 'text-lg border-2 border-purple-300': day.isCurrent }">
                  {{ day.day.toString().padStart(2, '0') }}
                </span>
                <div class="dots flex flex-wrap justify-center mt-2">
                  <span
                    v-for="{ key, dot } in attributes"
                    :key="key"
                    :class="['w-2 h-2 rounded-full mx-0.5', dot.class]"
                    @click.stop="handleClickCalendarItem(attributes.find(attr => attr.key === key)?.customData)"
                    @mouseover="showPopover(key, attributes.find(attr => attr.key === key)?.customData)"
                    @mouseleave="hidePopover"
                    class="cursor-pointer hover:scale-125 transition duration-200"
                    :title="attributes.find(attr => attr.key === key)?.popover.label"
                  ></span>
                </div>
                <div v-if="activePopoverKey === key" class="popover absolute z-50 bg-white/95 backdrop-blur-md p-4 rounded-xl shadow-2xl text-purple-800 transform transition-all duration-300" :style="popoverStyle">
                  <h4 class="text-lg font-bold">{{ activePopoverData?.title || activePopoverData?.label }}</h4>
                  <p class="text-sm">{{ activePopoverData?.content || activePopoverData?.message }}</p>
                  <p v-if="activePopoverData?.start_date" class="text-xs">เริ่ม: {{ formatDate(activePopoverData.start_date) }}</p>
                  <p v-if="activePopoverData?.end_date" class="text-xs">สิ้นสุด: {{ formatDate(activePopoverData.end_date) }}</p>
                </div>
              </div>
            </template>
          </VCalendar>
        </div>
      </section>

      <section class="bg-white/95 backdrop-blur-md p-6 rounded-2xl shadow-xl transform hover:scale-101 transition duration-300">
        <h2 class="text-2xl font-bold text-purple-800 mb-6 flex justify-between items-center border-b-2 border-purple-200 pb-2">
          บันทึกย่อ
          <button @click="addNote" class="bg-purple-500 hover:bg-purple-600 text-white font-bold py-2 px-4 rounded-xl shadow-md hover:shadow-lg transition duration-300 transform hover:-translate-y-1">
            + เพิ่มบันทึก
          </button>
        </h2>
        <div v-if="notes.length === 0" class="text-purple-500 text-center italic">
          ยังไม่มีบันทึกย่อ
        </div>
        <div v-else class="space-y-4">
          <NoteCard
            v-for="(noteItem, index) in notes"
            :key="noteItem._id"
            :note="noteItem"
            @delete="deleteNote(noteItem._id)"
            @update:note="handleNoteUpdate(index, $event)"
            @refreshDashboard="refreshAllData"
            class="transform hover:scale-105 transition duration-300"
          />
        </div>
      </section>
    </main>

    <div v-if="showModal" class="fixed inset-0 bg-purple-900/50 flex items-center justify-center z-50">
      <div class="bg-white/95 backdrop-blur-md p-6 rounded-2xl shadow-2xl w-full max-w-md transform hover:scale-105 transition duration-300">
        <h3 class="text-2xl font-bold text-purple-800 mb-6 border-b-2 border-purple-200 pb-2">เพิ่มรายการสำหรับวันที่ {{ selectedDate.toLocaleDateString('th-TH', { dateStyle: 'full' }) }}</h3>
        <div class="flex flex-col space-y-4">
          <button @click="navigateToCreateEvent" class="bg-purple-600 hover:bg-purple-700 text-white font-bold py-3 px-6 rounded-xl shadow-md hover:shadow-lg transition duration-300 transform hover:-translate-y-1">
            เพิ่มกิจกรรม
          </button>
          <button @click="navigateToCreateNoteOnCalendar" class="bg-purple-500 hover:bg-purple-600 text-white font-bold py-3 px-6 rounded-xl shadow-md hover:shadow-lg transition duration-300 transform hover:-translate-y-1">
            เพิ่มบันทึกย่อ (เชื่อมกับปฏิทิน)
          </button>
          <button @click="showModal = false" class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-3 px-6 rounded-xl shadow-md transition duration-300">
            ยกเลิก
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useCookie, useRuntimeConfig, navigateTo } from '#imports';
import { Calendar as VCalendar } from 'v-calendar';

const token = useCookie('token');
const config = useRuntimeConfig();
const apiBase = config.public.apiBase || 'http://localhost:5000/api';

const notes = ref([]);
const events = ref([]);
const calendarEntries = ref([]); // Keep this but don't fetch if endpoint not available
const noteCalendarAttributes = ref([]);
const eventCalendarAttributes = ref([]);
const calendarEntryAttributes = ref([]);
const selectedDate = ref(new Date());
const showModal = ref(false);
const activePopoverKey = ref(null);
const activePopoverData = ref(null);
const popoverStyle = ref({ top: '0px', left: '0px', display: 'none' });

const fetchNotes = async () => {
  if (!token.value) {
    navigateTo('/login');
    return;
  }
  try {
    const response = await $fetch(`${apiBase}/notes`, {
      headers: { Authorization: `Bearer ${token.value}` }
    });
    notes.value = Array.isArray(response) ? response.map(note => ({ ...note, _id: note.id || note._id })) : [];
    noteCalendarAttributes.value = notes.value
      .filter(note => note.note_date)
      .map(note => ({
        key: `note-${note.id || note._id}`,
        dates: new Date(note.note_date),
        popover: { label: `บันทึก: ${note.title}`, visibility: 'hover', hideIndicator: true },
        customData: { id: note.id || note._id, type: 'note_on_calendar', ...note },
        dot: { color: 'yellow', class: 'bg-yellow-500' }
      }));
  } catch (error) {
    console.error('Error fetching notes:', error);
    if (error.response?.status === 401) {
      token.value = null;
      navigateTo('/login');
    }
  }
};

const fetchEvents = async () => {
  if (!token.value) {
    navigateTo('/login');
    return;
  }
  try {
    const response = await $fetch(`${apiBase}/events`, {
      headers: { Authorization: `Bearer ${token.value}` }
    });
    events.value = Array.isArray(response) ? response.map(event => ({ ...event, _id: event.id || event._id })) : [];
    eventCalendarAttributes.value = events.value.map(event => {
      const startDate = new Date(event.start_date);
      const endDate = event.end_date ? new Date(event.end_date) : startDate;
      return {
        key: `event-${event.id || event._id}`,
        dates: { start: startDate, end: endDate },
        popover: { label: `กิจกรรม: ${event.title}`, visibility: 'hover', hideIndicator: true },
        customData: { id: event.id || event._id, type: 'event', ...event },
        dot: { color: 'blue', class: 'bg-blue-500' }
      };
    });
  } catch (error) {
    console.error('Error fetching events:', error);
    if (error.response?.status === 401) {
      token.value = null;
      navigateTo('/login');
    }
  }
};

// Skip fetching calendar_entries if endpoint not available
const fetchCalendarEntries = async () => {
  if (!token.value) {
    navigateTo('/login');
    return;
  }
  try {
    const response = await $fetch(`${apiBase}/calendar_entries`, {
      headers: { Authorization: `Bearer ${token.value}` }
    }).catch(err => {
      if (err.response?.status === 404) {
        console.warn('Endpoint /api/calendar_entries not found, skipping...');
        return { data: [] }; // Return empty data to avoid crash
      }
      throw err;
    });
    calendarEntries.value = Array.isArray(response.data) ? response.data.map(entry => ({ ...entry, _id: entry.id || entry._id })) : [];
    calendarEntryAttributes.value = calendarEntries.value.map(entry => ({
      key: `entry-${entry.id || entry._id}`,
      dates: new Date(entry.date),
      popover: { label: `เตือน: ${entry.message}`, visibility: 'hover', hideIndicator: true },
      customData: { id: entry.id || entry._id, type: 'calendar_entry', ...entry },
      dot: { color: 'red', class: 'bg-red-500' }
    }));
  } catch (error) {
    console.error('Error fetching calendar entries:', error);
    if (error.response?.status === 401) {
      token.value = null;
      navigateTo('/login');
    }
  }
};

const refreshAllData = () => {
  fetchNotes();
  fetchEvents();
  fetchCalendarEntries(); // Keep this but handle 404 gracefully
};

const allAttributes = computed(() => [
  ...noteCalendarAttributes.value,
  ...eventCalendarAttributes.value,
  ...calendarEntryAttributes.value
].filter(attr => attr));

const logout = () => {
  token.value = null;
  navigateTo('/login');
};

const addNote = () => navigateTo('/notes/create');

const deleteNote = async (noteId) => {
  if (!token.value) {
    navigateTo('/login');
    return;
  }
  if (!confirm('คุณแน่ใจหรือไม่ที่จะลบบันทึกนี้?')) return;
  try {
    await $fetch(`${apiBase}/notes/${noteId}`, { method: 'DELETE', headers: { Authorization: `Bearer ${token.value}` } });
    refreshAllData();
  } catch (error) {
    console.error('Error deleting note:', error);
    if (error.response?.status === 401) {
      token.value = null;
      navigateTo('/login');
    }
  }
};

const handleNoteUpdate = (index, updatedNote) => {
  notes.value[index] = { ...notes.value[index], ...updatedNote };
};

const addCalendarItem = (day) => {
  selectedDate.value = day.date;
  showModal.value = true;
};

const navigateToCreateEvent = () => {
  showModal.value = false;
  navigateTo(`/events/create?date=${selectedDate.value.toISOString().split('T')[0]}`);
};

const navigateToCreateNoteOnCalendar = () => {
  showModal.value = false;
  navigateTo(`/notes/create?date=${selectedDate.value.toISOString().split('T')[0]}`);
};

const handleClickCalendarItem = (itemData) => {
  if (!token.value) {
    navigateTo('/login');
    return;
  }
  if (itemData?.type === 'event') navigateTo(`/events/edit/${itemData.id}`);
  else if (itemData?.type === 'calendar_entry') navigateTo(`/calendar-entries/edit/${itemData.id}`);
  else if (itemData?.type === 'note_on_calendar') navigateTo(`/notes/edit/${itemData.id}`);
};

const getThaiDayAbbr = (weekdayId) => {
  const thaiDays = ['อา', 'จ.', 'อ.', 'พ.', 'พฤ', 'ศ.', 'ส.'];
  return thaiDays[(weekdayId - 1 + 7) % 7];
};

const showPopover = (key, data) => {
  activePopoverKey.value = key;
  activePopoverData.value = data || {};
  const rect = event.target.getBoundingClientRect();
  popoverStyle.value = {
    top: `${rect.bottom + window.scrollY + 5}px`,
    left: `${rect.left + window.scrollX - 100}px`,
    display: 'block'
  };
};

const hidePopover = () => {
  activePopoverKey.value = null;
  activePopoverData.value = null;
  popoverStyle.value.display = 'none';
};

const formatDate = (dateStr) => {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  return date.toLocaleString('th-TH', {
    timeZone: 'Asia/Bangkok',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

onMounted(() => refreshAllData());
</script>

<style scoped>
/* CSS เดิม */
.calendar-container {
  overflow-x: auto;
  border-radius: 1rem;
  padding: 0.5rem;
  background: linear-gradient(135deg, #e0c1f4, #f5e6ff);
}

.day-content {
  min-height: 60px;
  position: relative;
}

.day-label {
  position: absolute;
  top: 5px;
  right: 5px;
  z-index: 10;
  transition: all 0.3s ease;
}

.v-calendar-custom .vc-day-content {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 50%;
  padding: 0.25rem;
}

.v-calendar-custom .vc-day-content:hover {
  background: rgba(230, 200, 245, 0.9);
  transform: scale(1.1);
}

.dots {
  position: absolute;
  bottom: 5px;
  left: 0;
  right: 0;
  justify-content: center;
}

.popover {
  min-width: 200px;
  padding: 1rem;
  border-radius: 1rem;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
  animation: popIn 0.3s ease-out;
  display: none;
}

@keyframes popIn {
  from {
    opacity: 0;
    transform: scale(0.8);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

@media (max-width: 640px) {
  .day-label { font-size: 0.75rem; padding: 0.125rem 0.5rem; }
  .dots span { width: 1.5px; height: 1.5px; }
  header { flex-direction: column; gap: 1rem; }
  nav button { width: 100%; }
  main { grid-template-columns: 1fr; }
  .calendar-container { max-width: 100%; }
}

@media (min-width: 641px) and (max-width: 1024px) {
  main { grid-template-columns: 1fr 1fr; }
  .calendar-container { max-width: 100%; }
}
</style>