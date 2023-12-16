#!/usr/bin/env python
"""
Name: Nathan Atchison & Isaac Teo
Date: December 14, 2022
Course Code: CS-473-1

Authors: Nathan Atchison & Isaac Teo 2023

Purpose: The purpose of this file is to implement a solution to the bus packing problem
"""

import locationData
import time
from packing import packing
from kmeans import kmeans
from helperFunctions import getNames, getBusData, writeOutput

# Based on c-sharp code written by previous CS-473 students & distributed Kent Jones
# https://whitgit.whitworth.edu/2023/fall/CS-473-1/Group_Projects/project-resources/bus-routing

def main():
    # Get the sizes of all groups and their location data
    groupSizes, locData = locationData.getData()
    # Used for Empiracal Analysis
    # src: https://stackoverflow.com/questions/7370801/how-do-i-measure-elapsed-time-in-python
    start = time.time()
    # Initialize our minimum amount of buses remaining to infinity
    minBuses = float("Inf")
    # Initialize our results to be and empty dictionary
    results = {}
    # Run 100 test cases to try and find the best solution
    for _ in range(100):
        # Grab our initial bus data for the test case
        busData = getBusData()

        # Do our initial packing through kMeans with all groups at the start
        clusters, remBuses, busGroups = packing(kmeans(locData, sum(busData.values())), groupSizes, busData)

        # Run 100 times to optimize the remaining groups not assigned a bus
        for _ in range(100):
            # Grab the location data of the remaining groups
            newLocData = getNames(clusters, locData)
            # Run the packing algorithm for the remaining groups
            newClusters, newRemBuses, newBusGroups = packing(kmeans(newLocData, sum(remBuses.values())), groupSizes, remBuses)
            # Store whoever was leftover after this run of the optimization
            clusters = newClusters
            # Store whatever buses are left after this run of the optimization
            remBuses = newRemBuses
            # Add the new bus groups created through this run of the optimization to our already created groups
            for key in newBusGroups.keys():
                for bus in newBusGroups[key]:
                    busGroups[key].append(bus)
        # Check if the current test case resulted in more buses being used
        if sum(remBuses.values()) < minBuses:
            # Store the data from this test case
            results["Remaining Groups"] = clusters.copy()
            results["Remaining Buses"] = remBuses.copy()
            results["Bus Groupings"] = busGroups.copy()
            # Set the largest number of buses used to be how many we used in this test case
            minBuses = sum(remBuses.values())

    writeOutput(results, groupSizes)
    end = time.time()
    print(end - start)

if __name__ == '__main__':
    main()