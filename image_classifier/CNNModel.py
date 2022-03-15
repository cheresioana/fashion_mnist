import glob

import numpy as np
from keras import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from keras.optimizer_v1 import SGD
import tensorflow as tf
from matplotlib import pyplot
from numpy import mean, std
from sklearn.model_selection import KFold


class CNNModel():
    def __init__(self, checkpoints):
        self.model = None
        self.checkpoints = checkpoints + "/cp.ckpt"
        self.checkpoints_dir = checkpoints

    def define_model(self):
        tf.compat.v1.disable_eager_execution()
        model = Sequential()
        model.add(Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_uniform', input_shape=(28, 28, 1)))
        model.add(MaxPooling2D((2, 2)))
        model.add(Flatten())
        model.add(Dense(100, activation='relu', kernel_initializer='he_uniform'))
        model.add(Dense(10, activation='softmax'))
        # compile model
        opt = SGD(lr=0.01, momentum=0.9)
        model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])
        return model

    def load_model(self):
        self.model = self.define_model()
        checkpoints = glob.glob(self.checkpoints_dir + '/*ckpt*')
        if not checkpoints:
            return None
        self.model.load_weights(self.checkpoints)
        return self.model

    # evaluate the model with 5 (or more) folds
    def train_evaluate_model(self, dataX, dataY, n_folds=5):
        scores, histories = list(), list()
        # prepare cross validation
        kfold = KFold(n_folds, shuffle=True, random_state=1)
        # enumerate splits

        cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=self.checkpoints,
                                                         save_weights_only=True,
                                                         verbose=1)

        for train_ix, test_ix in kfold.split(dataX):
            # define model
            model = self.define_model()
            # select rows for train and validation
            trainX, trainY, validationX, validationY = dataX[train_ix], dataY[train_ix], dataX[test_ix], dataY[test_ix]
            # fit model
            history = model.fit(trainX, trainY, epochs=10, batch_size=32, validation_data=(validationX, validationY),
                                verbose=0, callbacks=[cp_callback])
            # evaluate model
            _, acc = model.evaluate(validationX, validationY, verbose=0)
            print('> %.3f' % (acc * 100.0))
            # append scores
            scores.append(acc)
            histories.append(history)
        self.model = model
        return scores, histories

    # plot diagnostic learning curves
    def summarize_diagnostics(self, histories):
        for i in range(len(histories)):
            # plot loss
            pyplot.subplot(211)
            pyplot.title('Cross Entropy Loss')
            pyplot.plot(histories[i].history['loss'], color='blue', label='train')
            pyplot.plot(histories[i].history['val_loss'], color='orange', label='test')
            # plot accuracy
            pyplot.subplot(212)
            pyplot.title('Classification Accuracy')
            pyplot.plot(histories[i].history['accuracy'], color='blue', label='train')
            pyplot.plot(histories[i].history['val_accuracy'], color='orange', label='test')
        pyplot.show()

    def summarize_performance(self, scores):
        # print summary
        print('Accuracy: mean=%.3f std=%.3f, n=%d' % (mean(scores) * 100, std(scores) * 100, len(scores)))
        # box and whisker plots of results
        pyplot.boxplot(scores)
        pyplot.show()

    def evaluate_performance(self, test_x, test_y):
        _, acc = self.model.evaluate(test_x, test_y, verbose=0)
        return acc

    def predict(self, img):
        #this is needed for thread safety due to keras
        model = self.define_model()
        model.load_weights(self.checkpoints)

        img = np.array(img).reshape(1, 28, 28, 1)
        # prepare pixel data
        img = img.astype('float32')
        img = img / 255.0
        predict_x = model.predict(img)
        return np.argmax(predict_x, axis=1)
