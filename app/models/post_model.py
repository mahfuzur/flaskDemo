from datetime import datetime
from dataclasses import dataclass
from app.config.db import db


@dataclass
class Post(db.Model):
    __tablename__ = "posts"

    id: db.Integer
    title: db.String
    body: db.Text
    published_at: db.DateTime
    created_at: db.DateTime
    updated_at: db.DateTime
    created_by: db.Integer
    updated_by: db.Integer

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)
    published_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, nullable=False)
    updated_by = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Post {self.id}: {self.title}>"

    def __hash__(self):
        return hash(self.name)
