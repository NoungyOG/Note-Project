import VCalendar from 'v-calendar';
import 'v-calendar/dist/style.css'; // **สำคัญมาก** สำหรับ Stylesheet ของ v-calendar

export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.vueApp.use(VCalendar, {});
});