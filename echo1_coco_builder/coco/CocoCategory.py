from marshmallow import Schema, fields


class CocoCategorySchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    supercategory = fields.Str()


class CocoCategory:
    def __init__(self, kwargs):
        for attr in (
            "id",
            "name",
            "supercategory",
        ):
            if attr in kwargs:
                setattr(self, attr, kwargs.get(attr))
