# backend/routes/events.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Event, User # ตรวจสอบให้แน่ใจว่า Event และ User ถูก import จาก models.py
from datetime import datetime, timezone # เพิ่ม timezone

events = Blueprint('events', __name__)

@events.route('/events', methods=['GET'])
@jwt_required()
def get_events():
    user_id = get_jwt_identity()
    events_list = Event.objects(user_id=user_id).order_by('start_date')
    return jsonify([{
        "id": str(event.id),
        "title": event.title,
        "description": event.description,
        # ส่งวันที่เป็น ISO format (พร้อม timezone information เพื่อความถูกต้อง)
        "start_date": event.start_date.isoformat(),
        "end_date": event.end_date.isoformat() if event.end_date else None,
        "all_day": event.all_day,
        "category": event.category,
        "location": event.location
    } for event in events_list]), 200

@events.route('/events/<event_id>', methods=['GET'])
@jwt_required()
def get_event(event_id):
    user_id = get_jwt_identity()
    event = Event.objects(id=event_id, user_id=user_id).first()
    if not event:
        return jsonify({"msg": "Event not found or unauthorized"}), 404
    return jsonify({
        "id": str(event.id),
        "title": event.title,
        "description": event.description,
        "start_date": event.start_date.isoformat(),
        "end_date": event.end_date.isoformat() if event.end_date else None,
        "all_day": event.all_day,
        "category": event.category,
        "location": event.location
    }), 200

@events.route('/events', methods=['POST'])
@jwt_required()
def create_event():
    user_id = get_jwt_identity()
    data = request.get_json()
    user = User.objects(id=user_id).first()

    start_date_str = data.get('start_date')
    if not start_date_str:
        return jsonify({"msg": "Start date is required"}), 400

    try:
        # พยายาม parse เป็น ISO format ก่อน
        start_date = datetime.fromisoformat(start_date_str)
        if start_date.tzinfo is None: # ถ้าไม่มี timezone (naive datetime), ให้ถือว่าเป็น UTC
            start_date = start_date.replace(tzinfo=timezone.utc)
    except ValueError:
        # ถ้าไม่ใช่ ISO format (เช่น 'YYYY-MM-DD' จากการคลิกวัน), ให้เติมเวลาเริ่มต้นเป็น 00:00:00 UTC
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        except ValueError:
            return jsonify({"msg": "Invalid start_date format"}), 400

    end_date = None
    if data.get('end_date'):
        end_date_str = data['end_date']
        try:
            end_date = datetime.fromisoformat(end_date_str)
            if end_date.tzinfo is None:
                end_date = end_date.replace(tzinfo=timezone.utc)
        except ValueError:
            try:
                end_date = datetime.strptime(end_date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
            except ValueError:
                return jsonify({"msg": "Invalid end_date format"}), 400

    event = Event(
        user_id=user,
        title=data.get('title'),
        description=data.get('description'),
        start_date=start_date,
        end_date=end_date,
        all_day=data.get('all_day', False),
        category=data.get('category'),
        location=data.get('location')
    )
    event.save()
    return jsonify({"msg": "Event created!", "id": str(event.id)}), 201

@events.route('/events/<event_id>', methods=['PUT'])
@jwt_required()
def update_event(event_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    event = Event.objects(id=event_id, user_id=user_id).first()
    if not event:
        return jsonify({"msg": "Event not found or unauthorized"}), 404
    
    update_data = {
        'updated_at': datetime.utcnow()
    }
    
    if 'title' in data: update_data['title'] = data['title']
    if 'description' in data: update_data['description'] = data['description']
    
    if 'start_date' in data:
        start_date_str = data['start_date']
        try:
            parsed_start_date = datetime.fromisoformat(start_date_str)
            if parsed_start_date.tzinfo is None:
                parsed_start_date = parsed_start_date.replace(tzinfo=timezone.utc)
            update_data['start_date'] = parsed_start_date
        except ValueError:
            try:
                parsed_start_date = datetime.strptime(start_date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
                update_data['start_date'] = parsed_start_date
            except ValueError:
                return jsonify({"msg": "Invalid start_date format"}), 400
                
    if 'end_date' in data:
        if data['end_date'] is not None:
            end_date_str = data['end_date']
            try:
                parsed_end_date = datetime.fromisoformat(end_date_str)
                if parsed_end_date.tzinfo is None:
                    parsed_end_date = parsed_end_date.replace(tzinfo=timezone.utc)
                update_data['end_date'] = parsed_end_date
            except ValueError:
                try:
                    parsed_end_date = datetime.strptime(end_date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
                    update_data['end_date'] = parsed_end_date
                except ValueError:
                    return jsonify({"msg": "Invalid end_date format"}), 400
        else: # อนุญาตให้ตั้งค่า end_date เป็น None
            update_data['end_date'] = None
            
    if 'all_day' in data: update_data['all_day'] = data['all_day']
    if 'category' in data: update_data['category'] = data['category']
    if 'location' in data: update_data['location'] = data['location']

    try:
        event.update(**update_data) # ใช้ .update() สำหรับการอัปเดตแบบ field-by-field
        return jsonify({"msg": "Event updated!"}), 200
    except Exception as e:
        return jsonify({"msg": f"Update failed: {str(e)}"}), 500

@events.route('/events/<event_id>', methods=['DELETE'])
@jwt_required()
def delete_event(event_id):
    user_id = get_jwt_identity()
    event = Event.objects(id=event_id, user_id=user_id).first()
    if not event:
        return jsonify({"msg": "Event not found or unauthorized"}), 404
    event.delete()
    return jsonify({"msg": "Event deleted!"}), 200