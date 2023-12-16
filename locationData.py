#!/usr/bin/env python
"""
Name: Nathan Atchison & Isaac Teo
Date: December 14, 2022
Course Code: CS-473-1

Authors: Nathan Atchison & Isaac Teo 2023

Purpose: The purpose of this file is to get data about groups and destinations
"""

# importing geopy library and Nominatim class
from geopy.geocoders import Nominatim
from helperFunctions import normalizeLongLats
import csv

# Src: https://medium.com/@hazallgultekin/convert-address-to-latitude-longitude-using-python-21844da3d032

# This function gets the group data from our GroupData.csv file and uses it to find Geographical Data to be used for clustering
# Inputs: N/A
# Outputs/Returns: groupSize: Dictionary containing all the group sizes
#                  normLongLatDict: Dictionary containing all the normalized longitudes and latitudes of each destination
def getData():
    groupLoc = {}
    groupSize = {}

    # Open the Group Data spreadsheet
    with open("GroupData.csv", mode = 'r') as file:
        # Read the .csv file and create dictionaries for every line
        csvFile = csv.DictReader(file)
        # Run through every line of data in our .csv file
        for line in csvFile:
            # Get the full address for the destination from our .csv
            fullAddress = line['Address'] + "," + line['City'] + "," + line['State']
            # Get the name of the group
            groupName = line['Group_Name']
            # Get how many students are in this group
            numStudents = line['Number_Of_Students']
            # Store the address with the group name as the key
            groupLoc[groupName] = fullAddress
            # Store the size of the group with the group name as the key
            groupSize[groupName] = int(numStudents)
            
    # calling the Nominatim tool and create Nominatim class
    loc = Nominatim(user_agent="Geopy Library")

    # Address for Whitworth
    homeLoc = loc.geocode("300 W Hawthorne Rd, Spokane, WA", timeout=None)

    # Initialize our dictionary that will contain the longitudes 
    # and latitudes of all destinations
    longLatDict = {}

    # Run through every group for Community Building Day
    for group in groupLoc:
        # Create the getLoc object containg data about the destination
        getLoc = loc.geocode(groupLoc[group], timeout=None)
        # Store the latitude and longitude of the location in the longLatDict Dictionary
        longLatDict[group] = {}
        longLatDict[group]["Longitude"] = getLoc.longitude
        longLatDict[group]["Latitude"] = getLoc.latitude

    # Normalize the latitudes and longitudes
    normLongLatDict = normalizeLongLats(longLatDict, homeLoc)
        
    return groupSize, normLongLatDict
