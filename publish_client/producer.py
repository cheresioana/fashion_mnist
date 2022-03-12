from image_classifier.utils.load_mnist import load_mnist
import sys

config = {
    "test_images": "data\\fashion\\t10k-images-idx3-ubyte.gz",
    "test_labels": "data\\fashion\\t10k-labels-idx1-ubyte.gz",
}


if __name__ == '__main__':
    client_id = int(sys.argv[1])
    x_valid, y_valid = load_mnist(config["test_images"], config["test_labels"])
    print(y_valid.shape)
    for idx in range(client_id * 2, client_id * 2 + 2):
        to_send_data = x_valid[idx]
        print("To send array of bytes that match the %d entry form the validation:"%idx)
