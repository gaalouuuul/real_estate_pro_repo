from app.extensions import db
from .base import TimestampMixin


class VisitRequest(db.Model, TimestampMixin):
    __tablename__ = "visit_requests"

    id           = db.Column(db.Integer, primary_key=True)
    property_id  = db.Column(db.Integer, db.ForeignKey("properties.id"), nullable=False)
    requester_id = db.Column(db.Integer, db.ForeignKey("users.id"),      nullable=False)
    requested_at = db.Column(db.String(30),  nullable=False)
    status       = db.Column(db.String(30),  nullable=False, default="pending", index=True)
    message      = db.Column(db.String(500), nullable=True)

    # Relations
    property  = db.relationship("Property", backref="visit_requests")
    requester = db.relationship("User",     backref="visit_requests")

    def to_dict(self) -> dict:
        return {
            "id":           self.id,
            "property_id":  self.property_id,
            "requester_id": self.requester_id,
            "requested_at": self.requested_at,
            "status":       self.status,
            "message":      self.message,
            "created_at":   self.created_at.isoformat() if self.created_at else None,
            "updated_at":   self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self) -> str:
        return f"<VisitRequest property={self.property_id} requester={self.requester_id} status={self.status}>"