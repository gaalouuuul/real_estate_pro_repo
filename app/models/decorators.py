from functools import wraps
from flask import request, jsonify
from app.utils.jwt_utils import decode_token

def jwt_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization")
        if not auth or not auth.startswith("Bearer "):
            return jsonify({"error": "missing token"}), 401
        token = auth.split(" ")[1]
        try:
            request.current_user = decode_token(token)
        except Exception:
            return jsonify({"error": "invalid token"}), 401
        return f(*args, **kwargs)
    return wrapper

def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user = getattr(request, "current_user", None)
            if not user or user["role"] not in roles:
                return jsonify({"error": "forbidden"}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator