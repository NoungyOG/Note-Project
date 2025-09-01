# xAI API Documentation

Base URL: `http://localhost:5000/api`. All endpoints use JWT authentication (except `/api/register` and `/api/login`).

## Authentication
### Register
- **Endpoint**: `/api/register`
- **Method**: `POST`
- **Body**: `{"username": "string", "password": "string"}`
- **Response (201)**: `{"msg": "User registered successfully"}`
- **Response (400)**: `{"msg": "Username already exists"}`
- **Note**: Username must be unique.

### Login
- **Endpoint**: `/api/login`
- **Method**: `POST`
- **Body**: `{"username": "string", "password": "string"}`
- **Response (200)**: `{"access_token": "your_jwt_token_here"}`
- **Response (401)**: `{"msg": "Invalid credentials"}`
- **Note**: Use `Authorization: Bearer <token>` for other endpoints.

## Notes
### Get All Notes
- **Endpoint**: `/api/notes`
- **Method**: `GET`
- **Headers**: `Authorization: Bearer <token>`
- **Response (200)**: `[{"id": "note_id", "title": "string", "content": "string", "created_at": "timestamp", "updated_at": "timestamp"}]`
- **Note**: Returns `[]` if no notes.

### Create Note
- **Endpoint**: `/api/notes`
- **Method**: `POST`
- **Headers**: `Authorization: Bearer <token>`
- **Body**: `{"title": "string", "content": "string"}`
- **Response (201)**: `{"msg": "Note created!", "id": "note_id"}`

### Get Note
- **Endpoint**: `/api/notes/{note_id}`
- **Method**: `GET`
- **Headers**: `Authorization: Bearer <token>`
- **Response (200)**: `{"id": "note_id", "title": "string", "content": "string", "created_at": "timestamp", "updated_at": "timestamp"}`
- **Response (404)**: If not found.

### Update Note
- **Endpoint**: `/api/notes/{note_id}`
- **Method**: `PUT`
- **Headers**: `Authorization: Bearer <token>`
- **Body**: `{"title": "string", "content": "string"}`
- **Response (200)**: `{"msg": "Note updated!"}`
- **Response (404)**: If not found.

### Delete Note
- **Endpoint**: `/api/notes/{note_id}`
- **Method**: `DELETE`
- **Headers**: `Authorization: Bearer <token>`
- **Response (200)**: `{"msg": "Note deleted!"}`
- **Response (404)**: If not found.

## Events
### Get All Events
- **Endpoint**: `/api/events`
- **Method**: `GET`
- **Headers**: `Authorization: Bearer <token>`
- **Response (200)**: `[{"id": "event_id", "title": "string", "description": "string", "start_date": "timestamp", "end_date": "timestamp", "all_day": bool, "category": "string", "location": "string"}]`
- **Note**: Returns `[]` if no events.

### Create Event
- **Endpoint**: `/api/events`
- **Method**: `POST`
- **Headers**: `Authorization: Bearer <token>`
- **Body**: `{"title": "string", "description": "string", "start_date": "YYYY-MM-DD", "end_date": "YYYY-MM-DD", "all_day": bool, "category": "string", "location": "string"}`
- **Response (201)**: `{"msg": "Event created!", "id": "event_id"}`
- **Response (400)**: If date invalid.

### Get Event
- **Endpoint**: `/api/events/{event_id}`
- **Method**: `GET`
- **Headers**: `Authorization: Bearer <token>`
- **Response (200)**: `{"id": "event_id", "title": "string", "description": "string", "start_date": "timestamp", "end_date": "timestamp", "all_day": bool, "category": "string", "location": "string"}`
- **Response (404)**: If not found.

### Update Event
- **Endpoint**: `/api/events/{event_id}`
- **Method**: `PUT`
- **Headers**: `Authorization: Bearer <token>`
- **Body**: `{"title": "string", "description": "string", "start_date": "YYYY-MM-DD", "end_date": "YYYY-MM-DD", "all_day": bool, "category": "string", "location": "string"}`
- **Response (200)**: `{"msg": "Event updated!"}`
- **Response (400)**: If date invalid.

### Delete Event
- **Endpoint**: `/api/events/{event_id}`
- **Method**: `DELETE`
- **Headers**: `Authorization: Bearer <token>`
- **Response (200)**: `{"msg": "Event deleted!"}`
- **Response (404)**: If not found.

## Calendar Entries (Optional)
### Get All Calendar Entries
- **Endpoint**: `/api/calendar_entries`
- **Method**: `GET`
- **Headers**: `Authorization: Bearer <token>`
- **Response (200)**: `[{"id": "calendar_id", "user_id": "user_id", "message": "string", "date": "timestamp", "created_at": "timestamp", "updated_at": "timestamp"}]`
- **Note**: Returns `[]` if none; requires uncommenting in `app.py`.

### Create Calendar Entry
- **Endpoint**: `/api/calendar_entries`
- **Method**: `POST`
- **Headers**: `Authorization: Bearer <token>`
- **Body**: `{"message": "string", "date": "YYYY-MM-DD"}`
- **Response (201)**: `{"id": "calendar_id", "user_id": "user_id", "message": "string", "date": "timestamp", "created_at": "timestamp", "updated_at": "timestamp"}`
- **Response (400)**: If date invalid.

### Get Calendar Entry
- **Endpoint**: `/api/calendar_entries/{id}`
- **Method**: `GET`
- **Headers**: `Authorization: Bearer <token>`
- **Response (200)**: `{"id": "calendar_id", "user_id": "user_id", "message": "string", "date": "timestamp", "created_at": "timestamp", "updated_at": "timestamp"}`
- **Response (404)**: If not found.

### Update Calendar Entry
- **Endpoint**: `/api/calendar_entries/{id}`
- **Method**: `PUT`
- **Headers**: `Authorization: Bearer <token>`
- **Body**: `{"message": "string", "date": "YYYY-MM-DD"}`
- **Response (200)**: `{"id": "calendar_id", "user_id": "user_id", "message": "string", "date": "timestamp", "created_at": "timestamp", "updated_at": "timestamp"}`
- **Response (400)**: If date invalid.

### Delete Calendar Entry
- **Endpoint**: `/api/calendar_entries/{id}`
- **Method**: `DELETE`
- **Headers**: `Authorization: Bearer <token>`
- **Response (200)**: `{"msg": "Calendar entry deleted successfully"}`
- **Response (404)**: If not found.

## General Notes
- **Auth**: Use `Bearer <token>` for protected endpoints.
- **Date**: Use `YYYY-MM-DD` format.
- **Errors**: 400 (invalid input), 401 (unauthorized), 404 (not found).
- **Env**: MongoDB at `localhost:27017`, DB `simple_notes`.
- **Security**: Update `SECRET_KEY` and `JWT_SECRET_KEY` in `config.py`.