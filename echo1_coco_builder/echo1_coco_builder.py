from __future__ import annotations

from .coco.CocoAnnotation import CocoAnnotation, CocoAnnotationSchema
from .coco.CocoImage import CocoImage, CocoImageSchema
from .coco.CocoInfo import CocoInfo, CocoInfoSchema
from .coco.CocoCategory import CocoCategorySchema, CocoCategory
from marshmallow import Schema, fields


clamp = lambda n, minn, maxn: max(min(maxn, n), minn)


class CocoBuilderSchema(Schema):
    info = fields.Nested(CocoInfoSchema)
    images = fields.List(fields.Nested(CocoImageSchema))
    annotations = fields.List(fields.Nested(CocoAnnotationSchema))
    categories = fields.List(fields.Nested(CocoCategorySchema))


class CocoBuilder:
    def __init__(self):
        self.__images = {}
        self.categories = []
        self.info = {}
        self.annotations = []

    def add_annotation(self, data):
        # Validate data against the schema
        annotation = CocoAnnotation(data)
        schema = CocoAnnotationSchema()
        result = schema.dump(annotation)
        result = schema.load(result)
        image = self.__images[result["image_id"]]

        # Get the bounding box coordinates
        xmin, ymin, width, height = result.get("bbox")

        # Clamp the xmin, ymin, xmax, ymax values
        xmin = clamp(xmin, 0, image.get("width"))
        ymin = clamp(ymin, 0, image.get("height"))
        xmax = clamp(xmin + width, 0, image.get("width"))
        ymax = clamp(ymin + height, 0, image.get("height"))

        # Set the clamped width and height
        width = xmax - xmin
        height = ymax - ymin

        # Clamp the xmin, ymin, width, height values
        result["bbox"] = [xmin, ymin, width, height]

        # Append to the annotations
        self.annotations.append(result)

    @property
    def images(self):
        images = []
        for idx, image in self.__images.items():
            images.append(image)

        return images

    def add_image(self, data):
        # Validate data against the schema
        image = CocoImage(data)
        schema = CocoImageSchema()
        result = schema.dump(image)
        result = schema.load(result)

        # Add the image array to the object
        self.__images[result["id"]] = result

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
