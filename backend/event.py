from mongoengine import Document, ObjectIdField, ReferenceField, StringField, DateTimeField, BooleanField
from datetime import datetime

class Event(Document):
    user_id = ReferenceField('User', required=True)
    title = StringField(required=True)
    description = StringField()
    start_date = DateTimeField(required=True)
    end_date = DateTimeField()
    all_day = BooleanField(default=False)
    category = StringField()
    location = StringField()
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)