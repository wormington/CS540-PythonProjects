"""
    Author: Cade Wormington
    Class: CS 540
    Lecture: 
"""

import math

# euclidean_distance() does a "distance" calculation using the PRCP, TMAX, and TMIN of two data points.
#
# data_point1: the first point to use in the calculation
# data_point2: the second point to use in the calculation
def euclidean_distance(data_point1, data_point2):
    # this uses the 3D euclidean distance formula, except x, y, and z, are replaced with PRCP, TMAX, and TMIN for each point
    dist = math.sqrt(math.pow(data_point1["PRCP"] - data_point2["PRCP"], 2) + math.pow(data_point1["TMAX"] - data_point2["TMAX"], 2) + math.pow(data_point1["TMIN"] - data_point2["TMIN"], 2))
    return dist

# read_dataset() reads the lines of a file as weather data, turns each line into a Dictionary, and puts
# each Dictionary in a List that it returns.
#
# filename: the file name or path of the weather data to read
def read_dataset(filename):
    dictList = []

    # the file is opened in read mode and each line is split by its spaces. the elements split by spaces
    # are assigned to their respective key in a Dictionary. each Dictionary is added to a List that is returned.
    with open(filename, "r") as file:
        for line in file:
            # line.replace() is used to remove the newline characters from the end of the lines
            line = line.replace("\n", "")
            itemList = line.split(" ")
            dictList.append({"DATE":itemList[0], "PRCP":float(itemList[1]), "TMAX":float(itemList[2]), "TMIN":float(itemList[3]), "RAIN":itemList[4]})
    return dictList

# majority_vote() looks at a list of weather data dictionaries and returns the majority value of the "RAIN" key.
# Note: a tie in the vote returns "TRUE".
#
# nearest_neighbors: the list of weather data dictionaries to get the majority for
def majority_vote(nearest_neighbors):
    # trues and falses are counter variables. the respective one is incremented when a weather data dictionary
    # holds its value.
    trues = 0
    falses = 0

    # this for loop iterates through the list to count trues and falses
    for item in nearest_neighbors:
        if item["RAIN"] == "TRUE":
            trues += 1
        else:
            falses += 1

    # the majority value is returned. a tie returns "TRUE".
    if trues > falses:
        return "TRUE"
    elif trues == falses:
        return "TRUE"
    else:
        return "FALSE"

# k_nearest_neighbors() uses the above methods to predict whether it is raining in test_point.
#
# filename: the file name or path of the weather data to read
# test_point: the point that we want to predict the weather of
# k: the number of close data points we want to use for the prediction
def k_nearest_neighbors(filename, test_point, k):
    # calls read_dataset() to populate a list of weather data dictionaries
    dataList = read_dataset(filename)

    # neighbors is a list of weather data dictionaries and their distance to test_point. 
    # it is a 2D array.
    neighbors = []

    # this for loop populates neighbors, a list of k data points that are the closest to test_point.
    for item in dataList:
        dist = euclidean_distance(item, test_point)

        # if there are less than k items in neighbors, any weather data is added.
        if len(neighbors) < k:
            neighbors.append([item, dist])
        # if there are k items in neighbors, farther data points are replaced with closer ones.
        else:
            for i in range(len(neighbors)):
                if neighbors[i][1] > dist:
                    neighbors[i] = [item, dist]
                    break
    
    # nearest_neighbors is the same list as neighbors, except without the extra distance data.
    nearest_neighbors = []
    for neighbor in neighbors:
        nearest_neighbors.append(neighbor[0])

    # the closest points are sent to majority_vote(), where the majority for "RAIN" is calculated and printed.
    print(majority_vote(nearest_neighbors))
