def load_mnist(image_path, labels_path, kind='train'):
    import os
    import gzip
    import numpy as np

    labels_path = os.path.join(os.getcwd(), labels_path)
    image_path = os.path.join(os.getcwd(), image_path)
    with gzip.open(labels_path, 'rb') as lbpath:
        labels = np.frombuffer(lbpath.read(), dtype=np.uint8,
                               offset=8)

    with gzip.open(image_path, 'rb') as imgpath:
        images = np.frombuffer(imgpath.read(), dtype=np.uint8,
                               offset=16).reshape(len(labels), 784)

    return images, labels