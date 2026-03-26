from flask import Blueprint, request, jsonify
from app.services.property_service import PropertyService

bp = Blueprint("properties", __name__)


@bp.route("/properties", methods=["POST"])
def create_property():
    """
    Create a property
    ---
    tags:
      - Properties
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
            - city
            - type
            - owner_id
          properties:
            name:
              type: string
              example: Appartement Paris
            description:
              type: string
              example: Bel appartement lumineux
            city:
              type: string
              example: Paris
            type:
              type: string
              example: apartment
            owner_id:
              type: integer
              example: 1
            price:
              type: integer
              example: 300000
            surface:
              type: integer
              example: 70
            status:
              type: string
              example: draft
    responses:
      201:
        description: Property created
    """
    data = request.get_json()
    prop = PropertyService.create(data)
    return jsonify(prop.to_dict()), 201


@bp.route("/properties", methods=["GET"])
def list_properties():
    """
    List properties
    ---
    tags:
      - Properties
    parameters:
      - in: query
        name: city
        required: false
        type: string
        example: Paris
      - in: query
        name: type
        required: false
        type: string
        example: apartment
      - in: query
        name: min_price
        required: false
        type: integer
        example: 100000
      - in: query
        name: max_price
        required: false
        type: integer
        example: 500000
      - in: query
        name: search
        required: false
        type: string
        example: lumineux
    responses:
      200:
        description: Properties retrieved
    """
    city = request.args.get("city")
    property_type = request.args.get("type")
    min_price = request.args.get("min_price", type=int)
    max_price = request.args.get("max_price", type=int)
    search = request.args.get("search")

    props = PropertyService.list_properties(
        city=city,
        property_type=property_type,
        min_price=min_price,
        max_price=max_price,
        search=search,
    )
    return jsonify([prop.to_dict() for prop in props]), 200


@bp.route("/properties/<int:property_id>", methods=["GET"])
def get_property(property_id):
    """
    Get property by id
    ---
    tags:
      - Properties
    parameters:
      - in: path
        name: property_id
        required: true
        type: integer
    responses:
      200:
        description: Property found
      404:
        description: Property not found
    """
    prop = PropertyService.get_by_id(property_id)
    return jsonify(prop.to_dict()), 200


@bp.route("/properties/<int:property_id>", methods=["PUT"])
def update_property(property_id):
    """
    Update a property
    ---
    tags:
      - Properties
    consumes:
      - application/json
    parameters:
      - in: path
        name: property_id
        required: true
        type: integer
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            description:
              type: string
            city:
              type: string
            type:
              type: string
            price:
              type: integer
            surface:
              type: integer
            status:
              type: string
    responses:
      200:
        description: Property updated
    """
    data = request.get_json()
    prop = PropertyService.update(property_id, data)
    return jsonify(prop.to_dict()), 200


@bp.route("/properties/<int:property_id>", methods=["DELETE"])
def delete_property(property_id):
    """
    Delete a property
    ---
    tags:
      - Properties
    parameters:
      - in: path
        name: property_id
        required: true
        type: integer
    responses:
      200:
        description: Property deleted
    """
    PropertyService.delete(property_id)
    return jsonify({"message": "Property deleted"}), 200


@bp.route("/properties/<int:property_id>/archive", methods=["PATCH"])
def archive_property(property_id):
    """
    Archive a property
    ---
    tags:
      - Properties
    parameters:
      - in: path
        name: property_id
        required: true
        type: integer
    responses:
      200:
        description: Property archived
    """
    prop = PropertyService.archive(property_id)
    return jsonify(prop.to_dict()), 200


@bp.route("/properties/<int:property_id>/publish", methods=["PATCH"])
def publish_property(property_id):
    """
    Publish a property
    ---
    tags:
      - Properties
    parameters:
      - in: path
        name: property_id
        required: true
        type: integer
    responses:
      200:
        description: Property published
    """
    prop = PropertyService.publish(property_id)
    return jsonify(prop.to_dict()), 200


@bp.route("/properties/<int:property_id>/unpublish", methods=["PATCH"])
def unpublish_property(property_id):
    """
    Unpublish a property
    ---
    tags:
      - Properties
    parameters:
      - in: path
        name: property_id
        required: true
        type: integer
    responses:
      200:
        description: Property unpublished
    """
    prop = PropertyService.unpublish(property_id)
    return jsonify(prop.to_dict()), 200


@bp.route("/properties/<int:property_id>/rooms", methods=["POST"])
def add_room(property_id):
    """
    Add a room to a property
    ---
    tags:
      - Rooms
    consumes:
      - application/json
    parameters:
      - in: path
        name: property_id
        required: true
        type: integer
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
          properties:
            name:
              type: string
              example: Chambre 1
            size:
              type: integer
              example: 14
            features:
              type: string
              example: placard, fenêtre
    responses:
      201:
        description: Room added
    """
    data = request.get_json()
    room = PropertyService.add_room(property_id, data)
    return jsonify(room.to_dict()), 201


@bp.route("/properties/<int:property_id>/rooms/<int:room_id>", methods=["PUT"])
def update_room(property_id, room_id):
    """
    Update a room
    ---
    tags:
      - Rooms
    consumes:
      - application/json
    parameters:
      - in: path
        name: property_id
        required: true
        type: integer
      - in: path
        name: room_id
        required: true
        type: integer
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            size:
              type: integer
            features:
              type: string
    responses:
      200:
        description: Room updated
    """
    data = request.get_json()
    room = PropertyService.update_room(property_id, room_id, data)
    return jsonify(room.to_dict()), 200


@bp.route("/properties/<int:property_id>/rooms/<int:room_id>", methods=["DELETE"])
def delete_room(property_id, room_id):
    """
    Delete a room
    ---
    tags:
      - Rooms
    parameters:
      - in: path
        name: property_id
        required: true
        type: integer
      - in: path
        name: room_id
        required: true
        type: integer
    responses:
      200:
        description: Room deleted
    """
    PropertyService.delete_room(property_id, room_id)
    return jsonify({"message": "Room deleted"}), 200