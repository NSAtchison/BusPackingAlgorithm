#!/usr/bin/env python
"""
Name: Nathan Atchison & Isaac Teo
Date: December 14, 2022
Course Code: CS-473-1

Authors: Nathan Atchison & Isaac Teo 2023

Purpose: The purpose of this file is to develop a k-means algorithm to use in the bus packing problem
"""

import math
import numpy as np
from collections import defaultdict

# Puts groups into clusters based on k-means
# Inputs: longLatDict: Dictionary containing all group longitudes and latitudes
#         numBuses: Integer equal to the number of buses available
# Ouputs: clusters: Dictionary of lists containing the clustered groups
def kmeans(longLatDict, numBuses):
    means = []
    for i in range(numBuses):
        # gets random initial means
        xPt = 2*np.random.rand(1)-1  # pick random points within data domain (-1 to 1) along both axises
        yPt = 2*np.random.rand(1)-1
        means.append([i, xPt[0], yPt[0]])   # add initial means index and coordinates to means list
    clusters = defaultdict(list)    # initialize clusters dictionary
    prevClusters = {0}  # temp dictionary to hold the previous cluster

    while prevClusters != clusters: # repeat until the clusters stop changing
        prevClusters = clusters.copy()
        # loops through each group in our dictionary and compares its coordinates to each of our means
        for group in longLatDict:
            groupLong = longLatDict[group]["Longitude"]
            groupLat = longLatDict[group]["Latitude"]
            minDist = float("Inf")  
            closestCluster = 0  
            # loop through each mean and compare its distance to the current group
            for mean in means:
                xDiff = (groupLong - mean[1])**2
                yDiff = (groupLat - mean[2])**2
                dist = math.sqrt(xDiff + yDiff)
                if(dist < minDist): # add group to closest cluster
                    minDist = dist  # stores current minimum distance from current point to nearest mean
                    closestCluster = mean[0]    # stores index of mean closest to current group
            usedGroup = False   # initialize usedGroup to false
            for cluster in clusters:
                if group in clusters[cluster]:
                    usedGroup = True    # if a group has been added to a cluster, set usedGroup to true and exit loop
                    break
            if not usedGroup:   # if group has not been added to a cluster, add it to the closet one
                clusters[closestCluster].append(group)  # add group to nearest cluster

        # loops through each cluster, finds the centroid and adjusts the means based on the centroids
        for cluster in clusters:
            xSum = 0
            ySum = 0
            # gets the sum of x- and y-coodinates and finds the averages of both to determine the centroid of each cluster
            for group in clusters[cluster]:
                xSum += longLatDict[group]["Longitude"]
                ySum += longLatDict[group]["Latitude"]
            means[cluster][1] = xSum/len(clusters[cluster])
            means[cluster][2] = ySum/len(clusters[cluster])

    return clusters # return the dictionary of clusters