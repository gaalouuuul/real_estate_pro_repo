from app.extensions import db
from .base import TimestampMixin
import bcrypt


class User(db.Model, TimestampMixin):
    __tablename__ = "users"

    id            = db.Column(db.Integer, primary_key=True)
    first_name    = db.Column(db.String(100), nullable=False)
    last_name     = db.Column(db.String(100), nullable=False)
    birth_date    = db.Column(db.String(20),  nullable=True)
    email         = db.Column(db.String(255), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role          = db.Column(db.String(20),  nullable=False, default="user", index=True)

    # Relations
    properties = db.relationship("Property", backref="owner", lazy=True, cascade="all, delete-orphan")
    favorites  = db.relationship("Favorite", backref="user",  lazy=True, cascade="all, delete-orphan")

    def check_password(self, password: str) -> bool:
        """Vérifie le mot de passe fourni contre le hash stocké."""
        return bcrypt.checkpw(
            password.encode("utf-8"),
            self.password_hash.encode("utf-8")
        )

    def to_dict(self) -> dict:
        return {
            "id":         self.id,
            "first_name": self.first_name,
            "last_name":  self.last_name,
            "birth_date": self.birth_date,
            "email":      self.email,
            "role":       self.role,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self) -> str:
        return f"<User {self.email}>"