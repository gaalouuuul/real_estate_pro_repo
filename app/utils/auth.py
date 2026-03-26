import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, current_app
from app.models import Property
from app.utils.errors import ApiError


def issue_token(user) -> str:
    """Génère un vrai JWT signé avec SECRET_KEY, expire dans 24h."""
    payload = {
        "sub":  user.id,
        "role": user.role,
        "iat":  datetime.utcnow(),
        "exp":  datetime.utcnow() + timedelta(hours=24),
    }
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")


def _decode_token(token: str) -> dict:
    """Décode et valide le JWT. Lève ApiError si invalide ou expiré."""
    try:
        return jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise ApiError("token expired", 401)
    except jwt.InvalidTokenError:
        raise ApiError("invalid token", 401)


def require_auth(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise ApiError("unauthorized — missing token", 401)
        token = auth_header[7:]
        request.user_ctx = _decode_token(token)
        return fn(*args, **kwargs)
    return wrapper


def current_user_id() -> int:
    return int(request.user_ctx["sub"])


def current_user_role() -> str:
    return str(request.user_ctx["role"])


def require_roles(*roles):
    def decorator(fn):
        @wraps(fn)
        @require_auth
        def wrapper(*args, **kwargs):
            if current_user_role() not in roles:
                raise ApiError("forbidden", 403)
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def require_property_owner_or_admin(property_id_arg: str = "property_id"):
    def decorator(fn):
        @wraps(fn)
        @require_auth
        def wrapper(*args, **kwargs):
            prop = Property.query.get_or_404(kwargs[property_id_arg])
            if current_user_role() != "admin" and prop.owner_id != current_user_id():
                raise ApiError("forbidden", 403)
            return fn(*args, **kwargs)
        return wrapper
    return decorator