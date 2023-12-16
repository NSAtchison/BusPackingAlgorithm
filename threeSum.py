#!/usr/bin/env python
"""
Name: Nathan Atchison & Isaac Teo
Date: December 14, 2022
Course Code: CS-473-1

Authors: Nathan Atchison & Isaac Teo 2023

Purpose: The purpose of this file is to develop a threeSum algorithm to use in the bus packing problem
"""

# This function goes through each group in each cluster and checks if the sum of any three
# group's sizes can fill any of the bus sizes from among the available buses
# Inputs: cluster: Dictionary containing the groups within a cluster
#         busSize: Integer value of a bus's size
#         groupSizes: Dictionary containing the size of each group
#         busGrouping: Dictionary of lists containing the groups assigned to each bus
#         busData: Dictionary containing the sizes and number of buses
# Outputs: N/A, busGroupings, busData, and cluster get modified
def threeSum(cluster, busSize, groupSizes, busGroupings, busData):
    # Run through every index in our array
    for group1 in cluster:
        # Get the first number in our 3sum
        firstNum = groupSizes[group1]
        for group2 in cluster:
            # Get the next number in our 3 sum
            secondNum = groupSizes[group2]
            # Calculate the value we are searching for
            searchNum = busSize - (firstNum + secondNum)
            # Check if there is a group with the size we are looking for
            if searchNum in groupSizes.values():
                # Find the name of that group
                group3 = list(groupSizes.keys())[list(groupSizes.values()).index(searchNum)]
                # Make sure that we have 3 distinct groups and that we have a bus of size busSize
                if group3 != group1 and group3 != group2 and group1 != group2 and group3 in cluster and busData[busSize] > 0:
                    # Add the 3 groups to our busGroupings dictionary
                    if busGroupings[busSize]:
                        busGroupings[busSize].append([group1, group2, group3])
                    else:
                        busGroupings[busSize] = [[group1, group2, group3]]
                    # Remove one bus of size busSize from our busData dictionary
                    busData[busSize] -= 1
                    # Remove the three groups from our cluster
                    cluster.remove(group1)
                    cluster.remove(group2)
                    cluster.remove(group3)
                    # Recursively go through the cluster to find more 3Sums to pack into buses
                    threeSum(cluster, busSize, groupSizes, busGroupings, busData)
                    # Break statement prevents duplicate attempts to add groups (Necessary in 3Sum)
                    break
