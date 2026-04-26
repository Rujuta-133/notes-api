from ..extensions import db 

class Note(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200))
    content = db.Column(db.Text)
    
    
