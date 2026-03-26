from app.utils.errors import ApiError


def require_fields(payload, required_fields):
    if not isinstance(payload, dict):
        raise ApiError("invalid json payload", 400)
    for field in required_fields:
        if payload.get(field) in (None, ""):
            raise ApiError(f"{field} is required", 400)
    return payload
