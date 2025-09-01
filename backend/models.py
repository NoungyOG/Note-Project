# backend/models.py
from mongoengine import Document, StringField, ReferenceField, DateTimeField, BooleanField, ObjectIdField
from datetime import datetime

class User(Document):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    # เพิ่ม role, name ถ้ามีตาม schema อื่นๆ ที่เคยเห็น
    # role = StringField(default='user')
    # name = StringField()

class Note(Document):
    user_id = ReferenceField(User, required=True)
    title = StringField(required=True)
    content = StringField()
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    # เพิ่ม field สำหรับเก็บวันที่เกี่ยวข้องสำหรับปฏิทิน
    note_date = DateTimeField() # <-- เพิ่ม field นี้เข้ามา

class Event(Document):
    user_id = ReferenceField(User, required=True)
    title = StringField(required=True)
    description = StringField()
    start_date = DateTimeField(required=True)
    end_date = DateTimeField()
    all_day = BooleanField(default=False)
    category = StringField()
    location = StringField()
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

# ----------------------------------------------------
# **เพิ่มคลาส CalendarEntry นี้เข้ามาใน models.py**
# class CalendarEntry(Document):
#     user_id = ReferenceField(User, required=True)
#     message = StringField(required=True)
#     date = DateTimeField(required=True) # วันที่ของข้อความเตือน
#     created_at = DateTimeField(default=datetime.utcnow)
#     updated_at = DateTimeField(default=datetime.utcnow)
#     def to_json(self):
#         return {
#             "id": str(self.id), # ใช้ str(self.id) เพื่อแปลง ObjectId ให้เป็น string
#             "message": self.message,
#             "date": self.date.isoformat(), # ส่งวันที่เป็น ISO format
#             "created_at": self.created_at.isoformat(),
#             "updated_at": self.updated_at.isoformat()
#         }
# ----------------------------------------------------