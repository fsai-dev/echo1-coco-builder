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

## Example use
```python
import pandas as pd
from echo1_coco_builder.echo1_coco_builder import CocoBuilder

# Open a CSV using pandas
df = pd.read_csv("test.csv")

# Initialize the coco builder
coco_builder = CocoBuilder()

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
    coco_builder.add_image(image_id, file_name, image_width, image_height)

    # add a new category
    coco_builder.add_category(category_id, category_name)

    # add a new annotation
    coco_builder.add_annotation(annotation_id, image_id, category_id, bbox, [], 0, 0)

# add info
coco_builder.add_info(2022, "v1.0", "Echo1", "", "https://echo1.io")

# print the data in the coco format as a python object
print(coco_builder)

# print the data in the coco format as json
print(coco_builder.get())

# save the data in the coco format as json
python_file = open("example-data.json", "w")
python_file.write(coco_builder.get())
python_file.close()
```