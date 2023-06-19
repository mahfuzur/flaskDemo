from app.config.db import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    encrypted_password = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )

    def __init__(self, full_name, email, encrypted_password):
        self.full_name = full_name
        self.email = email
        self.encrypted_password = encrypted_password

    def __repr__(self):
        return f"<User {self.id}: {self.email}>"
