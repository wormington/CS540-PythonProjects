"""
    Author: Cade Wormington
    Class: CS 540
    Lecture: 
"""

import math
import copy
import random
import csv
import os

# Returns the dataset to be used for the program. In this case, the data is stored in 
# the 'lakedata.csv' file that is in the same directory as the program.
def get_dataset():
    # Gets the directory that the main file is in and tacks on 'lakedata.csv' so that
    # the program can open the data file. This assumes the data file is in the same directory
    # and has the name 'lakedata.csv'.
    dirname = os.path.dirname(__file__)
    filepath = os.path.join(dirname, 'lakedata.csv')

    # Takes the CSV file and creates a 2D array out of the data in the file. It also converts the 
    # strings to ints. 
    with open(filepath) as csvfile:
        csvreader = csv.reader(csvfile)

        returnArr = []
        for line in csvreader:
            tempArr = []
            for item in line:
                tempArr.append(int(item))
            returnArr.append(tempArr)

    # Returns the completed array.        
    return returnArr

# Prints out the dataset length, mean, and sample standard deviation. The mean and sample standard 
# deviation are for the y-values. (days frozen)
def print_stats(dataset):
    dataLen = len(dataset)

    # Calculates the mean for the y-values by adding them up and dividing by the dataset length.
    mean = 0
    for item in dataset:
        mean += item[1]
    mean /= dataLen

    # Calculates the sample std. dev. for the dataset.
    stdDev = 0
    for item in dataset:
        tempVal = item[1] - mean
        tempVal = math.pow(tempVal, 2)
        stdDev += tempVal
    stdDev = stdDev / (dataLen - 1)
    stdDev = math.sqrt(stdDev)

    # Prints out all the required values and rounds them.
    print(str(round(dataLen, 2)))
    print(str(round(mean, 2)))
    print(str(round(stdDev, 2)))

    return

# Calculates the mean squared error for certain values of beta_0 and beta_1.
def regression(beta_0, beta_1):
    dataset = get_dataset()
    dataLen = len(dataset)

    # Performs the mean squared error calculation.
    mse = 0
    for item in dataset:
        tempVal = beta_0 + (beta_1 * item[0]) - item[1]
        tempVal = math.pow(tempVal, 2)
        mse += tempVal
    mse /= dataLen

    # Returns the mean squared error for this dataset.
    return mse

# An alternative form of the above function that allows you to specify the dataset
# to use. It is primarily used in calculations where the data must be normalized.
def regression_norm(beta_0, beta_1, data):
    dataset = data
    dataLen = len(dataset)

    # Performs the mean squared error calculation for the specified dataset.
    mse = 0
    for item in dataset:
        tempVal = beta_0 + (beta_1 * item[0]) - item[1]
        tempVal = math.pow(tempVal, 2)
        mse += tempVal
    mse /= dataLen

    # Returns the mean squared error calculation for the specified dataset.
    return mse

# This functions performs the partial derivatives on the mean squared error and returns them.
def gradient_descent(beta_0, beta_1):
    dataset = get_dataset()
    dataLen = len(dataset)

    # This segment performs the partial derivative on MSE for beta_0.
    parDer0 = 0
    for item in dataset:
        tempVal = beta_0 + (beta_1 * item[0]) - item[1]
        parDer0 += tempVal
    parDer0 = (parDer0 * 2) / dataLen

    # This segment performs the partial derivative on MSE for beta_1.
    parDer1 = 0
    for item in dataset:
        tempVal = beta_0 + (beta_1 * item[0]) - item[1]
        tempVal = tempVal * item[0]
        parDer1 += tempVal
    parDer1 = (parDer1 * 2) / dataLen

    # Returns the partial derivatives.
    return (parDer0, parDer1)

# An alternative form of the above function that allows you to specify the dataset to use.
# It is mainly used to calculate the partial derivatives with a normalized dataset.
def gradient_descent_norm(beta_0, beta_1, data):
    dataset = data
    dataLen = len(dataset)

    # This segment performs the partial derivative on MSE for beta_0.
    parDer0 = 0
    for item in dataset:
        tempVal = beta_0 + (beta_1 * item[0]) - item[1]
        parDer0 += tempVal
    parDer0 = (parDer0 * 2) / dataLen

    # This segment performs the partial derivative on MSE for beta_1.
    parDer1 = 0
    for item in dataset:
        tempVal = beta_0 + (beta_1 * item[0]) - item[1]
        tempVal = tempVal * item[0]
        parDer1 += tempVal
    parDer1 = (parDer1 * 2) / dataLen

    # Returns the partial derivatives.
    return (parDer0, parDer1)

# Another alternative form of the above function that calculates the partial derivatives using
# a random point in the dataset. It is mainly used in the stochastic gradient descent function.
def gradient_descent_norm_sto(beta_0, beta_1, data):
    dataset = data
    dataLen = len(dataset)

    # Chooses a random point in the dataset.
    rand = random.randint(0, dataLen - 1)

    # The random point is used to calculate the partial derivatives as shown in the project instructions.
    parDer0 = 0
    parDer0 = 2 * (beta_0 + (beta_1 * dataset[rand][0]) - dataset[rand][1])

    parDer1 = 0
    parDer1 = 2 * (beta_0 + (beta_1 * dataset[rand][0]) - dataset[rand][1]) * dataset[rand][0]

    # Returns the partial derivatives.
    return (parDer0, parDer1)

# Performs a gradient descent over all items in the dataset.
def iterate_gradient(T, eta):
    betas = [[0, 0]]

    # Performs the specified calculation to update the betas T times. Also uses the specified
    # eta in the calculation.
    for num in range(1, T + 1):
        prevBeta0 = betas[num - 1][0]
        prevBeta1 = betas[num - 1][1]
        parDers = gradient_descent(prevBeta0, prevBeta1)

        newVal0 = eta * parDers[0]
        newVal0 = prevBeta0 - newVal0

        newVal1 = eta * parDers[1]
        newVal1 = prevBeta1 - newVal1

        # Puts the betas into an array so that we can 'save' the value for the next iteration.
        betas.append([newVal0, newVal1])

        # Gets the MSE for the specified betas.
        regVal = regression(betas[num][0], betas[num][1])

        # Prints out the required values and rounds them.
        print(str(num) + " " + str(round(betas[num][0], 2)) + " " + str(round(betas[num][1], 2)) + " " + str(round(regVal, 2)))

    return

# An alternative form of the above function that allows you to specify the dataset to use.
# It is mainly used to perform iterate_gradient() with a normalized dataset.
def iterate_gradient_norm(T, eta, data):
    dataset = data
    betas = [[0, 0]]

    # Performs the specified calculation to update the betas T times. Also uses the specified
    # eta in the calculation.
    for num in range(1, T + 1):
        prevBeta0 = betas[num - 1][0]
        prevBeta1 = betas[num - 1][1]
        parDers = gradient_descent_norm(prevBeta0, prevBeta1, dataset)

        newVal0 = eta * parDers[0]
        newVal0 = prevBeta0 - newVal0

        newVal1 = eta * parDers[1]
        newVal1 = prevBeta1 - newVal1

        # Puts the betas into an array so that we can 'save' the value for the next iteration.
        betas.append([newVal0, newVal1])

        # Gets the MSE for the specified betas.
        regVal = regression_norm(betas[num][0], betas[num][1], dataset)

        # Prints out the required values and rounds them.
        print(str(num) + " " + str(round(betas[num][0], 2)) + " " + str(round(betas[num][1], 2)) + " " + str(round(regVal, 2)))

    return

# Another alternative form of the above function that performs a gradient descent over the data using
# a random point in the dataset. It is mainly used in the stochastic gradient descent function.
def iterate_gradient_norm_sto(T, eta, data):
    dataset = data
    betas = [[0, 0]]

    # Performs the specified calculation to update the betas T times. Also uses the specified
    # eta in the calculation.
    for num in range(1, T + 1):
        prevBeta0 = betas[num - 1][0]
        prevBeta1 = betas[num - 1][1]
        parDers = gradient_descent_norm_sto(prevBeta0, prevBeta1, dataset)

        newVal0 = eta * parDers[0]
        newVal0 = prevBeta0 - newVal0

        newVal1 = eta * parDers[1]
        newVal1 = prevBeta1 - newVal1

        # Puts the betas into an array so that we can 'save' the value for the next iteration.
        betas.append([newVal0, newVal1])

        # Gets the MSE for the specified betas.
        regVal = regression_norm(betas[num][0], betas[num][1], dataset)

        # Prints out the required values and rounds them.
        print(str(num) + " " + str(round(betas[num][0], 2)) + " " + str(round(betas[num][1], 2)) + " " + str(round(regVal, 2)))

    return

# Uses the closed-form equation for calculating beta values.
def compute_betas():
    dataset = get_dataset()
    dataLen = len(dataset)

    # This segment calculates both the x and y means for the dataset.
    xMean = 0
    yMean = 0
    for item in dataset:
        xMean += item[0]
        yMean += item[1]
    xMean /= dataLen
    yMean /= dataLen
    
    # This segment calculates the beta_1 and beta_0 for a dataset.
    topSum = 0
    botSum = 0
    # Calculates the sums needed for the beta_1 calculation.
    for item in dataset:
        tempValX = item[0] - xMean
        tempValY = item[1] - yMean
        topSum += (tempValX * tempValY)
        botSum += math.pow(tempValX, 2)
    
    # Uses the above sums and dataset means to compute the betas.
    beta_1 = topSum / botSum
    beta_0 = yMean - (beta_1 * xMean)

    # Gets the MSE by plugging the betas into regression().
    mse = regression(beta_0, beta_1)

    # Returns the betas and the mean squared error.
    return (beta_0, beta_1, mse)

# Uses the computed betas from compute_betas() and plugs them into the linear regression equation
# to estimate the number of days that Lake Mendota is closed in the specified year.
def predict(year):
    betas = compute_betas()

    prediction = betas[0] + (year * betas[1])

    return prediction

# Performs a gradient descent over all items in the dataset. This function normalizes the x values
# of the dataset before calculation.
def iterate_normalized(T, eta):
    dataset = get_dataset()
    normDataset = copy.deepcopy(dataset)
    dataLen = len(dataset)

    # Calculates the mean of our dataset.
    mean = 0
    for item in dataset:
        mean += item[0]
    mean /= dataLen

    # Calculates the sample standard deviation for our dataset.
    stdDev = 0
    for item in dataset:
        tempVal = item[0] - mean
        tempVal = math.pow(tempVal, 2)
        stdDev += tempVal
    stdDev = stdDev / (dataLen - 1)
    stdDev = math.sqrt(stdDev)

    # Normalizes all x-values in the dataset and puts them into normDataset.
    for item in normDataset:
        item[0] = (item[0] - mean) / stdDev

    # Performs a gradient descent over the normalized dataset. The necessary values are also printed
    # from this function call.
    iterate_gradient_norm(T, eta, normDataset)

    return

# This function is the same as the last function except it does a stochastic gradient descent, so
# the betas are calculated from a random point in the dataset.
def sgd(T, eta):
    dataset = get_dataset()
    normDataset = copy.deepcopy(dataset)
    dataLen = len(dataset)

    # Calculates the mean of our dataset.
    mean = 0
    for item in dataset:
        mean += item[0]
    mean /= dataLen

    # Calculates the sample standard deviation for our dataset.
    stdDev = 0
    for item in dataset:
        tempVal = item[0] - mean
        tempVal = math.pow(tempVal, 2)
        stdDev += tempVal
    stdDev = stdDev / (dataLen - 1)
    stdDev = math.sqrt(stdDev)

    # Normalizes all x-values in the dataset and puts them into normDataset.
    for item in normDataset:
        item[0] = (item[0] - mean) / stdDev

    # Performs a gradient descent over the normalized dataset. The necessary values are also printed
    # from this function call.
    iterate_gradient_norm_sto(T, eta, normDataset)

    return
