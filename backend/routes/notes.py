from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Note, User
from datetime import datetime

notes = Blueprint('notes', __name__)

@notes.route('/notes', methods=['GET'])
@jwt_required()
def get_notes():
    user_id = get_jwt_identity()
    user = User.objects(id=user_id).first()
    notes_list = Note.objects(user_id=user).order_by('-created_at')
    return jsonify([{
        "id": str(note.id),
        "title": note.title,
        "content": note.content,
        "created_at": note.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": note.updated_at.strftime("%Y-%m-%d %H:%M:%S")
    } for note in notes_list]), 200

@notes.route('/notes/<note_id>', methods=['GET'])
@jwt_required()
def get_note(note_id):
    user_id = get_jwt_identity()
    note = Note.objects(id=note_id, user_id=user_id).first()
    if not note:
        return jsonify({"msg": "Note not found or unauthorized"}), 404
    return jsonify({
        "id": str(note.id),
        "title": note.title,
        "content": note.content,
        "created_at": note.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": note.updated_at.strftime("%Y-%m-%d %H:%M:%S")
    }), 200

@notes.route('/notes', methods=['POST'])
@jwt_required()
def create_note():
    user_id = get_jwt_identity()
    data = request.get_json()
    user = User.objects(id=user_id).first()
    note = Note(user_id=user, title=data['title'], content=data['content']).save()
    return jsonify({"msg": "Note created!", "id": str(note.id)}), 201

@notes.route('/notes/<note_id>', methods=['PUT'])
@jwt_required()
def update_note(note_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    note = Note.objects(id=note_id, user_id=user_id).first()
    if not note:
        return jsonify({"msg": "Note not found or unauthorized"}), 404
    try:
        note.update(
            title=data.get('title', note.title),
            content=data.get('content', note.content),
            updated_at=datetime.utcnow()
        )
        return jsonify({"msg": "Note updated!"}), 200
    except Exception as e:
        return jsonify({"msg": f"Update failed: {str(e)}"}), 500

@notes.route('/notes/<note_id>', methods=['DELETE'])
@jwt_required()
def delete_note(note_id):
    user_id = get_jwt_identity()
    note = Note.objects(id=note_id, user_id=user_id).first()
    if not note:
        return jsonify({"msg": "Note not found or unauthorized"}), 404
    note.delete()
    return jsonify({"msg": "Note deleted!"}), 200