from flask import Blueprint, request, jsonify
from app.services.user_service import UserService
from app.utils.errors import ApiError

bp = Blueprint("users", __name__)


def handle_error(e):
    """Convertit une ApiError en réponse JSON propre."""
    if isinstance(e, ApiError):
        return jsonify({"error": e.message}), e.status_code
    return jsonify({"error": "internal server error"}), 500


@bp.route("/users", methods=["POST"])
def create_user():
    """
    Create a user
    ---
    tags:
      - Users
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - first_name
            - last_name
            - email
            - password
          properties:
            first_name:
              type: string
              example: Ahmed
            last_name:
              type: string
              example: Gaaloul
            birth_date:
              type: string
              example: "2000-01-01"
            email:
              type: string
              example: ahmed@test.com
            password:
              type: string
              example: "secret123"
            role:
              type: string
              example: owner
    responses:
      201:
        description: User created
      400:
        description: Invalid payload
      409:
        description: Email already in use
    """
    try:
        data = request.get_json(silent=True)
        user = UserService.create(data)
        return jsonify(user.to_dict()), 201
    except ApiError as e:
        return handle_error(e)


@bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    """
    Get user by ID
    ---
    tags:
      - Users
    parameters:
      - in: path
        name: user_id
        required: true
        schema:
          type: integer
    responses:
      200:
        description: User retrieved
      404:
        description: User not found
    """
    try:
        user = UserService.get_by_id(user_id)
        return jsonify(user.to_dict()), 200
    except ApiError as e:
        return handle_error(e)


@bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    """
    Update user information
    ---
    tags:
      - Users
    parameters:
      - in: path
        name: user_id
        required: true
        schema:
          type: integer
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            first_name:
              type: string
              example: Ahmed Updated
            last_name:
              type: string
              example: Gaaloul
            birth_date:
              type: string
              example: "2000-01-01"
            email:
              type: string
              example: ahmed.updated@example.com
            password:
              type: string
              example: "newpassword123"
    responses:
      200:
        description: User updated
      400:
        description: Invalid payload
      404:
        description: User not found
      409:
        description: Email already in use
    """
    try:
        data = request.get_json(silent=True)
        user = UserService.update(user_id, data)
        return jsonify(user.to_dict()), 200
    except ApiError as e:
        return handle_error(e)


@bp.route("/users/<int:user_id>/properties", methods=["GET"])
def get_user_properties(user_id):
    """
    Get properties of a user
    ---
    tags:
      - Users
    parameters:
      - in: path
        name: user_id
        required: true
        schema:
          type: integer
      - in: query
        name: include_archived
        required: false
        schema:
          type: boolean
        example: false
    responses:
      200:
        description: User properties retrieved
      404:
        description: User not found
    """
    try:
        include_archived = request.args.get("include_archived", "false")
        properties = UserService.get_user_properties(user_id, include_archived)
        return jsonify([p.to_dict() for p in properties]), 200
    except ApiError as e:
        return handle_error(e)


@bp.route("/users/<int:user_id>/favorites", methods=["GET"])
def get_user_favorites(user_id):
    """
    Get user's favorite properties
    ---
    tags:
      - Users
    parameters:
      - in: path
        name: user_id
        required: true
        schema:
          type: integer
    responses:
      200:
        description: Favorite properties retrieved
      404:
        description: User not found
    """
    try:
        favorites = UserService.get_user_favorites(user_id)
        return jsonify([f.to_dict() for f in favorites]), 200
    except ApiError as e:
        return handle_error(e)


@bp.route("/users/<int:user_id>/visit-requests", methods=["GET"])
def get_user_visit_requests(user_id):
    """
    Get user's visit requests
    ---
    tags:
      - Users
    parameters:
      - in: path
        name: user_id
        required: true
        schema:
          type: integer
    responses:
      200:
        description: Visit requests retrieved
      404:
        description: User not found
    """
    try:
        visits = UserService.get_user_visit_requests(user_id)
        return jsonify([v.to_dict() for v in visits]), 200
    except ApiError as e:
        return handle_error(e)