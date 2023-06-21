from dataclasses import dataclass

from app.config.db import db


@dataclass
class User(db.Model):
    __tablename__ = "users"

    id: db.Integer
    full_name: db.String
    email: db.String
    role: db.String
    created_at: db.DateTime

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    encrypted_password = db.Column(db.String(100))
    role = db.Column(db.Enum('user', 'admin'), default='user')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )

    def __repr__(self):
        return f"<User {self.id}: {self.email}>"

    def __hash__(self):
        return hash(self.name)
