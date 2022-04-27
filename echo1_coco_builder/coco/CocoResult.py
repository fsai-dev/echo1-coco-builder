from marshmallow import Schema, fields


class CocoResultSchema(Schema):
    image_id = fields.Int()
    bbox = fields.List(fields.Int)
    score = fields.Float()
    category_id = fields.Int(required=True)
    category_name = fields.Str(required=True)
    segmentation = fields.List(fields.List(fields.Int))
    iscrowd = fields.Int()
    area = fields.Float()


class CocoResult:
    def __init__(self, kwargs):
        for attr in (
            "image_id",
            "bbox",
            "score",
            "category_id",
            "category_name",
            "segmentation",
            "iscrowd",
            "area",
        ):
            if attr in kwargs:
                setattr(self, attr, kwargs.get(attr))
