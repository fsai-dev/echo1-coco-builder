from marshmallow import Schema, fields


class CocoAnnotationSchema(Schema):
    id = fields.Int(required=True)
    image_id = fields.Int(required=True)
    category_id = fields.Int(required=True)
    bbox = fields.List(fields.Int)
    segmentation = fields.List(fields.List(fields.Int))
    iscrowd = fields.Int()
    area = fields.Float()


class CocoAnnotation:
    def __init__(self, kwargs):
        for attr in (
            "id",
            "image_id",
            "category_id",
            "bbox",
            "segmentation",
            "iscrowd",
            "area",
        ):
            if attr in kwargs:
                setattr(self, attr, kwargs.get(attr))
