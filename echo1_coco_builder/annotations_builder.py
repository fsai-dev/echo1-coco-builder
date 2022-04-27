from __future__ import annotations

from .coco.CocoAnnotation import CocoAnnotation, CocoAnnotationSchema
from .coco.CocoImage import CocoImage, CocoImageSchema
from .coco.CocoInfo import CocoInfo, CocoInfoSchema
from .coco.CocoCategory import CocoCategorySchema, CocoCategory
from marshmallow import Schema, fields
from loguru import logger


clamp = lambda n, minn, maxn: max(min(maxn, n), minn)


class CocoAnnotationsBuilderSchema(Schema):
    info = fields.Nested(CocoInfoSchema)
    images = fields.List(fields.Nested(CocoImageSchema))
    annotations = fields.List(fields.Nested(CocoAnnotationSchema))
    categories = fields.List(fields.Nested(CocoCategorySchema))


class CocoAnnotationsBuilder:
    def __init__(self):
        self.__annotations = {}
        self.__images = {}
        self.__categories = {}
        self.info = {}

    @property
    def annotations(self):
        annotations = []
        for idx, annotation in self.__annotations.items():
            annotations.append(annotation)

        return annotations

    def add_annotation(self, data):
        # Validate data against the schema
        annotation = CocoAnnotation(data)
        schema = CocoAnnotationSchema()
        result = schema.dump(annotation)
        result = schema.load(result)

        # If the annotation exists then skip
        if result["id"] in self.__annotations:
            logger.warning(
                "An annotation exists with the id {}. Skipping...".format(result["id"])
            )
            logger.warning(result)
            return

        # If the image if does not exists then skip
        if result["image_id"] not in self.__images:
            logger.error(
                "Unable to add annotation with the id {}. The image with the id {} does not exist.".format(
                    result["id"], result["image_id"]
                )
            )
            return

        # Access the image by image id
        image = self.__images[result["image_id"]]

        # Get the bounding box coordinates
        xmin, ymin, width, height = result.get("bbox")
        xmax = xmin + width
        ymax = ymin + height

        for x in [xmin, xmax]:
            if x > image.get("width"):
                logger.warning(
                    "Annotation {} has an xmin or xmax value greater than the image width. Automatically clamping the value.".format(
                        result["id"]
                    )
                )

        for y in [ymin, ymax]:
            if y > image.get("height"):
                logger.warning(
                    "Annotation {} has a ymin or max value greater than the image height. Automatically clamping the value.".format(
                        result["id"]
                    )
                )

        # Clamp the xmin, ymin, xmax, ymax values
        xmin = clamp(xmin, 0, image.get("width"))
        xmax = clamp(xmax, 0, image.get("width"))
        ymin = clamp(ymin, 0, image.get("height"))
        ymax = clamp(ymax, 0, image.get("height"))

        # Set the clamped width and height
        width = xmax - xmin
        height = ymax - ymin

        # Clamp the xmin, ymin, width, height values
        result["bbox"] = [xmin, ymin, width, height]

        # Append to the annotations
        self.__annotations[result["id"]] = result

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

    @property
    def categories(self):
        categories = []
        for idx, category in self.__categories.items():
            categories.append(category)

        return categories

    def add_category(self, data):
        # Validate data against the schema
        category = CocoCategory(data)
        schema = CocoCategorySchema()
        result = schema.dump(category)
        result = schema.load(result)

        # Add the category array to the object
        self.__categories[result["id"]] = result

    def add_info(self, data):
        # Validate data against the schema
        info = CocoInfo(data)
        schema = CocoInfoSchema()
        result = schema.dump(info)
        result = schema.load(result)
        # Add info to the object
        self.info = result

    def get(self):
        schema = CocoAnnotationsBuilderSchema()
        return schema.dumps(self)

    def __str__(self):
        return self.get()
