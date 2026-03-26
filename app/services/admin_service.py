from app.models.audit_log import AuditLog
from app.models.property import Property
from app.models.room import Room


class AdminService:
    @staticmethod
    def property_stats():
        properties = Property.query.all()

        total_properties = len(properties)
        active_properties = len([p for p in properties if not p.archived])
        archived_properties = len([p for p in properties if p.archived])
        published_properties = len([p for p in properties if p.status == "published"])
        total_rooms = Room.query.count()

        by_city = {}
        for prop in properties:
            by_city[prop.city] = by_city.get(prop.city, 0) + 1

        return {
            "total_properties": total_properties,
            "active_properties": active_properties,
            "archived_properties": archived_properties,
            "published_properties": published_properties,
            "total_rooms": total_rooms,
            "by_city": by_city,
        }

    @staticmethod
    def audit_logs(limit=100):
        logs = AuditLog.query.order_by(AuditLog.created_at.desc(), AuditLog.id.desc()).limit(limit).all()
        return [log.to_dict() for log in logs]