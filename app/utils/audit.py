from app.extensions import db
from app.models.audit_log import AuditLog


def log_action(action, entity_type, entity_id, actor_id=None, details=None):
    log = AuditLog(
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        actor_id=actor_id,
        details=details,
    )
    db.session.add(log)
    db.session.commit()
    return log