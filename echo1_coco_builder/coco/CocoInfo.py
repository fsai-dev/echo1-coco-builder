from marshmallow import Schema, fields


class CocoInfoSchema(Schema):
    year = fields.Int()
    version = fields.Str()
    contributor = fields.Str()
    description = fields.Str()
    url = fields.Str()
    date_created = fields.Str()


class CocoInfo:
    def __init__(self, kwargs):
        for attr in (
            "year",
            "version",
            "contributor",
            "description",
            "url",
            "date_created",
        ):
            if attr in kwargs:
                setattr(self, attr, kwargs.get(attr))
