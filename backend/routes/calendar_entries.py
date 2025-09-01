# backend/routes/calendar_entries.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
# from models import User, CalendarEntry
from datetime import datetime

calendar_entries = Blueprint('calendar_entries', __name__, url_prefix='/calendar_entries')

# Helper function to convert CalendarEntry object to dictionary for JSON response
def calendar_entry_to_dict(entry):
    return {
        "id": str(entry.id), # Convert ObjectId to string
        "user_id": str(entry.user_id.id),
        "message": entry.message,
        "date": entry.date.isoformat(), # ISO format for date
        "created_at": entry.created_at.isoformat(),
        "updated_at": entry.updated_at.isoformat()
    }

# --- GET all calendar entries for a user ---
@calendar_entries.route('', methods=['GET'])
@jwt_required()
def get_calendar_entries():
    current_user_id = get_jwt_identity()
    user = User.objects(username=current_user_id).first()
    if not user:
        return jsonify({"msg": "User not found"}), 404

    entries = CalendarEntry.objects(user_id=user.id).order_by('-date', '-created_at') # Order by date descending
    return jsonify([calendar_entry_to_dict(entry) for entry in entries]), 200

# --- CREATE a new calendar entry ---
@calendar_entries.route('', methods=['POST']) # <--- THIS IS THE CRITICAL LINE FOR POST REQUESTS
@jwt_required()
def create_calendar_entry():
    current_user_id = get_jwt_identity()
    user = User.objects(username=current_user_id).first()
    if not user:
        return jsonify({"msg": "User not found"}), 404

    data = request.get_json()
    message = data.get('message')
    date_str = data.get('date') # Expecting 'YYYY-MM-DD'

    if not message or not date_str:
        return jsonify({"msg": "Message and date are required"}), 400

    try:
        # Assuming date_str is in 'YYYY-MM-DD' format
        entry_date = datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return jsonify({"msg": "Invalid date format. Use YYYY-MM-DD"}), 400

    try:
        new_entry = CalendarEntry(
            user_id=user.id,
            message=message,
            date=entry_date # Store as datetime object
        )
        new_entry.save()
        return jsonify(calendar_entry_to_dict(new_entry)), 201
    except Exception as e:
        return jsonify({"msg": f"Error creating calendar entry: {str(e)}"}), 500

# --- GET a single calendar entry by ID ---
@calendar_entries.route('/<id>', methods=['GET'])
@jwt_required()
def get_calendar_entry(id):
    current_user_id = get_jwt_identity()
    user = User.objects(username=current_user_id).first()
    if not user:
        return jsonify({"msg": "User not found"}), 404

    entry = CalendarEntry.objects(id=id, user_id=user.id).first()
    if not entry:
        return jsonify({"msg": "Calendar entry not found"}), 404
    return jsonify(calendar_entry_to_dict(entry)), 200

# --- UPDATE a calendar entry ---
@calendar_entries.route('/<id>', methods=['PUT'])
@jwt_required()
def update_calendar_entry(id):
    current_user_id = get_jwt_identity()
    user = User.objects(username=current_user_id).first()
    if not user:
        return jsonify({"msg": "User not found"}), 404

    entry = CalendarEntry.objects(id=id, user_id=user.id).first()
    if not entry:
        return jsonify({"msg": "Calendar entry not found"}), 404

    data = request.get_json()
    message = data.get('message')
    date_str = data.get('date')

    if not message or not date_str:
        return jsonify({"msg": "Message and date are required"}), 400

    try:
        entry_date = datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return jsonify({"msg": "Invalid date format. Use YYYY-MM-DD"}), 400

    try:
        entry.update(
            message=message,
            date=entry_date,
            updated_at=datetime.utcnow()
        )
        # Fetch the updated object to return
        updated_entry = CalendarEntry.objects(id=id).first()
        return jsonify(calendar_entry_to_dict(updated_entry)), 200
    except Exception as e:
        return jsonify({"msg": f"Error updating calendar entry: {str(e)}"}), 500

# --- DELETE a calendar entry ---
@calendar_entries.route('/<id>', methods=['DELETE'])
@jwt_required()
def delete_calendar_entry(id):
    current_user_id = get_jwt_identity()
    user = User.objects(username=current_user_id).first()
    if not user:
        return jsonify({"msg": "User not found"}), 404

    entry = CalendarEntry.objects(id=id, user_id=user.id).first()
    if not entry:
        return jsonify({"msg": "Calendar entry not found"}), 404

    try:
        entry.delete()
        return jsonify({"msg": "Calendar entry deleted successfully"}), 200
    except Exception as e:
        return jsonify({"msg": f"Error deleting calendar entry: {str(e)}"}), 500