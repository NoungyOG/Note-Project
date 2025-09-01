class Config:
    SECRET_KEY = 'your-secret-key'
    JWT_SECRET_KEY = 'your-jwt-secret'
    MONGODB_SETTINGS = {
        'db': 'simple_notes',  # เปลี่ยนฐานข้อมูลเป็น simple_notes
        'host': 'localhost',
        'port': 27017
    }