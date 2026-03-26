from marshmallow import Schema, fields, validate


class RegisterSchema(Schema):
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    birth_date = fields.Str(load_default=None)
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))
    role = fields.Str(load_default="user", validate=validate.OneOf(["user", "owner", "admin"]))


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class UpdateUserSchema(Schema):
    first_name = fields.Str()
    last_name = fields.Str()
    birth_date = fields.Str(allow_none=True)
