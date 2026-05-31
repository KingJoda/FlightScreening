### utils.py ###

import numpy as np


class DriftCalculator():

    def __init__(self):
        # Constants
        self.BallisticCoefficient = 15 #kgm^-2
        self.GravitationalAcceleration = 9.80665 # ms^-1

        # Static Tracker for updating drifts
        self.ZonalDriftTracker     = 0
        self.MeridionalDriftTracker = 0
        self.DensityTracker        = 0
        self.AltitudeTracker       = 0


    ### Change in terminal fallback velocity? - Ask Øyvind
    def _fallBackVelocity(self, highAtmosphericDensity):
        '''
        Calculates Fallback Velocity difference between two regions of differing air density.
        Equation defined in Screening Methodology Part 1

        Parameters:
            self (DriftCalculator): Instantiation of a DriftCalculator object containing static variables to be tracked / used as constants
            highAtmosphericDensity (float): New atmospheric density to compare against the previous value

        Returns:
            fbv (float): Calculated Fallback Velocity
        '''

        lowAtmosphericDensity = self.DensityTracker

        fbv = 2 * np.sqrt((self.BallisticCoefficient * self.GravitationalAcceleration)/(lowAtmosphericDensity + highAtmosphericDensity))

        return fbv


    ### Time for Debris to fall a given distance
    def _fallBackTime(self, highAltitude, fallBackVelocity):
        '''
        Calculates the fallback time between 2 altitudes with a given change in fallback velocity
        Equation defined in Screening Methodology Part 2

        Parameters:
            self (DriftCalculator): Instantiation of a DriftCalculator object containing static variables to be tracked / used as constants
            highAltitude (float): New altitude to be diffed against the stored previous value
            fallbackVelocity (float): Difference in fallback velocity from the two altitudes
        
        Returns:
            timeDiff (float): Time taken to fall between the provided altitude & the stored previous
        '''

        lowAltitude = self.AltitudeTracker

        timeDiff = (highAltitude - lowAltitude)/fallBackVelocity

        return timeDiff


    ### East/West displacement (+ve is East)
    def _zonalDisplacement(self, zonalWindVelocity, fallBackTime): # Assumes average debris speed matches the wind speed
        '''
        Calculates the East/West distance travelled by falling debris 
        Equation defined in Screening Methodology Part 3

        Parameters:
            self (DriftCalculator): Instantiation of a DriftCalculator object containing static variables to be tracked / used as constants
            zonalWindVelocity (float): Measured wind velocity in the East/West direction
            fallBackTime (float): Time taken to fall a given distance
        
        Returns:
            zonalDisp (float): Distance travelled in the East/West direction
        '''

        zonalDisp = zonalWindVelocity * fallBackTime

        return zonalDisp
        

    ### North/West displacement (+ve is North)
    def _meridionalDisplacement(self, meridionalWindVelocity, fallBackTime):
        '''
        Calculates the North/South distance travelled by falling debris 
        Equation defined in Screening Methodology Part 3

        Parameters:
            self (DriftCalculator): Instantiation of a DriftCalculator object containing static variables to be tracked / used as constants
            meridionalWindVelocity (float): Measured wind velocity in the North/South direction
            fallBackTime (float): Time taken to fall a given distance
        
        Returns:
            meridionalDisp (float): Distance travelled in the East/West direction
        '''

        meridionalDisp = meridionalWindVelocity * fallBackTime

        return meridionalDisp


    ### East/West drift (+ve is east)
    def UpdateZonalDrift(self, altitude, density, windVelocity): # Assumes debris drops directly down (no initial zonal velocity)
        '''
        Calculates & updates an internal tracker for total zonal drift. 
        Each increment in altitude change can provide a new difference defined 
        by a change in pressure & wind applied

        Parameters:
            self (DriftCalculator): Instantiation of a DriftCalculator object containing static variables to be tracked / used as constants
            altitude (float):       New altitude 
            density (float):        Air density at the new altitude
            windVelocity (float):   Wind velocity in the East/West direction at the new altitude

        Returns:
            newZonalDrift (float):  Total distance travelled by falling debris in the East/West direction as it falls to sea-level
        '''

        # Calculate the change in Fallback Time
        fv = self._fallBackVelocity( density)
        t  = self._fallBackTime(altitude, fv)

        # Calculate the new Zonal Drift
        disp = self._zonalDisplacement(windVelocity, t)
        newZonalDrift = self.ZonalDriftTracker + disp

        # Update Trackers
        self.DensityTracker    = density
        self.AltitudeTracker   = altitude
        self.ZonalDriftTracker = newZonalDrift

        # .item casts the value back to a python native float
        return newZonalDrift.item()


    ### North/South drift (+ve is north)
    def UpdateMeridionalDrift(self, altitude, density, windVelocity): # Assumes debris drops directly down (no initial meridional velocity)
        '''
        Calculates & updates an internal tracker for total meridional drift. 
        Each increment in altitude change can provide a new difference defined 
        by a change in pressure & wind applied

        Parameters:
            self (DriftCalculator): Instantiation of a DriftCalculator object containing static variables to be tracked / used as constants
            altitude (float):       New altitude 
            density (float):        Air density at the new altitude
            windVelocity (float):   Wind velocity in the North/South direction at the new altitude

        Returns:
            newMeridionalDrift (float): Total distance travelled by falling debris in the North/South direction as it falls to sea-level
        '''

        # Calculate the change in Fallback Time
        fv = self._fallBackVelocity(density)
        t  = self._fallBackTime(altitude, fv)

        # Calculate the new Meridional Drift
        disp = self._meridionalDisplacement(windVelocity, t)
        newMeridionalDrift = self.MeridionalDriftTracker + disp

        # Update Trackers
        self.DensityTracker         = density
        self.AltitudeTracker        = altitude
        self.MeridionalDriftTracker = newMeridionalDrift

        # .item casts the value back to a python native float
        return newMeridionalDrift.item()