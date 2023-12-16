#!/usr/bin/env python
"""
Name: Nathan Atchison & Isaac Teo
Date: December 14, 2022
Course Code: CS-473-1

Authors: Nathan Atchison & Isaac Teo 2023

Purpose: The purpose of this file is to take clusters created through K-Means clustering and pack as many as possible into buses to full capacity
"""
from collections import defaultdict
from threeSum import threeSum
from twoSum import twoSum

# Implements a packing algorithm for an inputed collection of clusters
# Inputs: clusters: Dictionary containing all clusters created through K-means
#         groupSizes: Dictionary containing all data about groups sizes in our clusters
#         busData: Dictionary containing all data about what buses are available
# Outputs: clusters: Dictionary containing all groups not packed to a bus and
#          busData: Dictionary containing all buses that weren't used
#          busGroupings: Dictionary containing all pairings who were assigned a bus and what size bus they were assigned
def packing(clusters, groupSizes, busData):
    # Sourt the keys of our busData dictionary in descending order
    sortedBusData = sorted(busData.keys(), reverse=True)
    # Initialize our dictionary containing our groupings of buses (how buses have been loaded)
    busGroupings = defaultdict(list)

    # check if any single groups can fill a bus
    # Run for every cluster
    for cluster in clusters:
        # Run for every group in the cluster
        for group in clusters[cluster]:
            # Run for every possible bus size
            for busSize in sortedBusData:
                # Check if a group can fill a bus on their own and that there is a bus of that size
                if groupSizes[group] == int(busSize) and busData[busSize] > 0:
                    # Add group and bus to busGroupings
                    if busGroupings[busSize]:
                        busGroupings[busSize].append([group])
                    else:
                        busGroupings[busSize] = [[group]]
                    # decrement numbers of available buses from busData[busSize]
                    busData[busSize] -= 1
                    clusters[cluster].remove(group) # remove used groups from cluster       
                    break # We've already put the group on a bus, so don't check for any other buses

        # check if any two groups can fill a bus with 2sum
        for busSize in busData.keys():
            twoSum(clusters[cluster], busSize, groupSizes, busGroupings, busData)

        # check if any three groups can fill a bus with 3sum
        for busSize in busData.keys():
            threeSum(clusters[cluster], busSize, groupSizes, busGroupings, busData)
    
    # Return clusters (clusters containing groups that haven't been assigned a bus), busData (How many buses of each capacity remaining),
    # and busGroupings (groups that have been assigned to different bus capacities)
    return clusters, busData, busGroupings
