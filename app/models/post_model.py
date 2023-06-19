from datetime import datetime

from app.config.db import db


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)
    published_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, nullable=False)
    updated_by = db.Column(db.Integer, nullable=False)

    def __init__(self, title, body, created_by, updated_by):
        self.title = title
        self.body = body
        self.created_by = created_by
        self.updated_by = updated_by

    def __repr__(self):
        return f"<Post {self.id}: {self.title}>"
