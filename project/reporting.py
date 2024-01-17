# This is a template.
# You should modify the functions below to match
# the signatures determined by the project specification

from utils import *
import numpy as np


def getPollutantColumn(pollutantType):
    """Gets which collumn of data a pollutant is in"""
    if pollutantType == "NO":
        pollutantTypeCollumn = 2
    if pollutantType == "PM10":
        pollutantTypeCollumn = 3
    if pollutantType == "PM25":
        pollutantTypeCollumn = 4
    return pollutantTypeCollumn


def daily_average(data, monitoring_station, pollutant):
    """Generates the average value every day, giving 365 bits of data"""
    pollutantCollumn = getPollutantColumn(pollutant)
    stationData = data[monitoring_station][:, pollutantCollumn]
    dailyAverageList = []
    tempList = []
    for item in stationData:
        if len(tempList) < 23: #iterates every 24 pieces of data
            tempList.append(item)
        else:
            tempList.append(item)
            dailyAverageList.append(meanvalue(tempList))
            tempList.clear()
    return dailyAverageList


def daily_median(data, monitoring_station, pollutant):
    """Generates the median vaue every day, giving 365 bits of data"""
    pollutantCollumn = getPollutantColumn(pollutant)
    stationData = data[monitoring_station][:, pollutantCollumn]
    dailyMedianList = []
    tempList = []
    for item in stationData:
        if len(tempList) < 23: #iterates every 24 pieces of data
            tempList.append(item)
        else:
            tempList.append(item)
            sortedList = sorted(
                [float(x) if x != "No data" else 0 for x in tempList]) #sorts the list
            Medianval = (sortedList[11] + sortedList[12])/2 #gets the median value
            dailyMedianList.append(Medianval)
            tempList.clear()
    return (dailyMedianList)


def hourly_average(data, monitoring_station, pollutant):
    """Gets the average pollution value for every hour of the day (24 values)"""
    pollutantCollumn = getPollutantColumn(pollutant)
    stationData = data[monitoring_station][:, pollutantCollumn]
    hourlyAverageList = []
    tempList = []
    for x in range(0, 24): 
        tempList = stationData[x::24] #skips every 24 pieces of data
        hourlyAverageList.append(meanvalue(tempList)) #generates average
    return hourlyAverageList


def monthly_average(data, monitoring_station, pollutant):
    """Generates the average value for every month (12 values)"""
    pollutantCollumn = getPollutantColumn(pollutant)
    dateStationData = np.column_stack(
        (data[monitoring_station][:, 0], data[monitoring_station][:, pollutantCollumn])) #gets the date and value
    month = 1
    tempList = []
    monthlyAverageList = []
    for x in range(0, 8760):
        dataMonth = int(dateStationData[x, 0][5:7])
        if dataMonth == month: #means it has got data from a month apart from 1 value
            tempList.append(dateStationData[x, 1])
        elif dataMonth > month: 
            month += 1
            monthlyAverageList.append(meanvalue(tempList))
            tempList.clear()
            tempList.append(dateStationData[x, 1])
    monthlyAverageList.append(meanvalue(tempList))
    return monthlyAverageList


def peak_hour_date(data, date, monitoring_station, pollutant):
    """Your documentation goes here"""
    pollutantCollumn = getPollutantColumn(pollutant)
    dateStationData = np.column_stack(
        (data[monitoring_station][:, 0], data[monitoring_station][:, pollutantCollumn], data[monitoring_station][:, 1]))#gets time and value
    tempList = []
    tempJumboList = []
    for x in range(0, len(data[monitoring_station][:, pollutantCollumn])):
        if date == dateStationData[x, 0]:
            row = x
            break
    for y in range(0, 24):
        tempList.append(dateStationData[row + y, 1])
        tempJumboList.append(dateStationData[row + y, :])
    peakValue = str(maxvalue(tempList))
    timePeakValue = ""
    for z in range(0, 24):
        if peakValue == dateStationData[row + z, 1]:
            timePeakValue = dateStationData[row + z, 2]
            break
    peakValueAndTime = timePeakValue + " : " + str(peakValue) #generates time and peak value
    return peakValueAndTime


def count_missing_data(data,  monitoring_station, pollutant):
    pollutantCollumn = getPollutantColumn(pollutant)
    stationData = data[monitoring_station][:, pollutantCollumn]
    missingDataCount = 0
    for item in stationData:
        if item == "No data": 
            missingDataCount += 1 #counts all missing data
    return missingDataCount


def fill_missing_data(data, new_value,  monitoring_station, pollutant):
    """Your documentation goes here"""
    pollutantCollumn = getPollutantColumn(pollutant)
    stationData = data[monitoring_station][:, pollutantCollumn]
    for x in range(0, len(stationData)):
        if stationData[x] == "No data":
            stationData[x] = new_value #replaces no data with a val
    data[monitoring_station][:, pollutantCollumn] = stationData #replaces data with new data
    return data
