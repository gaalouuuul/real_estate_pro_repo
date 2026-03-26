from werkzeug.security import check_password_hash, generate_password_hash
from app.extensions import db
from app.models.user import User
from app.utils.audit import log_action
from app.utils.auth import issue_token
from app.utils.errors import ApiError


class AuthService:
    @staticmethod
    def register(data):
        if not data:
            raise ApiError("invalid payload", 400)

        required_fields = ["first_name", "last_name", "email", "password"]
        for field in required_fields:
            if data.get(field) in (None, ""):
                raise ApiError(f"{field} is required", 400)

        password = str(data["password"])

        if User.query.filter_by(email=data["email"]).first():
            raise ApiError("email already exists", 409)

        user = User(
            first_name=data["first_name"],
            last_name=data["last_name"],
            birth_date=data.get("birth_date"),
            email=data["email"],
            password_hash=generate_password_hash(password),
            role=data.get("role", "user"),
        )
        db.session.add(user)
        db.session.commit()

        log_action(
            action="register",
            entity_type="user",
            entity_id=user.id,
            actor_id=user.id,
            details=f"User {user.email} registered"
        )

        return user

    @staticmethod
    def login(data):
        if not data:
            raise ApiError("invalid payload", 400)

        email = data.get("email")
        password = str(data.get("password", ""))

        if not email or not password:
            raise ApiError("email and password are required", 400)

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password_hash, password):
            raise ApiError("invalid credentials", 401)

        log_action(
            action="login",
            entity_type="user",
            entity_id=user.id,
            actor_id=user.id,
            details=f"User {user.email} logged in"
        )

        return {
            "access_token": issue_token(user),
            "user": AuthService.serialize_user(user)
        }

    @staticmethod
    def serialize_user(user):
        return {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "birth_date": user.birth_date,
            "email": user.email,
            "role": user.role,
        }