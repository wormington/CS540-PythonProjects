"""
    Author: Cade Wormington
    Class: CS 540
    Lecture: 
"""

import tensorflow as tf
from tensorflow import keras
import numpy as np

# Returns the image and label data from the fashion_mnist dataset. This function returns a tuple in the format (images, labels).
# The training images and labels are returned when training = True. The test images and labels are returned when training = False.
def get_dataset(training = True):
    # Gets the fashion_mnist data and sets each dataset to its appropriate variable.
    fashion_mnist = keras.datasets.fashion_mnist
    (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

    # Determines if training is True or False and returns the appropriate image and label data.
    # Note that an extra dimension is added to the images to signify that they are greyscale.
    toReturn = None
    if training:
        toReturn = (np.expand_dims(train_images, axis = 3), train_labels)
    else:
        toReturn = (np.expand_dims(test_images, axis = 3), test_labels)
    
    return toReturn

# Returns the model we use for our Convolutional Neural Network, as specified in the instructions.
def build_model():
    # We start with a Keras Sequential object.
    model = keras.Sequential()

    # We first add a Conv2D layer. We specify the input_shape since this is the first layer.
    layer1 = keras.layers.Conv2D(filters = 64, kernel_size = 3, activation = 'relu', input_shape = (28, 28, 1))
    model.add(layer1)

    # We then add another Conv2D layer.
    layer2 = keras.layers.Conv2D(filters = 32, kernel_size = 3, activation = 'relu')
    model.add(layer2)

    # We then add a Flatten layer to get our results into a single dimension.
    layer3 = keras.layers.Flatten()
    model.add(layer3)

    # We then add a Dense layer with a Softmax activation to make our results probabilities.
    layer4 = keras.layers.Dense(units = 10, activation = 'softmax')
    model.add(layer4)

    # Finally, we compile the model and return it.
    model.compile(optimizer = 'Adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])
    return model

# This function takes a basic CNN model and trains it against a dataset. It also validates the model against the 
# test data as it trains. It is essentially a wrapper function for Keras's 'model.fit()'.
# The parameter 'model' is the model to train.
# 'train_img' is the image data to train with.
# 'train_lab' is the label data for the training images.
# 'test_img' is the test image data to validate the model against.
# 'test_lab' is the test label data to go with the image data.
# 'T' is the number of epochs to train the model under.
def train_model(model, train_img, train_lab, test_img, test_lab, T):
    # Note that we turn the label data into categories rather than single integers before passing it to model.fit().
    train_labels = keras.utils.to_categorical(train_lab)
    test_labels = keras.utils.to_categorical(test_lab)

    model.fit(x = train_img, y = train_labels, epochs = T, validation_data = (test_img, test_labels))
    return

# Outputs the top 3 predicted categories for a specified image after running it through the CNN.
# 'model' is the model to use for prediction.
# 'images' is the dataset of images to use for prediction.
# 'index' is the index of the specific image to predict for from 'images'.
def predict_label(model, images, index):
    # class_names is an array of strings, where the index of each label corresponds to the numerical label tag.
    class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle Boot']

    # We call model.predict() to get the 2D array of label predictions. 
    predictions = model.predict(x = images)

    # The label probabilities and their names are added to 'sorter' for easy sorting. Label names are matched to their
    # respective probabilities here.
    sorter = []
    for num in range(10):
        sorter.append([predictions[index][num], class_names[num]])

    # 'sorter' is sorted in descending order according to label probabilities.
    sorter.sort(reverse = True)

    # The top three labels and their names are picked from sorter and printed.
    print(sorter[0][1] + ': ' + '{:.2%}'.format(sorter[0][0]))
    print(sorter[1][1] + ': ' + '{:.2%}'.format(sorter[1][0]))
    print(sorter[2][1] + ': ' + '{:.2%}'.format(sorter[2][0]))

    return
