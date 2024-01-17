# This is a template.
# You should modify the functions below to match
# the signatures determined by the project specification.
#
# This module will access data from the LondonAir Application Programming Interface (API)
# The API provides access to data to monitoring stations.
#
# You can access the API documentation here http://api.erg.ic.ac.uk/AirQuality/help
#
from utils import *
import requests
import datetime


def validateDateInput(startDate, endDate, currDayUsed):
    "Validates a start and end date to make sure there are no issues"
    valid = 0
    try:
        sd = datetime.datetime.strptime(startDate, '%Y-%m-%d').date() #checks if start date is in correct format
    except:
        print("\nError: Start date is not in correct format.")
        valid += 1
    try:
        ed = datetime.datetime.strptime(endDate, '%Y-%m-%d').date() #checks if end date is in correct format
    except:
        print("\nError: End date is not in correct format.")
        valid += 2
    if valid > 0:
        return valid
    if datetime.date.today() < ed and currDayUsed == 0: #checks that end date is not in the future
        print("\nError: End date is after current date.")
        valid = 2
    if ed < sd: #checks that the order of the start and end date is correct
        print("\nError: End date is before start date.") 
        valid = 3
    if ed > sd + datetime.timedelta(days=365): #makes sure its no more than 365 days of data
        print("\nError: Timeframe is over year.")
        valid = 3
    return valid


def isDataPresent(apiData):
    """Checks if data is present on the api for a specific time zone, area and species"""
    pollutionData = []
    d = apiData["RawAQData"]["Data"]
    for x in d:
        if x["@Value"] != "":
            pollutionData.append(x["@Value"]) #generates a list of all data
    if pollutionData == []: #checks if list is empty
        return False
    else:
        return True


def checkSiteCode(siteCode):
    """Checks if an inputted site code exists on the API to validate the input"""
    apiData = requests.get(
        "https://api.erg.ic.ac.uk/AirQuality/Information/MonitoringSites/GroupName=London/Json").json()
    d = apiData["Sites"]["Site"]
    Valid = False
    for x in d:
        if siteCode == (x["@SiteCode"]): #iterates through list to check if inputted site code is valid
            Valid = True
    return Valid


def checkSpecies(species):
    """Checks if an inputted species exists on the API to validate the input"""
    apiData = requests.get(
        "https://api.erg.ic.ac.uk/AirQuality/Information/Species/Json").json()
    d = apiData["AirQualitySpecies"]["Species"]
    Valid = False
    for x in d:
        if species == (x["@SpeciesCode"]): #iterates through list to check if inputted species is valid
            Valid = True
    return Valid


def averagePollutionLevels(startDate, endDate, apiData, siteCode, Pollutant):
    """Calculates the average pollution levels for an area between dates(max timeframe of a year)"""
    d = apiData["RawAQData"]["Data"]
    totalHours = 0
    totalDataHours = 0
    pollutionData = []
    for x in d:
        totalHours += 1
        if x["@Value"] != "":
            totalDataHours += 1
            pollutionData.append(x["@Value"]) #generates list of data
    avgPollutionData = meanvalue(pollutionData) #gets average of list
    if totalDataHours == totalHours:
        print("\nThe average pollution value of pollutant {P} at site {S} from {SD} to {ED}({TD} hours) is {AP}".format(
            P=Pollutant, S=siteCode, SD=startDate, ED=endDate, TD=totalHours, AP=avgPollutionData))
    else:
        print("\nThe average pollution value of pollutant {P} at site {S} from {SD} to {ED}({TD} hours, {TDM} hours of which are missing data) is {AP}".format(
            P=Pollutant, S=siteCode, SD=startDate, ED=endDate, TD=totalHours, TDM=totalHours-totalDataHours, AP=avgPollutionData))


def compareSites(firstSite, secondSite, API1, API2):
    """Compares the data from two sites and gives: Averages, how many times the pollution levels were higher on each site, and find the hours
    where the difference between the pollution values was at its biggest in both ways"""
    siteOneD = API1["RawAQData"]["Data"]
    siteTwoD = API2["RawAQData"]["Data"]
    siteOneData = []
    siteTwoData = []
    siteOneValues = []
    siteTwoValues = []
    for x in siteOneD:
        siteOneData.append((x["@MeasurementDateGMT"], x["@Value"])) #gets a list of tuples with the time and value
    for y in siteTwoD:
        siteTwoData.append((y["@MeasurementDateGMT"], y["@Value"])) #gets a list of tuples with the time and value
    for x1 in siteOneD:
        siteOneValues.append(x1["@Value"]) #gets a list of just the values
    for y1 in siteTwoD:
        siteTwoValues.append(y1["@Value"]) #gets a list of just the values
    siteOneAvg = meanvalue(siteOneValues)
    siteTwoAvg = meanvalue(siteTwoValues)
    print("\nAverages: Site 1({S1}) average: {A1}, Site 2({S2}) average: {A2}".format(
        S1=firstSite, S2=secondSite, A1=siteOneAvg, A2=siteTwoAvg))
    dataLen = len(siteOneData)
    s1Bigger = 0
    s2Bigger = 0
    for z in range(0, dataLen):
        if siteOneValues[z] != "" and siteTwoValues != "":
            if siteOneValues[z] > siteTwoValues[z]: #checks when site one has more pollution than site two
                s1Bigger +=1
            if siteTwoValues[z] > siteOneValues[z]: #checks when site two has more pollution than site one
                s2Bigger +=1
    print("\nTimes pollution levels were higher in {S1}: {S1B}. Times pollution levels were higher in {S2}: {S2B}. (Data compared only on hours where both sites had an entry)".format(
        S1=firstSite, S2=secondSite, S1B=s1Bigger, S2B=s2Bigger))
    biggestDiff1 = 0
    biggestDiff2 = 0
    biggestDiff1Hour = ''
    biggestDiff2Hour = ''
    for z in range(0, dataLen):
        if siteOneValues[z] != "" and siteTwoValues[z] != "":
            siteOneValue = float(siteOneValues[z])
            siteTwoValue = float(siteTwoValues[z])
            diff1 = siteOneValue - siteTwoValue
            diff2 = siteTwoValue - siteOneValue
            if diff1 > biggestDiff1:
                biggestDiff1 = diff1
                biggestDiff1Hour = siteOneData[z][0] #checks if it is the biggest difference
            if diff2 > biggestDiff2:
                biggestDiff2 = diff2
                biggestDiff2Hour = siteTwoData[z][0] #checks if it is the biggest difference
    print("\nThe time where {S1} had the biggest size compared to {S2} was {T1} and the difference was {D1}.".format(
        S1=firstSite, S2=secondSite, T1=biggestDiff1Hour, D1=biggestDiff1))
    print("\nThe time where {S2} had the biggest size compared to {S1} was {T2} and the difference was {D2}.".format(
        S1=firstSite, S2=secondSite, T2=biggestDiff2Hour, D2=biggestDiff2))


def highestAndLowest(data, siteCode, species):
    """Outputs the five highest and lowest pollution values from the specified time frame (year or less)"""
    d = data["RawAQData"]["Data"]
    allData = []
    for x in d:
        if x["@Value"] != "":
            allData.append((x["@MeasurementDateGMT"], float(x["@Value"])))
    length = len(allData)
    allData.sort(key=lambda t: t[1], reverse = True) #orders the list according the second value in the tuple
    print("\nHighest Pollution Values:")
    for y in range(0,5): #generates top 5 values
        print("\n{no}: {time} - {value}".format(
            no = y+1, time=allData[y][0], value=allData[y][1]))
    print("\nLowest Pollution Values:")
    for z in range(0,5): #generates bottom 5 values
        print("\n{no}: {time} - {value}".format(
            no = z+1, time=allData[length - z - 1][0], value=allData[length - z - 1][1]))