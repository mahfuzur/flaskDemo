from datetime import datetime
from dataclasses import dataclass
from app.config.db import db


@dataclass
class Post(db.Model):
    id: int
    title: str
    body: str
    published_at: str
    created_at: datetime
    updated_at: datetime
    created_by: int
    updated_by: int

    __tablename__ = "posts"

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
