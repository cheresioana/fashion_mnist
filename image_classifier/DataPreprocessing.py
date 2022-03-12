import math

from keras.utils.np_utils import to_categorical
from matplotlib import pyplot
from image_classifier.utils.load_mnist import load_mnist
import numpy as np

class DataPreprocessing:

    def __init__(self, train_img_path, train_labels_path, test_img_path, test_label_path):
        #load the test data
        self.test_datax, self.test_datay = load_mnist(test_img_path, test_label_path)
        #load the train data
        self.train_datax, self.train_datay = load_mnist(train_img_path, train_labels_path)
        #find image size assuming it is square
        self.img_size = int(math.sqrt(self.train_datax[0].size))
        if self.img_size * self.img_size != self.train_datax[0].size:
            raise Exception("The width is not equal with the height")

    def visualize_data(self):
        print('Train: X=%s, y=%s' % (self.train_datax.shape, self.train_datay.shape))
        print('Test: X=%s, y=%s' % (self.test_datax.shape, self.test_datay.shape))
        print('Possible labels: %s'% np.unique(self.train_datay))
        for i in range(9):
            # define subplot
            ax = pyplot.subplot(330 + 1 + i)
            # plot raw pixel data
            ax.title.set_text(self.train_datay[i])
            pyplot.imshow(self.train_datax[i].reshape(self.img_size, self.img_size), cmap=pyplot.get_cmap('gray'))
        # show the figure
        pyplot.show()

    def normalize_data(self):
        self.train_datax_norm = self.train_datax.astype('float32')
        self.test_datax_norm = self.test_datax.astype('float32')
        #normalize in range 0-1
        self.train_datax_norm = self.train_datax_norm / 255.0
        self.test_datax_norm = self.test_datax_norm / 255.0

    def rearange_data(self):
        self.train_datax_norm = self.train_datax_norm.reshape(self.train_datay.shape[0] ,self.img_size, self.img_size, 1)
        self.test_datax_norm = self.test_datax_norm.reshape(self.test_datay.shape[0], self.img_size, self.img_size, 1)

    def encode_labels(self):
        #one hot encoding
        self.train_datay_enc = to_categorical(self.train_datay)
        self.test_datay_enc = to_categorical(self.test_datay)

    def process_data(self):
        self.normalize_data()
        self.encode_labels()
        self.rearange_data()
        return self.train_datax_norm, self.train_datay_enc, self.test_datax_norm, self.test_datay_enc
