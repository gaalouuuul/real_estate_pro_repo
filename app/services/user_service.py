from app.extensions import db
from app.models.user import User
from app.models.property import Property
from app.models.favorite import Favorite
from app.models.visit_request import VisitRequest
from app.utils.errors import ApiError
import bcrypt


class UserService:

    @staticmethod
    def create(data):
        if not data:
            raise ApiError("invalid payload", 400)

        # Champs obligatoires
        required_fields = ["first_name", "last_name", "email", "password"]
        for field in required_fields:
            if data.get(field) in (None, ""):
                raise ApiError(f"{field} is required", 400)

        # Vérification email unique
        if User.query.filter_by(email=data["email"].lower()).first():
            raise ApiError("email already in use", 409)

        # Hash du mot de passe (ne jamais stocker en clair)
        password_hash = bcrypt.hashpw(
            data["password"].encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

        user = User(
            first_name    = data["first_name"],
            last_name     = data["last_name"],
            birth_date    = data.get("birth_date"),
            email         = data["email"].lower(),
            password_hash = password_hash,
            role          = data.get("role", "user"),
        )

        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get_by_id(user_id):
        user = User.query.get(user_id)
        if not user:
            raise ApiError("user not found", 404)
        return user

    @staticmethod
    def update(user_id, data):
        if not data:
            raise ApiError("invalid payload", 400)

        user = User.query.get(user_id)
        if not user:
            raise ApiError("user not found", 404)

        if "first_name" in data:
            if data["first_name"] in (None, ""):
                raise ApiError("first_name cannot be empty", 400)
            user.first_name = data["first_name"]

        if "last_name" in data:
            if data["last_name"] in (None, ""):
                raise ApiError("last_name cannot be empty", 400)
            user.last_name = data["last_name"]

        if "birth_date" in data:
            user.birth_date = data["birth_date"]

        # Vérifier que le nouvel email n'est pas déjà pris par quelqu'un d'autre
        if "email" in data:
            if data["email"] in (None, ""):
                raise ApiError("email cannot be empty", 400)
            existing = User.query.filter_by(email=data["email"].lower()).first()
            if existing and existing.id != user_id:
                raise ApiError("email already in use", 409)
            user.email = data["email"].lower()

        # Mise à jour du mot de passe si fourni
        if "password" in data and data["password"]:
            user.password_hash = bcrypt.hashpw(
                data["password"].encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")

        db.session.commit()
        return user

    @staticmethod
    def get_user_properties(user_id, include_archived="false"):
        # Vérifier que l'utilisateur existe
        if not User.query.get(user_id):
            raise ApiError("user not found", 404)

        query = Property.query.filter_by(owner_id=user_id)
        if include_archived != "true":
            query = query.filter_by(archived=False)
        return query.all()

    @staticmethod
    def get_user_favorites(user_id):
        if not User.query.get(user_id):
            raise ApiError("user not found", 404)
        return Favorite.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_user_visit_requests(user_id):
        if not User.query.get(user_id):
            raise ApiError("user not found", 404)
        return VisitRequest.query.filter_by(requester_id=user_id).all()