// frontend/tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./components/**/*.{js,vue,ts}",
    "./layouts/**/*.vue",
    "./pages/**/*.vue",
    "./plugins/**/*.{js,ts}",
    "./app.vue",
    "./error.vue",
  ],
  theme: {
    extend: {
      colors: {
        // เพิ่มโทนสีม่วงพาสเทล
        'pastel-purple': {
          50: '#FDF7FE',  // Very light purple (almost white)
          100: '#FAE8FC', // Lighter purple
          200: '#F5D6FA',
          300: '#EEC2F6',
          400: '#E29DEE', // Main pastel purple
          500: '#D57AD4',
          600: '#BF5EBE',
          700: '#A144A2',
          800: '#832B87',
          900: '#641C6C',
        },
        // ปรับสีที่มีอยู่ให้เข้ากับธีม หรือสร้างชื่อใหม่เพื่อให้เรียกง่ายขึ้น
        // ตัวอย่าง:
        primary: '#E29DEE', // pastel-purple-400
        secondary: '#A144A2', // pastel-purple-700
        accent: '#D57AD4',   // pastel-purple-500
        neutral: '#FDF7FE',  // pastel-purple-50
        'dark-purple': '#641C6C', // pastel-purple-900
      },
    },
  },
  plugins: [],
}