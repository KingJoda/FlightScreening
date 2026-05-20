### dataHandler.py ###

import os
import csv
import copy

dataDir = "data"

def getTrajectory():
    '''
    Reads data from trajectory.csv into a data structure that 
    can later be parsed into an interpolation function
    '''

    trajectoryFile = os.path.join(dataDir, "trajectory.csv")
    
    # Create 2 lookups:
    #   - Altitude to Latitude
    #   - Altitude to Longitude

    # TODO: Use pandas structures to look cleaner
    # idx 0 tracks Altitude, 1 tracks Latitude, 2 tracks Longitude
    TrajectoryLut  = [[],[],[]]

    # Replace with pandas dataframe
    with open(trajectoryFile, 'r') as file:
        isHeaderRow = True
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            # Skip the row with column titles
            if True == isHeaderRow:
                isHeaderRow = False
                continue

            # Append values value to LUT
            TrajectoryLut[0].append(float(row[2]))
            TrajectoryLut[1].append(float(row[0]))
            TrajectoryLut[2].append(float(row[1]))

    return TrajectoryLut



def trajectoryInterpolation(dataSet, xVal):
    '''
    Trajectory is parabolic(ish) so should interpolate the data as a parabola
    mate this ain't true don't do that
    '''
    pass



def getWeatherData():
    '''
    Reads data from weather-data.csv into a data structure that 
    can later be parsed into an interpolation function
    '''

    weatherFile = os.path.join(dataDir, "weather_data.csv")
    
    # Create 3 lookups:
    #   - Altitude to density
    #   - Altitude to Zonal Wind Velocity
    #   - Altitude to Meridional Wind Velocity

    # idx 0 tracks Altitude, 1 tracks Density, 2 tracks Zonal Velocity, 3 tracks Meridional Velocity
    WeatherLut = [[],[],[],[]]


    # TODO: Replace this with a Pandas dataframe
    with open(weatherFile, 'r') as file:
        isHeaderRow = True
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            # Skip the row with column titles
            if True == isHeaderRow:
                isHeaderRow = False
                continue

            # Append values to LUT as floats
            WeatherLut[0].append(float(row[0]))
            WeatherLut[1].append(float(row[1]))
            WeatherLut[2].append(float(row[2]))
            WeatherLut[3].append(float(row[3]))
    
    return WeatherLut




def DriftInterpolation(dataSet, xVal):
    '''
    Zonal & Meridional drift is linear across altitude (Part 5 of Screening Methodology)
    
    Parameters:
        dataSet (list): Nested list containing data about zonal & merirional drifts at given altitudes.
    
    Returns:
        yVal (float): Expected value from a linear interpolation
    '''

    # Turns out there is a function for linear interpolation (phew)

    pass



def getDebrisExclusionZone():
    '''
    Reads data from dez.csv into a data structure that 
    can later be parsed into an interpolation function
    '''

    dezFile = os.path.join(dataDir, "dez.csv")
    
    # Create a LUT of coordinates
    
    # Could make list of lines? - Might do a funky point-to-point 
    # interpolation instead - could do both & test timing
    DEZLut = [[],[]]

    # TODO: Do a clever deepcopy instead of this / use pandas
    with open(dezFile, 'r') as file:
        isHeaderRow = True
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            # Skip the row with column titles
            if True == isHeaderRow:
                isHeaderRow = False
                continue

            # Read Latitude to idx 0
            DEZLut[0].append(float(row[0]))
            # Read Longitude into idx 1
            DEZLut[1].append(float(row[1]))
    
    return DEZLut


