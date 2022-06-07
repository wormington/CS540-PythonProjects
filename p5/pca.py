"""
    Author: Cade Wormington
    Class: CS 540
    Lecture: 
"""

from scipy.io import loadmat
from scipy.linalg import eigh
import numpy as np
from matplotlib import pyplot

# Takes a dataset and centers it relative to the origin.
# filename is the name of the .mat file that stores the dataset.
def load_and_center_dataset(filename):
    dataset = loadmat(filename)
    x = dataset['fea']

    # Converts x to a numpy array
    x = np.array(x)

    # Centers all of our data around the origin by subtracting the mean from our data points.
    centeredData = x - np.mean(x, axis=0)

    return centeredData

# Computes and returns the covariance matrix for a centered dataset.
# dataset is the dataset from which to compute the covariance matrix.
def get_covariance(dataset):
    n = len(dataset)

    # Takes the dot product of the transposed dataset against itself to produce a 1024 x 1024 array.
    # Also the first step in computing the covariance matrix.
    arr = np.dot(np.transpose(dataset), dataset)

    # Divides every item in the array by (n - 1), the final step in computing the covariance matrix.
    for row in range(len(arr)):
        for item in range(len(arr[0])):
            arr[row][item] = arr[row][item] / (n - 1)

    return arr

# Computes and returns the m largest eigenvalues and their eigenvectors in descending order.
# S is the covariance matrix for the dataset.
# m is the number of largest eigenvalues to compute.
def get_eig(S, m):

    # eigh() gets the array of the m largest eigenvalues and thier respective eigenvectors.
    vals, vects = eigh(S, eigvals=(len(S) - m, len(S) - 1))

    # Since the arrays are given to us in ascending order when we want descending order,
    # we flip them.
    descendVals = vals[::-1]

    # We then convert our values to a vertical matrix so that we can multiply them by the identity matrix.
    # This produces the diagonal descending matrix that we want.
    descendVals = np.transpose(descendVals)
    returnVals = descendVals * np.identity(m)

    # Because we flipped the order of eigenvalues above, we must also flip the order of their respective eigenvectors.
    returnVects = vects[:, ::-1]

    return returnVals, returnVects

# Projects an image into the M dimensional space and returns a numpy array representation
# of an image with dimensions d x 1.
# image is the image from the dataset to act on.
# U is the matrix of eigenvectors to use for projection.
def project_image(image, U):

    # Computes the projection of our image into the M dimension.
    # Computed using the formula as shown on Canvas. Note that U and U-transposed are flipped because of Python array orientation.
    preProjection = np.dot(image, U)
    projection = np.dot(preProjection, np.transpose(U))

    return projection

# Uses matplotlib to open a graphical representation of an image from the dataset and its projection
# into the M dimensional space.
# orig is the image from the dataset before projection. It is a 1D array.
# proj is the image from the dataset after projection. It is a 1D array.
def display_image(orig, proj):

    # Converts a 1024 x 1 array representation of an image to a 32 x 32 array representation.
    # Works by appending 32 rows of 32 pixels to origImage. The outer for loop initializes pixRow
    # and appends it to origImage at the end. The inner for loop appends each pixel to its respective
    # position in pixRow.
    origImage = []
    for row in range(0, len(orig), 32):
        pixRow = []
        for pixel in range(row, row + 32, 1):
            pixRow.append(orig[pixel])
        origImage.append(pixRow)

    # Rotates the final array to correct for rotation.
    origImage = np.array(origImage)
    origImage = np.transpose(origImage)

    # Converts a 1024 x 1 array representation of an image to a 32 x 32 array representation.
    # Works by appending 32 rows of 32 pixels to projImage. The outer for loop initializes pixRow
    # and appends it to projImage at the end. The inner for loop appends each pixel to its respective
    # position in pixRow.
    projImage = []
    for row in range(0, len(proj), 32):
        pixRow = []
        for pixel in range(row, row + 32, 1):
            pixRow.append(proj[pixel])
        projImage.append(pixRow)

    # Rotates the final array to correct for rotation.
    projImage = np.array(projImage)
    projImage = np.transpose(projImage)

    # Creates 1 row with 2 columns of subplots.
    figure, axes = pyplot.subplots(nrows=1, ncols=2)

    # Sets the titles of the subplots to their respective image names.
    axes[0].set_title('Original')
    axes[1].set_title('Projection')

    # Places each image into its subplot.
    origColor = axes[0].imshow(origImage, aspect='equal')
    projColor = axes[1].imshow(projImage, aspect='equal')

    # Gives each image a colorbar.
    figure.colorbar(origColor, ax=axes[0])
    figure.colorbar(projColor, ax=axes[1])

    # Shows the subplots.
    pyplot.show()
    return
