from ..extensions import db
from datetime import datetime

class Zapis(db.Model):
    __tablename__ = 'zapis'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
   

    def __repr__(self):
        return f'<Zapis {self.title}>'