# This is a template.
# You should modify the functions below to match
# the signatures determined by the project specification

from reporting import *
from intelligence import *
from monitoring import *
from utils import *
import numpy as np
import datetime


def main_menu():
    """
    Takes in the users input and if it is valid calls the correct function.
    If there is an error it iterates until they enter a valid answer.
    """
    userChoice = (input("Welcome to the AQUA system \nPlease select an option to continue: \n\nR - Access the PR module \nI - Access the MI module \nM - Access the RM module \nA - Print the About text \nQ - Quit the application \n\nPlease select an option: \n")).upper()
    valid = False
    while not (valid):
        valid = True
        if userChoice == "R":
            reporting_menu()
        elif userChoice == "I":
            intelligence_menu()
        elif userChoice == "M":
            monitoring_menu()
        elif userChoice == "A":
            about()
        elif userChoice == "Q":
            quit()
        else:
            valid = False
            userChoice = input(
                "Input not accepted \nPlease select an option to continue:\n\nR - Access the PR module\nI - Access the MI module\nM - Access the RM module\nA - Print the About text\nQ - Quit the application\n").upper()


def reporting_menu(pollutionData=None):
    """Assigns pollution data as a dictionary, then asks user what function they want to access, error checks, then asks what monitoring station
    and pollutant they want and error checks both of them. If needed (peak hour date) it will also ask for a date and error check. For fill missing data
    it also asks for a value to replace with. It then calls the relevant functions and calls itself again to repeat the menu."""
    if pollutionData == None:
        pollutionData = {
            "N. Kensington": np.genfromtxt("project\data\Pollution-London N Kensington.csv", delimiter=",", dtype=str, skip_header=1),
            "Marylebone Road": np.genfromtxt("project\data\Pollution-London Marylebone Road.csv", delimiter=",", dtype=str, skip_header=1),
            "Harlington": np.genfromtxt("project\data\Pollution-London Harlington.csv", delimiter=",", dtype=str, skip_header=1)
        }
    userChoice = input("What would you like to access? \n\nDA - Daily average pollution levels \nDM - Daily median pollution levels \nHA - Hourly average pollution levels \nMA - Monthly average pollution levels \nPH - Peak hour for pollution levels on any day \nCD - Count of all missing data \nFD - Fill any missing data \nMM - Main Menu\n").upper()
    valid = False
    while not (valid):
        valid = True
        if userChoice != "DA" and userChoice != "DM" and userChoice != "HA" and userChoice != "MA" and userChoice != "PH" and userChoice != "CD" and userChoice != "FD" and userChoice != "MM":
            valid = False
            userChoice = input("Input not accepted \nPlease select an option to continue:\n\nDA - Daily average pollution levels \nDM - Daily median pollution levels \nHA - Hourly average pollution levels \nMA - Monthly average pollution levels \nPH - Peak hour for pollution levels on any day \nCD - Count of all missing data \nFD - Fill any missing data \nMM - Main Menu\n").upper()
    if userChoice == "MM":
        main_menu()
    monitorStation = ""
    pollutantType = ""
    msValid = False
    ptValid = False
    while not (msValid):
        msValid = True
        monitorStation = input(
            "What Monitoring Station would you like to access data from? \n\nNK - N. Kensington \nMR - Marylebone Road \nH - Harlington\n").upper()
        if monitorStation != "NK" and monitorStation != "MR" and monitorStation != "H":
            msValid = False
            print("Not valid, please try again\n")
    if monitorStation == "NK":
        monitorStation = "N. Kensington"
    if monitorStation == "MR":
        monitorStation = "Marylebone Road"
    if monitorStation == "H":
        monitorStation = "Harlington"
    while not (ptValid):
        ptValid = True
        pollutantType = input(
            "What pollutant would you like? \n\nNO - Nitric Oxide\nPM10 \nPM25\n").upper()
        if pollutantType != "NO" and pollutantType != "PM10" and pollutantType != "PM25":
            ptValid = False
            print("Not valid, please try again\n")
    if userChoice == "DA":
        da = (daily_average(pollutionData, monitorStation, pollutantType))
        DAday = 0
        for item in da:
            DAday += 1
            print("\nDay {}: {}".format(DAday, item))
    if userChoice == "DM":
        dm = (daily_median(pollutionData, monitorStation, pollutantType))
        DMday = 0
        for item in dm:
            DMday += 1
            print("\nDay {}: {}".format(DMday, item))
    if userChoice == "HA":
        ha = (hourly_average(pollutionData, monitorStation, pollutantType))
        HAhour = 0
        for item in ha:
            print("\nHour {}: {}".format(HAhour, item))
            HAhour += 1
    if userChoice == "MA":
        ma = (monthly_average(pollutionData, monitorStation, pollutantType))
        MAmonth = 0
        for item in ma:
            MAmonth += 1
            month = datetime.date(1900, MAmonth, 1).strftime('%B')
            print("\n{}: {}".format(month, item))
    if userChoice == "PH":
        phValid = False
        while phValid == False:  # checks input to make sure it is in correct format
            phValid = True
            dayChosenInput = input(
                "What day would you like? Please input in format YYYY-MM-DD\n")
            try:
                dayChosen = datetime.datetime.strptime(
                    dayChosenInput, "%Y-%m-%d").date()
                dayChosen = str(dayChosen)
                if dayChosen[0:4] != "2021":
                    phValid = False
                    print("Error: date is not from 2021\n")
            except:
                phValid = False
                print("Error: please input date in correct format\n")
        print(peak_hour_date(pollutionData, dayChosen,
              monitorStation, pollutantType))
    if userChoice == "CD":
        print("Amount of missing data: {}".format(
            count_missing_data(pollutionData, monitorStation, pollutantType)))
    if userChoice == "FD":
        fdValid = False
        while fdValid == False:
            fdValid = True
            dataFillInput = input(
                "What data would you like to replace any \"No Data\" values with? Please only enter numbers.\n")
            if isFloat(dataFillInput) == False:
                fdValid = False
                print("Error: That was not a number")
        pollutionData = fill_missing_data(
            pollutionData, dataFillInput, monitorStation, pollutantType)
    print("\n")
    reporting_menu(pollutionData)


def getDates():
    """This gets the date for the monitoring menu to use. It gets a start and end date and error checks it using the validatedatinput function,
    using different errors to figure out what to output. It also allows the user to type in NOW to get the current date. It then returns both dates
    in a tuple"""
    dateValid = False
    errorKey = 0
    currentDayUsed = 0
    while not dateValid:
        dateValid = True
        if errorKey == 0 or errorKey == 1 or errorKey == 3:
            startDate = input(
                "\nWhat start date would you like? (In format YYYY-MM-DD)")
        if errorKey == 0 or errorKey == 2 or errorKey == 3:
            endDate = input(
                "\nWhat end date would you like? (Type NOW for data up until current time, otherwise in format YYYY-MM-DD, make sure the timeframe for the first date is a year or less)")
            if endDate == "NOW":
                endDate = str(datetime.date.today() +
                              datetime.timedelta(days=1))
                currentDayUsed = 1
        errorKey = validateDateInput(
            startDate, endDate, currentDayUsed)
        if errorKey > 0:
            dateValid = False
    return startDate, endDate


def monitoring_menu():
    """Asks them what function they which to use, then calls the get dates function, gets the side code(s) and pollution types from the user, error checking
    them. It then acccesses the api and gets the data in a json format ready for other functions to use. It then calls these functions. It then
    calls itself."""
    valid = False
    while not valid:
        valid = True
        userInput = input("\nWhat function would you like to use? \nPA - Get an average pollution value for a site with a timeframe of max one year \nCS - Get comparison data for two specific sites with a timeframe of max one year \nHL - Get the hours where pollution levels were at their highest and lowest within a timeframe of max one year\nMM - Main Menu\n").upper()
        if userInput != "PA" and userInput != "CS" and userInput != "HL" and userInput != "MM":
            print("\nInput not valid, please try again\n")
            valid = False
    if userInput == "PA":
        dataPresent = False
        while not dataPresent:
            dataPresent = True
            dates = getDates()
            startDate = dates[0]
            endDate = dates[1]
            areaValid = False
            while not areaValid:
                siteCode = input(
                    "\nPlease enter the siteCode for the area you are interested in").upper()
                areaValid = checkSiteCode(siteCode)
                if areaValid == False:
                    print("\nSite code does not exist")
            speciesValid = False
            while not speciesValid:
                speciesCode = input(
                    "\nPlease enter the speciesCode for the pollution species you are interested in").upper()
                speciesValid = checkSpecies(speciesCode)
                if speciesValid == False:
                    print("\nSpecies code does not exist")
            urlTemplate = "https://api.erg.ic.ac.uk/AirQuality/Data/SiteSpecies/SiteCode={site_code}/SpeciesCode={species_code}/StartDate={start_date}/EndDate={end_date}/Json"
            url = urlTemplate.format(
                site_code=siteCode,
                species_code=speciesCode,
                start_date=startDate,
                end_date=endDate
            )
            apiData = requests.get(url).json()
            dataPresent = isDataPresent(apiData)
            if dataPresent == False:
                print("\nNo data present for the dates/site code/species")
        averagePollutionLevels(
            startDate, endDate, apiData, siteCode, speciesCode)
    if userInput == "CS":
        dataPresent = False
        while dataPresent == False:
            areaValid = False
            bothAreaValid = False
            while not bothAreaValid:
                while not areaValid:
                    siteCode1 = input(
                        "\nPlease enter the first site code for one of the areas you want to compare").upper()
                    areaValid = checkSiteCode(siteCode1)
                    if areaValid == False:
                        print("\nFirst site code does not exist")
                areaValid = False
                while not areaValid:
                    siteCode2 = input(
                        "\nPlease enter the second site code for one of the areas you want to compare").upper()
                    areaValid = checkSiteCode(siteCode2)
                    if areaValid == False:
                        print("\nSecond site code does not exist")
                if siteCode1 == siteCode2:
                    print("\nSite codes cannot be the same")
                    bothAreaValid = False
                    areaValid = False
                else:
                    bothAreaValid = True
            dates = getDates()
            startDate = dates[0]
            endDate = dates[1]
            speciesValid = False
            while not speciesValid:
                speciesCode = input(
                    "\nPlease enter the speciesCode for the pollution species you are interested in").upper()
                speciesValid = checkSpecies(speciesCode)
                if speciesValid == False:
                    print("\nSpecies code does not exist")
            urlTemplate1 = "https://api.erg.ic.ac.uk/AirQuality/Data/SiteSpecies/SiteCode={site_code}/SpeciesCode={species_code}/StartDate={start_date}/EndDate={end_date}/Json"
            url1 = urlTemplate1.format(
                site_code=siteCode1,
                species_code=speciesCode,
                start_date=startDate,
                end_date=endDate
            )
            siteOneAPI= requests.get(url1).json()
            dataPresent1 = isDataPresent(siteOneAPI)
            if dataPresent1 == False:
                print("\nNo data present for the dates/1st site code/species")
            urlTemplate2 = "https://api.erg.ic.ac.uk/AirQuality/Data/SiteSpecies/SiteCode={site_code}/SpeciesCode={species_code}/StartDate={start_date}/EndDate={end_date}/Json"
            url2 = urlTemplate2.format(
                site_code=siteCode2,
                species_code=speciesCode,
                start_date=startDate,
                end_date=endDate
            )
            siteTwoAPI= requests.get(url2).json()
            dataPresent2 = isDataPresent(siteTwoAPI)
            if dataPresent2 == False:
                print("\nNo data present for the dates/2nd site code/species")
            if dataPresent2 == False or dataPresent1 == False:
                dataPresent = False
            else: dataPresent = True
        compareSites(siteCode1, siteCode2, siteOneAPI, siteTwoAPI)
    if userInput == "HL":
        dataPresent = False
        while not dataPresent:
            dataPresent = True
            dates = getDates()
            startDate = dates[0]
            endDate = dates[1]
            areaValid = False
            while not areaValid:
                siteCode = input(
                    "\nPlease enter the siteCode for the area you are interested in").upper()
                areaValid = checkSiteCode(siteCode)
                if areaValid == False:
                    print("\nSite code does not exist")
            speciesValid = False
            while not speciesValid:
                speciesCode = input(
                    "\nPlease enter the speciesCode for the pollution species you are interested in").upper()
                speciesValid = checkSpecies(speciesCode)
                if speciesValid == False:
                    print("\nSpecies code does not exist")
            urlTemplate = "https://api.erg.ic.ac.uk/AirQuality/Data/SiteSpecies/SiteCode={site_code}/SpeciesCode={species_code}/StartDate={start_date}/EndDate={end_date}/Json"
            url = urlTemplate.format(
                site_code=siteCode,
                species_code=speciesCode,
                start_date=startDate,
                end_date=endDate
            )
            apiData = requests.get(url).json()
            dataPresent = isDataPresent(apiData)
            if dataPresent == False:
                print("\nNo data present for the dates/site code/species")
        highestAndLowest(apiData, siteCode, speciesCode)
    if userInput == "MM":
        main_menu()
    monitoring_menu()
        


def intelligence_menu():
    """Gets what function the user wants to use, error checks that, then calls the relevant functions, then calls itself."""
    ogMap = "project\data\map.png"
    valid = False
    while not valid:
        valid = True
        userInput = input("\nWhat function would you like to use? \nPR - Generate a map of roads with pavements \nUR - Generate a map of roads with no information regarding pavement ability \nCC  - Generate a list of connected components \nCCO - Generate a list of ordered connected components and produce a graph of the two largest ones \nMM - Main Menu\n").upper()
        if userInput != "PR" and userInput != "UR" and userInput != "CC" and userInput != "CCO" and userInput != "MM":
            print("\nInput not valid, please try again\n")
            valid = False
    if userInput == "PR":
        find_red_pixels(ogMap)
        print("\nMap generated!")
    if userInput == "UR":
        find_cyan_pixels(ogMap)
        print("\nMap generated!")
    if userInput == "CC":
        detect_connected_components(find_red_pixels(ogMap))
        print("\nConnected Components detected!")
    if userInput == "CCO":
        detect_connected_components_sorted(
            detect_connected_components(find_red_pixels(ogMap)))
        print("\nConnected Components detected and ordered!")
    if userInput == "MM":
        main_menu()
    intelligence_menu()


def about():
    """Prints module number and candidate number"""
    print("\nModule No: ECM1400 \nCandidate No:244285")
    main_menu()


def quit():
    """Exits the program"""
    exit()


if __name__ == '__main__':
    main_menu()
