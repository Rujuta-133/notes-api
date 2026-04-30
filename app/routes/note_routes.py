from flask import Blueprint,request
from ..models.note import Note
from ..extensions import db

notes_bp = Blueprint("notes", __name__)

@notes_bp.route("/notes", methods=["POST"])
def create_note():
    #get json data
    data = request.get_json()

    title = data.get("title")
    content = data.get("content")

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




