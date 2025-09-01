const express = require('express');
const cors = require('cors');
const app = express();

app.use(express.json());
app.use(cors({
  origin: 'http://localhost:3000', // อนุญาตให้ localhost:3000 เข้าถึง
  credentials: true, // อนุญาต cookie/token
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'], // อนุญาต method ต่างๆ
  allowedHeaders: ['Authorization', 'Content-Type'] // อนุญาต header
}));

// Middleware ตรวจสอบ token (ตัวอย่าง)
const authenticateToken = (req, res, next) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];
  if (!token) return res.status(401).json({ msg: 'No token provided' });
  // ตรวจสอบ token (สมมติใช้ JWT)
  // if (jwt.verify(token, 'your_secret_key')) return next();
  next(); // ลบ comment และเพิ่ม logic JWT ถ้ามี
};

// Route สำหรับ notes
app.get('/api/notes/:id', authenticateToken, (req, res) => {
  const { id } = req.params;
  res.json({ id, title: 'Sample Title', content: 'Sample Content' }); // ตัวอย่างข้อมูล
});

app.put('/api/notes/:id', authenticateToken, (req, res) => {
  const { id } = req.params;
  const { title, content } = req.body;
  if (!title || !content) return res.status(400).json({ msg: 'Missing title or content' });
  // อัปเดตข้อมูล (สมมติใช้ array หรือ database)
  res.json({ id, title, content, message: 'Note updated successfully' });
});

app.listen(5000, () => console.log('Server running on port 5000'));