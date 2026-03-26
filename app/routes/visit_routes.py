from flask import Blueprint, request, jsonify
from app.utils.errors import ApiError

bp = Blueprint("visits", __name__)


def _get_json():
    data = request.get_json(silent=True)
    if data is None:
        raise ApiError("Content-Type must be application/json", 415)
    return data


@bp.route("/properties/<int:property_id>/visit-requests", methods=["POST"])
def create_visit_request(property_id):
    """
    Create a visit request for a property
    ---
    tags:
      - Visits
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: path
        name: property_id
        type: integer
        required: true
        example: 1
      - in: header
        name: Authorization
        type: string
        required: true
        example: Bearer your_jwt_token
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - requester_id
            - requested_at
          properties:
            requester_id:
              type: integer
              example: 1
            requested_at:
              type: string
              example: "2026-04-10T14:00:00"
            message:
              type: string
              example: "Disponible l'après-midi"
    responses:
      201:
        description: Visit request created
      400:
        description: Invalid payload
      415:
        description: Content-Type must be application/json
    """
    try:
        data = _get_json()
        from app.services.visit_service import VisitService
        visit = VisitService.create(property_id, data)
        return jsonify(visit.to_dict()), 201
    except ApiError as e:
        return jsonify({"error": e.message}), e.status_code


@bp.route("/visit-requests/<int:visit_id>/status", methods=["PATCH"])
def update_visit_status(visit_id):
    """
    Update visit request status
    ---
    tags:
      - Visits
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: path
        name: visit_id
        type: integer
        required: true
        example: 1
      - in: header
        name: Authorization
        type: string
        required: true
        example: Bearer your_jwt_token
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - status
          properties:
            status:
              type: string
              enum:
                - pending
                - accepted
                - rejected
              example: accepted
    responses:
      200:
        description: Visit status updated
      400:
        description: Invalid payload
      404:
        description: Visit request not found
    """
    try:
        data = _get_json()
        from app.services.visit_service import VisitService
        visit = VisitService.update_status(visit_id, data)
        return jsonify(visit.to_dict()), 200
    except ApiError as e:
        return jsonify({"error": e.message}), e.status_code


@bp.route("/visit-requests/<int:visit_id>", methods=["GET"])
def get_visit_request(visit_id):
    """
    Get a visit request by ID
    ---
    tags:
      - Visits
    parameters:
      - in: path
        name: visit_id
        type: integer
        required: true
        example: 1
    responses:
      200:
        description: Visit request retrieved
      404:
        description: Visit request not found
    """
    try:
        from app.services.visit_service import VisitService
        visit = VisitService.get_by_id(visit_id)
        return jsonify(visit.to_dict()), 200
    except ApiError as e:
        return jsonify({"error": e.message}), e.status_code


@bp.route("/properties/<int:property_id>/visit-requests", methods=["GET"])
def list_visit_requests(property_id):
    """
    List all visit requests for a property
    ---
    tags:
      - Visits
    parameters:
      - in: path
        name: property_id
        type: integer
        required: true
        example: 1
    responses:
      200:
        description: Visit requests retrieved
    """
    try:
        from app.services.visit_service import VisitService
        visits = VisitService.get_by_property(property_id)
        return jsonify([v.to_dict() for v in visits]), 200
    except ApiError as e:
        return jsonify({"error": e.message}), e.status_code