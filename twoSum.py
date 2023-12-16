#!/usr/bin/env python
"""
Name: Nathan Atchison & Isaac Teo
Date: December 14, 2022
Course Code: CS-473-1

Authors: Nathan Atchison & Isaac Teo 2023

Purpose: The purpose of this file is to develop a twoSum algorithm to use in the bus packing problem
"""

# This function goes through each group in each cluster and checks if the sum of any two
# group's sizes can fill any of the bus sizes from among the available buses
# Inputs: cluster: Dictionary containing the groups within a cluster
#         busSize: Integer value of a bus's size
#         groupSizes: Dictionary containing the size of each group
#         busGrouping: Dictionary of lists containing the groups assigned to each bus
#         busData: Dictionary containing the sizes and number of buses
# Outputs: N/A, busGroupings, busData, and cluster get modified
def twoSum(cluster, busSize, groupSizes, busGroupings, busData):
    for group in cluster:   # for each group in the current cluster
        if busSize - groupSizes[group] in groupSizes.values(): # check if bus capacity - size of current group = size of another group in cluster
            # Find the second group that will be added to this buss
            secondGroup = list(groupSizes.keys())[list(groupSizes.values()).index(busSize - groupSizes[group])]
            # Make sure that the second group is not the first and that we have buses of this size
            if group != secondGroup and secondGroup in cluster and busData[busSize] > 0:
                # Store the groups for this new bus in our busGrouping dictionary
                if busGroupings[busSize]:
                    busGroupings[busSize].append([group, secondGroup])
                else:
                    busGroupings[busSize] = [[group, secondGroup]]
                # Remove one bus of size busSize from being able to be used
                busData[busSize] -= 1
                # Remove the two groups from this cluster
                cluster.remove(group)
                cluster.remove(secondGroup)
                # Recursively run through the rest of the cluster looking for possible twoSums
                twoSum(cluster, busSize, groupSizes, busGroupings, busData)