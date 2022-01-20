from echo1_coco_builder import __version__
from echo1_coco_builder import __version__
from echo1_coco_builder.echo1_coco_builder import CocoBuilder
import pandas as pd, re


def string_to_list_int(a_string, sep=","):
    return a_string.split(sep)


def test_builder():

    # Open a CSV using pandas
    df = pd.read_csv("test.csv")

    # Initialize the coco generator
    coco_builder = CocoBuilder()

    # For each row in the csv
    for annotation_id, row in df.iterrows():

        # image_id must be an integer
        image_id = int(re.sub("[^0-9]", "", row["image_name"]))

        # image_name must be a string
        image_name = row["image_name"]

        # image_width and image_height must be an integer
        image_width = row["image_width"]
        image_height = row["image_height"]

        # category_id must be an integer
        category_id = row["category_id"]

        # category_name must be a string
        category_name = row["category_name"]

        # bbox format: [x,y,width,height]
        bbox = string_to_list_int(row["bbox"])

        # add a new image
        coco_builder.add_image(image_id, image_name, image_width, image_height)

        # add a new category
        coco_builder.add_category(category_id, category_name)

        # add a new annotation
        coco_builder.add_annotation(
            annotation_id, image_id, category_id, bbox, [], 0, 0
        )

    # add info
    coco_builder.add_info(2022, "v1.0", "Echo1")

    # images assertion
    assert len(coco_builder.images) == 2
    for image in coco_builder.images:
        assert type(image["id"]) is int
        assert type(image["image_name"]) is str
        assert type(image["height"]) is int
        assert type(image["width"]) is int

    # annotations assertion
    assert len(coco_builder.annotations) == 5
    for annotation in coco_builder.annotations:
        assert type(annotation["id"]) is int
        assert type(annotation["image_id"]) is int
        assert type(annotation["iscrowd"]) is int
        assert type(annotation["area"]) is float
        assert len(annotation["segmentation"]) == 0

    # categories assertion
    for category in coco_builder.categories:
        assert type(category["id"]) is int
        assert type(category["name"]) is str

    # info assertion
    assert coco_builder.info["version"] == "v1.0"
    assert coco_builder.info["year"] == 2022
    assert coco_builder.info["contributor"] == "Echo1"
