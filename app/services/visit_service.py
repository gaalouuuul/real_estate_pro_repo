from app.extensions import db
from app.models.visit_request import VisitRequest
from app.utils.errors import ApiError

VALID_STATUSES = ("pending", "accepted", "rejected")


class VisitService:

    @staticmethod
    def create(property_id, data):
        if not data:
            raise ApiError("invalid payload", 400)

        if not data.get("requester_id"):
            raise ApiError("requester_id is required", 400)
        if not data.get("requested_at"):
            raise ApiError("requested_at is required", 400)

        visit = VisitRequest(
            property_id  = property_id,
            requester_id = data["requester_id"],
            requested_at = data["requested_at"],
            message      = data.get("message"),
            status       = "pending",
        )
        db.session.add(visit)
        db.session.commit()
        return visit

    @staticmethod
    def get_by_id(visit_id):
        visit = VisitRequest.query.get(visit_id)
        if not visit:
            raise ApiError("visit request not found", 404)
        return visit

    @staticmethod
    def get_by_property(property_id):
        return VisitRequest.query.filter_by(property_id=property_id).all()

    @staticmethod
    def update_status(visit_id, data):
        if not data:
            raise ApiError("invalid payload", 400)

        status = data.get("status")
        if not status:
            raise ApiError("status is required", 400)
        if status not in VALID_STATUSES:
            raise ApiError(f"status must be one of: {', '.join(VALID_STATUSES)}", 400)

        visit = VisitRequest.query.get(visit_id)
        if not visit:
            raise ApiError("visit request not found", 404)

        visit.status = status
        db.session.commit()
        return visit