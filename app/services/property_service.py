from datetime import datetime
from app.extensions import db
from app.models.property import Property
from app.models.room import Room
from app.models.user import User
from app.utils.audit import log_action
from app.utils.errors import ApiError


class PropertyService:
    @staticmethod
    def create(data):
        if not data:
            raise ApiError("invalid payload", 400)

        required_fields = ["name", "city", "type", "owner_id"]
        for field in required_fields:
            if data.get(field) in (None, ""):
                raise ApiError(f"{field} is required", 400)

        owner = User.query.get(data["owner_id"])
        if not owner:
            raise ApiError("owner not found", 404)

        prop = Property(
            name=data["name"],
            description=data.get("description"),
            city=data["city"],
            property_type=data["type"],
            owner_id=data["owner_id"],
            price=data.get("price"),
            surface=data.get("surface"),
            status=data.get("status", "draft"),
            archived=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.session.add(prop)
        db.session.commit()

        log_action(
            action="create_property",
            entity_type="property",
            entity_id=prop.id,
            actor_id=prop.owner_id,
            details=f"Property created in {prop.city}"
        )

        return prop

    @staticmethod
    def list_properties(city=None, property_type=None, min_price=None, max_price=None, search=None):
        query = Property.query.filter_by(archived=False)

        if city:
            query = query.filter(Property.city.ilike(city))
        if property_type:
            query = query.filter(Property.property_type.ilike(property_type))
        if min_price is not None:
            query = query.filter(Property.price >= min_price)
        if max_price is not None:
            query = query.filter(Property.price <= max_price)
        if search:
            like_value = f"%{search}%"
            query = query.filter(
                db.or_(
                    Property.name.ilike(like_value),
                    Property.description.ilike(like_value)
                )
            )

        return query.all()

    @staticmethod
    def get_by_id(property_id):
        prop = Property.query.get(property_id)
        if not prop:
            raise ApiError("property not found", 404)
        return prop

    @staticmethod
    def update(property_id, data):
        prop = Property.query.get(property_id)
        if not prop:
            raise ApiError("property not found", 404)

        mapping = {
            "name": "name",
            "description": "description",
            "city": "city",
            "type": "property_type",
            "price": "price",
            "surface": "surface",
            "status": "status",
            "archived": "archived",
        }

        for key, attr in mapping.items():
            if key in data:
                setattr(prop, attr, data[key])

        prop.updated_at = datetime.utcnow()
        db.session.commit()

        log_action(
            action="update_property",
            entity_type="property",
            entity_id=prop.id,
            actor_id=prop.owner_id,
            details="Property updated"
        )

        return prop

    @staticmethod
    def delete(property_id):
        prop = Property.query.get(property_id)
        if not prop:
            raise ApiError("property not found", 404)

        owner_id = prop.owner_id
        prop_id = prop.id

        db.session.delete(prop)
        db.session.commit()

        log_action(
            action="delete_property",
            entity_type="property",
            entity_id=prop_id,
            actor_id=owner_id,
            details="Property deleted"
        )

    @staticmethod
    def archive(property_id):
        prop = Property.query.get(property_id)
        if not prop:
            raise ApiError("property not found", 404)

        prop.archived = True
        prop.updated_at = datetime.utcnow()
        db.session.commit()

        log_action(
            action="archive_property",
            entity_type="property",
            entity_id=prop.id,
            actor_id=prop.owner_id,
            details="Property archived"
        )

        return prop

    @staticmethod
    def publish(property_id):
        prop = Property.query.get(property_id)
        if not prop:
            raise ApiError("property not found", 404)

        prop.status = "published"
        prop.updated_at = datetime.utcnow()
        db.session.commit()

        log_action(
            action="publish_property",
            entity_type="property",
            entity_id=prop.id,
            actor_id=prop.owner_id,
            details="Property published"
        )

        return prop

    @staticmethod
    def unpublish(property_id):
        prop = Property.query.get(property_id)
        if not prop:
            raise ApiError("property not found", 404)

        prop.status = "unpublished"
        prop.updated_at = datetime.utcnow()
        db.session.commit()

        log_action(
            action="unpublish_property",
            entity_type="property",
            entity_id=prop.id,
            actor_id=prop.owner_id,
            details="Property unpublished"
        )

        return prop

    @staticmethod
    def add_room(property_id, data):
        prop = Property.query.get(property_id)
        if not prop:
            raise ApiError("property not found", 404)

        if not data or not data.get("name"):
            raise ApiError("room name is required", 400)

        room = Room(
            property_id=property_id,
            name=data["name"],
            size=data.get("size"),
            features=data.get("features"),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.session.add(room)
        db.session.commit()

        log_action(
            action="add_room",
            entity_type="room",
            entity_id=room.id,
            actor_id=prop.owner_id,
            details=f"Room added to property {property_id}"
        )

        return room

    @staticmethod
    def update_room(property_id, room_id, data):
        room = Room.query.filter_by(id=room_id, property_id=property_id).first()
        if not room:
            raise ApiError("room not found", 404)

        if "name" in data:
            room.name = data["name"]
        if "size" in data:
            room.size = data["size"]
        if "features" in data:
            room.features = data["features"]

        room.updated_at = datetime.utcnow()
        db.session.commit()

        prop = Property.query.get(property_id)

        log_action(
            action="update_room",
            entity_type="room",
            entity_id=room.id,
            actor_id=prop.owner_id if prop else None,
            details=f"Room {room_id} updated"
        )

        return room

    @staticmethod
    def delete_room(property_id, room_id):
        room = Room.query.filter_by(id=room_id, property_id=property_id).first()
        if not room:
            raise ApiError("room not found", 404)

        prop = Property.query.get(property_id)
        room_entity_id = room.id

        db.session.delete(room)
        db.session.commit()

        log_action(
            action="delete_room",
            entity_type="room",
            entity_id=room_entity_id,
            actor_id=prop.owner_id if prop else None,
            details=f"Room {room_id} deleted"
        )