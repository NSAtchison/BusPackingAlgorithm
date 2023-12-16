#!/usr/bin/env python
"""
Name: Nathan Atchison & Isaac Teo
Date: December 14, 2022
Course Code: CS-473-1

Authors: Nathan Atchison & Isaac Teo 2023

Purpose: The purpose of this file is to hold functions that aren't major functions and are used throughout the algorithm
"""
import math
import csv
import os

# This function normalized the latitudes and longitudes for each destination
# Inputs: longLatDict: Dictionary containing the non-normalized latitudes and longitudes
#         homeLoc: Object containing the data for Whitworth University
# Outputs/Returns: simpDict: Dictionary containing all the normalized latitudes and logitudes for each group's destinations
# Used this as basis: https://whitgit.whitworth.edu/2023/fall/CS-473-1/Group_Projects/project-resources/bus-routing
def normalizeLongLats(longLatDict, homeLoc):
    # Get the longitude and latitude of our home location (origin), Whiworth
    homeLocLat = homeLoc.latitude
    homeLocLong = homeLoc.longitude
    # Initialize a dictionary to hold our results
    simpDict = {}
    # Run through every group in our longLatDict dictionary
    for group in longLatDict:
        # Initialize a dictionary to be put in simpDict
        simpDict[group] = {}
        # Caluclate the x and y distances away from our home location
        xDist = longLatDict[group]["Longitude"] - homeLocLong
        yDist = longLatDict[group]["Latitude"] - homeLocLat
        # Find the distance between the current groups point and our origin point
        hyp = math.sqrt(xDist**2 + yDist**2)
        # Store the normalized latitudes and lognitudes in our simpDict dictionary
        simpDict[group]["Latitude"] = yDist / hyp
        simpDict[group]["Longitude"] = xDist / hyp
    return simpDict

# Function that gets the names of all groups in our clusters. This is used when optimizing to find what groups are
# left over after running the packing algorithm and return the location data of those groups
# Inputs: clusters: Dictionary containing all the groups in their clusters from the previous iteration
#          locData: Dictionary containing all the location data for every destination
# Outputs/Returns: temp: Dictionary that contains the location data for only the groups in clusters
def getNames(clusters, locData):
    # Initialize the group names array and our dictionary to store data
    groupNames = []
    temp = {}
    # Run through every cluster
    for cluster in clusters:
        # Run through every group in the current cluster
        for group in clusters[cluster]:
            # Add the group to our list of groups
            groupNames.append(group)

    # Run through every group
    for group in groupNames:
        # Get and store the location data of the current group in the temp dictionary
        temp[group] = locData[group]
    # Return the dictionary containing location data for all groups in clusters
    return temp

# Function that gets the the capacity and quantity data for the buses
# Inputs: N/A
# Outputs/Returns: busData: A dictionary contianing the capacity and quanities of buses
def getBusData():
    # Initialize a dictionary for our bus data
    busData = {}
    with open("BusData.csv", mode = 'r') as file:
            csvFile = csv.DictReader(file)
            # Run through every line in our csv file
            for line in csvFile:
                # Grab the size of the bus and how many buses of that size there are
                busSize = line["Capacity"]
                numBuses = line["Quantity"]
                # Store the data with bus size as the key and number of buses as the value
                busData[int(busSize)] = int(numBuses)
    # Return the bus data
    return busData

# Function that takes the remaining groups, who haven't been assigned to a bus, and outputs them to a
# .csv in the outputfiles directory
# Inputs: remGroups: Dictionary containing all groups that weren't packed in the algorithm
#         groupSize: Dictionary containing the sizes of all groups
# Outputs/Returns: Writes the non-packed groups and their size to the Remaining_Groups_Output.csv file
def writeRemGroups(remGroups, groupSizes):
    # Open the output file
    with open('outputfiles/Remaining_Groups_Output.csv', 'w', newline='') as csvfile:
        # Create our writer to the output file
        csvwriter = csv.writer(csvfile)
        # Write a header for our remaining groups
        csvwriter.writerow(["Remaining Groups", "Group Size"])
        # Run through every cluster
        for cluster in remGroups:
            # Run through every group in the cluster
            for group in remGroups[cluster]:
                # Write the group to our output file
                csvwriter.writerow([group, groupSizes[group]])

# Function that takes the remaining buses and their capacity and outputs them to a .csv in the
# outputfiles directory
# Inputs: remBuses: Dictionary containing all buses that weren't used in the algorithm
# Outputs/Returns: Writes the non-used buses to a the Remaining_Buses_Output.csv file
def writeRemBuses(remBuses):
    # Open the output file
    with open('outputfiles/Remaining_Buses_Output.csv', 'w', newline='') as csvfile:
        # Create our writer using Capacity and Quantity as our fields/column labels
        fieldnames = ["Capacity", "Quantity"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write our header for the file
        writer.writeheader()
        # Run through every bus size possible
        for busSize in remBuses:
            # Write the bus size and how many buses remain of that size
            writer.writerow({"Capacity": busSize, "Quantity": remBuses[busSize]})

# Function that takes all groupings and the bus size they were assigned to and writes them to a
# .csv file in the outputfiles directory
# Inputs: busGroupings: Dictionary containing all the groupings and the bus size they are assigned to
# Outputs/Returns: Writes the groupings and their assigned bus size to the Bus_Grouping_Output.csv file
def writeBusGroupings(busGroupings):
    with open("outputfiles/Bus_Grouping_Output.csv", 'w', newline='') as csvfile:
            # Create our writer for the current file
            csvwriter = csv.writer(csvfile)
            # Run through every bus size in our groupings
            for busSize in busGroupings:
                csvwriter.writerow(["Bus Capacity: " + str(busSize)])
                # Run through every grouping
                for grouping in busGroupings[busSize]:
                    # Write the grouping to the .csv file
                    csvwriter.writerow(grouping)
                # Write a gap row for ease of reading
                csvwriter.writerow("")

# Function that writes our results to .csv files in the outputfiles directory
# Inputs: results: Dictionary containing all the information that will be printed to our output files
#         groupSizes: Dictionary containing the sizes of all groups
# Outputs/Returns: A directory containing the three .csv output files will be created
def writeOutput(results, groupSizes):
    # Create the outputfiles directory if it doesn't exist
    if not os.path.exists("outputfiles/"):
        os.makedirs("outputfiles/")
    writeRemGroups(results["Remaining Groups"], groupSizes)
    writeRemBuses(results["Remaining Buses"])
    writeBusGroupings(results["Bus Groupings"])

    
