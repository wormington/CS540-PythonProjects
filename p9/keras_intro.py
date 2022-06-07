"""
    Author: Cade Wormington
    Class: CS 540
    Lecture: 
"""

import numpy as np
import matplotlib as mpl
from matplotlib import pyplot
import tensorflow as tf
from tensorflow import keras

# Returns the dataset of clothing images that we use for this project. The boolean parameter 'training' determines
# whether to return the training (True) dataset or the testing (False) dataset.
def get_dataset(training = True):
    # We load the full dataset into 2 tuples.
    fashion_mnist = keras.datasets.fashion_mnist
    (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

    # toReturn is set to the appropriate set of data based on what 'training' is set to.
    toReturn = None
    if training:
        imageArr = np.array(train_images)
        labelArr = np.array(train_labels)
        toReturn = (imageArr, labelArr)
    else:
        imageArr = np.array(test_images)
        labelArr = np.array(test_labels)
        toReturn = (imageArr, labelArr)

    # The dataset is returned.
    return toReturn

# Prints the total number of images, the dimensions of an image, and the amount of each label in the dataset.
def print_stats(images, labels):
    # Sets numImages to the number of images in the dataset.
    numImages = len(images)

    # Sets the image dimension variables to their respective values from the dataset.
    imageDimY = len(images[0])
    imageDimX = len(images[0][0])

    # Creates 'labelDict' as a counter. It then iterates through the label data and counts how many of each label is present.
    labelDict = {'0':0, '1':0, '2':0, '3':0, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0}
    for label in labels:
        labelDict[str(label)] = labelDict[str(label)] + 1

    # Prints the necessary information to the console.
    print(str(numImages))
    print(str(imageDimX) + 'x' + str(imageDimY))
    print('0. T-shirt/top - ' + str(labelDict['0']))
    print('1. Trouser - ' + str(labelDict['1']))
    print('2. Pullover - ' + str(labelDict['2']))
    print('3. Dress - ' + str(labelDict['3']))
    print('4. Coat - ' + str(labelDict['4']))
    print('5. Sandal - ' + str(labelDict['5']))
    print('6. Shirt - ' + str(labelDict['6']))
    print('7. Sneaker - ' + str(labelDict['7']))
    print('8. Bag - ' + str(labelDict['8']))
    print('9. Ankle boot - ' + str(labelDict['9']))
    return

# Shows a window of a specific image and its label. Written using the same methods from P5.
def view_image(image, label):
    # Creates a subplot.
    figure, axes = pyplot.subplots()

    # Sets the title of the only axis since we are only dealing with 1 subplot.
    axes.set_title(label)

    # Sets the plot to show the image we want.
    pos = axes.imshow(image, aspect = 'equal')

    # Generates a colorbar using the image we have just set.
    figure.colorbar(pos, ax = axes)

    # Shows the plot onscreen.
    pyplot.show()
    return

# Creates a model and adds the necessary layers to process our data.
def build_model():
    # First, we create a Sequential() keras object.
    model = keras.Sequential()

    # We then create and add a Flatten() layer. We specify that we are giving it 28x28 images since it is the first layer we add.
    layer1 = keras.layers.Flatten(input_shape = (28, 28))
    model.add(layer1)

    # We then create and add a Dense() layer that has 128 units and uses ReLU (Rectified Linear Unit) activation.
    layer2 = keras.layers.Dense(128, activation = 'relu')
    model.add(layer2)

    # We then create and add one more Dense() layer that has 10 units.
    layer3 = keras.layers.Dense(10)
    model.add(layer3)

    # Finally, we compile our model using the Sparse Categorical Crossentropy loss function, the Adam optimizer, and 'accuracy' as the only metric in 'metrics'.
    model.compile(loss = keras.losses.SparseCategoricalCrossentropy(from_logits = True), optimizer = 'Adam', metrics = ['accuracy'])

    # After compiling, we return the model.
    return model

# This is essentially a wrapper function for Keras's model.fit() function. It trains the model to a dataset.
# The 'model' parameter is the specific model to train. The 'images' and 'labels' parameters are the training images and their
# labels respectively. The 'T' parameter specifies how many epochs (iterations) to train the model over.
def train_model(model, images, labels, T):
    model.fit(x = images, y = labels, epochs = T)
    return

# This is essentially a wrapper function for Keras's model.evaluate() function. It tests the trained model against test data and prints the results.
# The 'model' parameter is the specific model to evaluate. The 'images' and 'labels' parameters are the testing images and their
# labels respectively. The 'show_loss' boolean parameter specifies whether or not to print the loss value after evaluation.
def evaluate_model(model, images, labels, show_loss = True):
    test_loss, test_accuracy = model.evaluate(x = images, y = labels, verbose = 0)

    # If 'show_loss' is false, loss is not printed to console.
    if show_loss:
        print('Loss: ' + str(round(test_loss, 2)))

    print('Accuracy: ' + '{:.2%}'.format(test_accuracy))
    return

# Uses the trained model to predict the label for a given image. It then prints out the top 3 labels and their percentage
# probabilities to the console. The 'model' parameter specifies the model to use for prediction. The 'images' parameter is the 
# dataset of images that we want to predict for. The 'index' parameter is the index for the specific image that we want to get the
# labels for.
#
# Note: predict_label() assumes that the model passed to it will have a Softmax layer as the last layer. This is assumed from the 
# fact that the project instructions say to add this layer BEFORE calling predict_label().
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
