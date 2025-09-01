from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from mongoengine import connect
from config import Config

from routes.auth import auth
from routes.notes import notes
from routes.events import events # <-- เพิ่มบรรทัดนี้
# from routes.calendar_entries import calendar_entries # <-- เพิ่มบรรทัดนี้

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
jwt = JWTManager(app)

# เชื่อมต่อ MongoDB ด้วย mongoengine
connect(
    db=app.config["MONGODB_SETTINGS"]["db"],
    host=app.config["MONGODB_SETTINGS"]["host"],
    port=app.config["MONGODB_SETTINGS"]["port"]
)

# Register Blueprints
app.register_blueprint(auth, url_prefix="/api")
app.register_blueprint(notes, url_prefix="/api")
app.register_blueprint(events, url_prefix="/api") # <-- เพิ่มบรรทัดนี้
# app.register_blueprint(calendar_entries, url_prefix="/api") 

if __name__ == "__main__":
    app.run(debug=True)