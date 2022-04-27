## Introduction

`echo1-coco-builder` provides a faster, safer way to build coco formatted data.

See: https://cocodataset.org/#format-data for more information

## Installation

```shell
# If using pip
pip install echo1-coco-builder

# If using poetry
poetry add echo1-coco-builder
```

## Example use (building coco annotations)

```python
import pandas as pd
from echo1_coco_builder.annotations_builder import CocoAnnotationsBuilder

# Open a CSV using pandas
df = pd.read_csv("./tests/data/test.csv")

# Initialize the coco builder
coco_builder = CocoAnnotationsBuilder()

# For each row in the csv
for annotation_id, row in df.iterrows():

    # image_id must be an integer
    image_id = row["image_name"]

    # image_name must be a string
    file_name = row["image_name"]

    # image_width and image_height must be an integer
    image_width = row["image_width"]
    image_height = row["image_height"]

    # category_id must be an integer
    category_id = row["category_id"]

    # category_name must be a string
    category_name = row["category_name"]

    # bbox format: [x,y,width,height]
    bbox = row["bbox"].split(",")

    # add a new image
    coco_builder.add_image(
        {
            "id": image_id,
            "file_name": file_name,
            "width": image_width,
            "height": image_height,
        }
    )

    # add a new category
    coco_builder.add_category({"id": category_id, "name": category_name})

    # add a new annotation
    coco_builder.add_annotation(
        {
            "id": annotation_id,
            "image_id": image_id,
            "category_id": category_id,
            "bbox": bbox,
            "segmentation": segmentation,
            "iscrowd": 0,
            "area": area,
        }
    )

# add info
coco_builder.add_info(
    {
        "year": 2022,
        "version": "v1.0",
        "contributor": "Echo1",
        "description": "Contact for more info.",
        "url": "https://echo1.io",
    }
)

# print the data in the coco format as a python object
print(coco_builder)

# print the data in the coco format as json
print(coco_builder.get())

# save the data in the coco format as json
python_file = open("example-data.json", "w")
python_file.write(coco_builder.get())
python_file.close()
```


## Example use (building coco results)

```python
from echo1_coco_builder.results_builder import CocoResultsBuilder


# Initialize the coco generator
results_builder = CocoResultsBuilder()
results_builder.add_result(
    {
        "image_id": 1,
        "bbox": [490, 365, 14, 26],
        "score": 0.8559583425521851,
        "category_id": 1,
        "category_name": "My Category",
        "segmentation": [],
        "iscrowd": 0,
        "area": 364,
    }
)

# print the data in the coco results format as a python object
print(results_builder)

# print the data in the coco results format as json
print(results_builder.get())
```