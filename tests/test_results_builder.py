from echo1_coco_builder.results_builder import CocoResultsBuilder


def test_results_builder():
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

    isinstance(results_builder.get(), str)
    isinstance(results_builder.results, list)

    for result in results_builder.results:
        assert isinstance(result["image_id"], int)
        assert isinstance(result["bbox"], list)
        assert isinstance(result["score"], float)
        assert isinstance(result["category_id"], int)
        assert isinstance(result["category_name"], str)
        assert len(result["segmentation"]) == 0
        assert isinstance(result["iscrowd"], int)
        assert isinstance(result["area"], float)
