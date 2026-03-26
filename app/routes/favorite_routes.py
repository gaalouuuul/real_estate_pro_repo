from flask import Blueprint, jsonify

bp = Blueprint("favorites", __name__)

@bp.route("/properties/<int:property_id>/favorite", methods=["POST"])
def add_favorite(property_id):
    """
    Add property to favorites
    ---
    tags:
      - Favorites
    parameters:
      - in: path
        name: property_id
        schema:
          type: integer
        required: true
        example: 1
      - in: header
        name: Authorization
        schema:
          type: string
        required: true
        example: Bearer your_jwt_token
    responses:
      201:
        description: Favorite added
      401:
        description: Missing or invalid token
      409:
        description: Already favorite
    """
    return jsonify({"message": "favorite added"}), 201


@bp.route("/properties/<int:property_id>/favorite", methods=["DELETE"])
def remove_favorite(property_id):
    """
    Remove property from favorites
    ---
    tags:
      - Favorites
    parameters:
      - in: path
        name: property_id
        schema:
          type: integer
        required: true
        example: 1
      - in: header
        name: Authorization
        schema:
          type: string
        required: true
        example: Bearer your_jwt_token
    responses:
      200:
        description: Favorite removed
      404:
        description: Favorite not found
    """
    return jsonify({"message": "favorite removed"}), 200