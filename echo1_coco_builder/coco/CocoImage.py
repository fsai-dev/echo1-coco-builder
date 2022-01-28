from marshmallow import Schema, fields


class CocoImageSchema(Schema):
    id = fields.Int(required=True)
    file_name = fields.Str(required=True)
    width = fields.Int(required=True)
    height = fields.Int(required=True)
    license = fields.Str()
    flickr_url = fields.Str()
    coco_url = fields.Str()
    date_captured = fields.Str()


class CocoImage:
    def __init__(self, kwargs):
        for attr in (
            "id",
            "file_name",
            "width",
            "height",
            "license",
            "flickr_url",
            "coco_url",
            "date_created",
        ):
            if attr in kwargs:
                setattr(self, attr, kwargs.get(attr))
