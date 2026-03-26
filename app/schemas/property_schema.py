from marshmallow import Schema, fields, validate

PROPERTY_TYPES = ["house", "apartment", "studio", "villa", "loft", "office", "other"]
PROPERTY_STATUS = ["draft", "published", "unpublished"]


class PropertyCreateSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(load_default=None)
    city = fields.Str(required=True)
    type = fields.Str(required=True, validate=validate.OneOf(PROPERTY_TYPES))
    price = fields.Int(load_default=None)
    surface = fields.Int(load_default=None)
    status = fields.Str(load_default="draft", validate=validate.OneOf(PROPERTY_STATUS))


class PropertyUpdateSchema(Schema):
    name = fields.Str()
    description = fields.Str(allow_none=True)
    city = fields.Str()
    type = fields.Str(validate=validate.OneOf(PROPERTY_TYPES))
    price = fields.Int(allow_none=True)
    surface = fields.Int(allow_none=True)
    status = fields.Str(validate=validate.OneOf(PROPERTY_STATUS))


class RoomSchema(Schema):
    name = fields.Str(required=True)
    size = fields.Int(load_default=None)
    features = fields.Str(load_default=None)


class RoomUpdateSchema(Schema):
    name = fields.Str()
    size = fields.Int(allow_none=True)
    features = fields.Str(allow_none=True)


class VisitRequestSchema(Schema):
    requested_at = fields.Str(required=True)
    message = fields.Str(load_default=None)
