from numpy import mean
from numpy import std
from matplotlib import pyplot
import config as cfg
from sklearn.model_selection import KFold
from image_classifier.CNNModel import  CNNModel
from image_classifier.DataPreprocessing import DataPreprocessing
from keras import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from keras.optimizer_v1 import SGD
import tensorflow as tf



def define_model():
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

# evaluate the model with 5 (or more) folds
def evaluate_model(dataX, dataY, n_folds=5):
    scores, histories = list(), list()
    # prepare cross validation
    kfold = KFold(n_folds, shuffle=True, random_state=1)
    # enumerate splits
    for train_ix, test_ix in kfold.split(dataX):
        # define model
        model = define_model()
        # select rows for train and validation
        trainX, trainY, validationX, validationY = dataX[train_ix], dataY[train_ix], dataX[test_ix], dataY[test_ix]
        # fit model
        history = model.fit(trainX, trainY, epochs=10, batch_size=32, validation_data=(validationX, validationY),
                            verbose=0)
        # evaluate model
        _, acc = model.evaluate(validationX, validationY, verbose=0)
        print('> %.3f' % (acc * 100.0))
        # append scores
        scores.append(acc)
        histories.append(history)
    return scores, histories


# plot diagnostic learning curves
def summarize_diagnostics(histories):
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


def summarize_performance(scores):
    # print summary
    print('Accuracy: mean=%.3f std=%.3f, n=%d' % (mean(scores) * 100, std(scores) * 100, len(scores)))
    # box and whisker plots of results
    pyplot.boxplot(scores)
    pyplot.show()


if __name__ == '__main__':
    dataLoader = DataPreprocessing(cfg.data['training_images'], cfg.data['training_labels'], cfg.data['test_images'],
                                   cfg.data['test_labels'])
    # dataLoader.visualize_data()
    train_x, train_y, test_x, test_y = dataLoader.process_data()
    scores, history = evaluate_model(train_x, train_y, n_folds=2)
    print(scores)
    summarize_diagnostics(history)
    summarize_performance(scores)
