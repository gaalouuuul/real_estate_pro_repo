from datetime import datetime
from app.extensions import db


class Property(db.Model):
    __tablename__ = "properties"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    city = db.Column(db.String(100), nullable=False)
    property_type = db.Column("type", db.String(50), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    price = db.Column(db.Integer, nullable=True)
    surface = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(30), nullable=False, default="draft")
    archived = db.Column(db.Boolean, nullable=False, default=False)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    rooms = db.relationship(
        "Room",
        backref="property",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "city": self.city,
            "type": self.property_type,
            "owner_id": self.owner_id,
            "price": self.price,
            "surface": self.surface,
            "status": self.status,
            "archived": self.archived,
            "room_count": len(self.rooms),
            "rooms": [
                {
                    "id": room.id,
                    "name": room.name,
                    "size": room.size,
                    "features": room.features,
                    "property_id": room.property_id,
                }
                for room in self.rooms
            ],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }