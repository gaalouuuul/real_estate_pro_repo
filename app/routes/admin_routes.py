from flask import Blueprint, jsonify, request
from app.services.admin_service import AdminService

bp = Blueprint("admin", __name__)

@bp.route("/stats/properties", methods=["GET"])
def property_stats():
    """
    Get property statistics
    ---
    tags:
      - Admin
    responses:
      200:
        description: Property statistics retrieved
    """
    return jsonify(AdminService.property_stats()), 200


@bp.route("/audit-logs", methods=["GET"])
def audit_logs():
    """
    Get audit logs
    ---
    tags:
      - Admin
    parameters:
      - in: query
        name: limit
        required: false
        type: integer
        example: 50
    responses:
      200:
        description: Audit logs retrieved
    """
    limit = request.args.get("limit", default=100, type=int)
    return jsonify(AdminService.audit_logs(limit=limit)), 200


@bp.route("/health", methods=["GET"])
def health():
    """
    Health check
    ---
    tags:
      - Health
    responses:
      200:
        description: API is healthy
    """
    return jsonify({"status": "ok"}), 200