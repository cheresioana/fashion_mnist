from keras import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from keras.optimizer_v1 import SGD
import tensorflow as tf


class CNNModel():
    def __init__(self):
        self.model = self.define_model()


    def fit(self):
        self.model.fit

