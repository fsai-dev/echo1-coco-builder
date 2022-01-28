from __future__ import annotations

from .coco.CocoAnnotation import CocoAnnotation, CocoAnnotationSchema
from .coco.CocoImage import CocoImage, CocoImageSchema
from .coco.CocoInfo import CocoInfo, CocoInfoSchema
from .coco.CocoCategory import CocoCategorySchema, CocoCategory
from marshmallow import Schema, fields


class CocoBuilderSchema(Schema):
    info = fields.Nested(CocoInfoSchema)
    images = fields.List(fields.Nested(CocoImageSchema))
    annotations = fields.List(fields.Nested(CocoAnnotationSchema))
    categories = fields.List(fields.Nested(CocoCategorySchema))


class CocoBuilder:
    def __init__(self):
        self.images = []
        self.categories = []
        self.info = {}
        self.annotations = []

    def add_annotation(self, data):
        # Validate data against the schema
        annotation = CocoAnnotation(data)
        schema = CocoAnnotationSchema()
        result = schema.dump(annotation)
        result = schema.load(result)
        self.annotations.append(result)

    def add_image(self, data):
        # Validate data against the schema
        image = CocoImage(data)
        schema = CocoImageSchema()
        result = schema.dump(image)
        result = schema.load(result)

        # Skip if the image has been added already
        for added_image in self.images:
            if added_image["id"] == image.id:
                return

        # Add to the images list if it does not exist
        self.images.append(result)

    def add_category(self, data):
        # Validate data against the schema
        category = CocoCategory(data)
        schema = CocoCategorySchema()
        result = schema.dump(category)
        result = schema.load(result)

        # Skip if the category has been added already
        for added_category in self.categories:
            if added_category["id"] == category.id:
                return

        # Add to the categories list if it does not exist
        self.categories.append(result)

    def add_info(self, data):
        # Validate data against the schema
        info = CocoInfo(data)
        schema = CocoInfoSchema()
        result = schema.dump(info)
        result = schema.load(result)
        # Add info to the object
        self.info = result

    def get(self):
        schema = CocoBuilderSchema()
        return schema.dumps(self)

    def __str__(self):
        return self.get()
