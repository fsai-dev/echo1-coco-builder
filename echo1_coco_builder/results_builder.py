import json
from .coco.CocoResult import CocoResultSchema, CocoResult
from marshmallow import Schema, fields


class CocoResultsBuilderSchema(Schema):
    results = fields.List(fields.Nested(CocoResultSchema))


class CocoResultsBuilder:
    def __init__(self):
        self.__results = []

    def add_result(self, data):
        # Validate data against the schema
        category = CocoResult(data)
        schema = CocoResultSchema()
        result = schema.dump(category)
        result = schema.load(result)

        # Add the category array to the object
        self.__results.append(result)

    @property
    def results(self):
        return self.__results

    def get(self):
        schema = CocoResultsBuilderSchema()
        return json.dumps(self.results)

    def __str__(self):
        return self.get()
