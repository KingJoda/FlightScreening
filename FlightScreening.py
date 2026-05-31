### FlightScreening.py ###

# Python Packages
import pandas as pd
import numpy as np
import scipy

# Utility Functions
from DriftCalculator import DriftCalculator
import ImpactPointCalculator
import dataHandler

### TODO: ADD DOCSTRINGS, UPDATE isCoordinateInPolygon

# Constants
AltitudeGranularity = 1 # NOT USED, REMOVE

def genDriftLuts(WeatherLut):
    '''
    Generates LUTs for Zonal & Meridional Drift
    
    Parameters:
        WeatherLut (list): Nested list containing data about atmospheric density & zonal & merirional wind velocities at given altitudes.
    
    Returns:
        DriftLut (list): Nested list containing data about debris zonal & meridional drift at given altitudes.
    '''

    # Create an instance of DriftCalculator. 
    # An instance is required as python makes static variables difficult
    driftCalc = DriftCalculator()

    DriftLut = [[],[],[]]

    dataIdx = 0

    # For each weather reading, calculate the Zonal & Meridional Drift & append it to the LUT
    # TODO: Sort the LUT to ensure the values are in order.....
    while dataIdx < len(WeatherLut[0]):

        # Get relevant data
        altitude = WeatherLut[0][dataIdx]
        density  = WeatherLut[1][dataIdx]
        zonalV   = WeatherLut[2][dataIdx]
        meridV   = WeatherLut[3][dataIdx]

        # Calculate zonal drift
        # NOTE: This function internally updates static trackers
        # BUG: This goes to -infinity eventually.....
        newZonalDrift = driftCalc.UpdateZonalDrift(altitude, density, zonalV)
        newMeridDrift = driftCalc.UpdateMeridionalDrift(altitude, density, meridV)

        # Populate the new LUT with the values
        DriftLut[0].append(altitude)
        DriftLut[1].append(newZonalDrift)
        DriftLut[2].append(newMeridDrift)

        # Increment the index
        dataIdx+=1
    
    return DriftLut



def analyseScreening():
    '''
    Main function: Calls functions to read weather data & convert them to zonal & meridional drifts.
                   These are then converted into latitudinal & longitudinal degreee changes & compared 
                   to a Debris Exclusion Zone (DEZ). If debris is expected to fall within the DEZ, 
                   the script will trigger an exception.
    
    TODO: Make something more intelligent for error reporting than hard-fail
    '''

    # Process the data files into LUTs
    TrajectoryLut = dataHandler.getTrajectory()
    WeatherLut = dataHandler.getWeatherData()
    DEZLut = dataHandler.getDebrisExclusionZone()

    # Use the weather data to create drift LUTs
    DriftLut = genDriftLuts(WeatherLut)

    # # Get the highest altitude from a trajectory LUT to loop from later
    # altitude = max(LatitudeLut[0]) # Could take final value but that makes an assumption about the file
    # To avoid making assumptions about the trajectory, for now just use the exact data provided
    maxTrajectoryDataIdx = len(TrajectoryLut[0]) -1

    # Check each granularity of altitude - Assumes measurements were less than 1s apart ;)
    # NOTE: Appendix B 14 CFR Part 420 Annex B1 Table B-1 states using an altitude up to 
    #       50,000 ft so potentially this could be sped up by checking a maximum altitude of 15240m
    # TODO: Look into 14 CFR Appendix-B-to-Part-420(c)(4) not sure if this is related to the calc or the source of data
    for trajectoryIdx in range(maxTrajectoryDataIdx):

        # Get the altitude
        altitude = TrajectoryLut[0][trajectoryIdx]

        # Determine the Zonal & Meridional Drift at the given altitude
        # Screening Methodology Part 5 states that this can be linearly interpolated
        zonalDrift = np.interp(altitude, DriftLut[0], DriftLut[1])
        meridDrift = np.interp(altitude, DriftLut[0], DriftLut[2])

        # Calculate the Impact Location
        rocketLatitude  = TrajectoryLut[1][trajectoryIdx]
        rocketLongitude = TrajectoryLut[2][trajectoryIdx]
        impactCoord = ImpactPointCalculator.debrisImpactPoint(rocketLongitude, rocketLatitude, zonalDrift, meridDrift)

        # Determine whether the Impact Location was outside the DEZ
        isInside = ImpactPointCalculator.isCoordinateInPolygon(DEZLut, impactCoord)

        if (True == isInside):
            raise Exception(f"IMPACT WITHIN DEZ DETECTED - NOGO.\n\
                              Impact Location ->\tLatitude: {impactCoord[0]}, Longitude: {impactCoord[1]}\n\
                              Rocket Altitidue ->\t{altitude}m")
        
    
    print(f"No impact within DEZ. Launch is Go.")


### Runs when the python script does 
if "__main__" == __name__:

    # Calls high-level function
    analyseScreening()