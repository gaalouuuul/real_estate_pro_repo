from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService
from app.utils.errors import ApiError

bp = Blueprint("auth", __name__)


@bp.route("/auth/register", methods=["POST"])
def register():
    """
    Register a new user
    ---
    tags:
      - Auth
    consumes:
      - application/json
    produces:
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
              example: "Ahmed"
            last_name:
              type: string
              example: "Gaaloul"
            birth_date:
              type: string
              example: "2000-01-01"
            email:
              type: string
              example: "ahmed@test.com"
            password:
              type: string
              example: "secret123"
            role:
              type: string
              enum: [user, owner, admin]
              example: "user"
    responses:
      201:
        description: User successfully registered
      400:
        description: Invalid payload
      409:
        description: Email already in use
    """
    try:
        data = request.get_json(silent=True)
        if not data:
            raise ApiError("Content-Type must be application/json", 415)
        user = AuthService.register(data)
        return jsonify(AuthService.serialize_user(user)), 201
    except ApiError as e:
        return jsonify({"error": e.message}), e.status_code


@bp.route("/auth/login", methods=["POST"])
def login():
    """
    Login user
    ---
    tags:
      - Auth
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
              example: "ahmed@test.com"
            password:
              type: string
              example: "secret123"
    responses:
      200:
        description: Login successful
      401:
        description: Invalid credentials
    """
    try:
        data = request.get_json(silent=True)
        if not data:
            raise ApiError("Content-Type must be application/json", 415)
        return jsonify(AuthService.login(data)), 200
    except ApiError as e:
        return jsonify({"error": e.message}), e.status_code