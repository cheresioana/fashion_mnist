import os

data = {
    "training_images": os.environ.get('TRAINING_IMAGES', "image_classifier/data/fashion/train-images-idx3-ubyte.gz"),
    "training_labels": os.environ.get('TRAINING_LABELS', "image_classifier/data/fashion/train-labels-idx1-ubyte.gz"),
    "test_images": os.environ.get('TEST_IMAGES', "image_classifier/data/fashion/t10k-images-idx3-ubyte.gz"),
    "test_labels": os.environ.get('TEST_LABELS', "image_classifier/data/fashion/t10k-labels-idx1-ubyte.gz"),
    "checkpoints": os.environ.get('CHECKPOINTS', "image_classifier/data/checkpoints")
}

gcp_project_id = "proj-258015"