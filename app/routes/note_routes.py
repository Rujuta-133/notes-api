from flask import Blueprint,request
from ..models.note import Note
from ..extensions import db

notes_bp = Blueprint("notes", __name__)

@notes_bp.route("/notes", methods=["POST"])
def create_note():
    #get json data
    data = request.get_json()
    if not data:
        return {"error" : "Invalid request body"}
    
    title = data.get("title")
    content = data.get("content")

    if not title.strip():
        return {"error" : "Title not present"}
    
    if not content.strip():
        return {"error" : "Content not present"}

    note = Note(title = title, content = content)

    db.session.add(note)
    db.session.commit()

    return {"message" : "Note created"}

@notes_bp.route("/notes", methods=["GET"])
def get_note():
    notes = Note.query.all()

    note_list = []

    for note in notes:
        note_dict = {"id" : note.id, "title": note.title, "content": note.content}
        note_list.append(note_dict)

    return {"notes": note_list}


@notes_bp.route("/notes/<int:id>", methods=["GET"])
def get_note_by_id(id): 
    note_with_id = Note.query.get(id)
    if note_with_id is None:
        return {"error" : "Note not found"}
    
    return {"id": note_with_id.id, "title": note_with_id.title, "content": note_with_id.content}


@notes_bp.route("/notes/<int:id>", methods=["DELETE"])
def delete_note(id):
    note_with_id = Note.query.get(id)
    if note_with_id is None:
        return {"error" : "Note not found"}
    
    db.session.delete(note_with_id)
    db.session.commit()

    return {"message" : "Note deleted"}

@notes_bp.route("/notes/<int:id>", methods=["PUT"])
def update_note(id):
    note_with_id = Note.query.get(id)
    if note_with_id is None:
        return {"error" : "Note not found"}
    
    note_to_update = request.get_json()

    if not note_to_update:
        return {"error" : "Invalid request body"}

    title = note_to_update.get("title")
    content = note_to_update.get("content")

    if title is None and content is None:
        return {"error" : "Title and content required"}

    if title is not None and not title.strip():
        return {"error" : "Title cannot be empty"}
    
    if content is not None and not content.strip():
        return {"error" : "Content cannot be empty"}
        
    if title is not None:    
        note_with_id.title =  title
    
    if content is not None:
        note_with_id.content = content


    db.session.commit()

    return {"message" : "Note updated"}
