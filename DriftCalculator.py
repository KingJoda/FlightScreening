### DriftCalculator.py ###

import numpy as np


class DriftCalculator():

    def __init__(self):
        # Constants
        # TODO: chexk this is lb/ft2 hahaha
        self.BallisticCoefficient = 15 #kgm^-2
        self.GravitationalAcceleration = 9.80665 # ms^-1

        # Static Tracker for updating drifts
        self.ZonalDriftTracker     = 0
        self.MeridionalDriftTracker = 0
        self.DensityTracker        = 0
        self.AltitudeTracker       = 0


    ### Change in terminal fallback velocity? - Ask Øyvind
    def _fallBackVelocity(self, highAtmosphericDensity):

        lowAtmosphericDensity = self.DensityTracker

        fbv = 2 * np.sqrt((self.BallisticCoefficient * self.GravitationalAcceleration)/(lowAtmosphericDensity + highAtmosphericDensity))

        return fbv


    ### Time for Debris to fall a given distance
    def _fallBackTime(self, highAltitude, fallBackVelocity):

        lowAltitude = self.AltitudeTracker

        timeDiff = (highAltitude - lowAltitude)/fallBackVelocity

        return timeDiff


    ### East/West displacement (+ve is East)
    def _zonalDisplacement(self, zonalWindVelocity, fallBackTime):

        zonalDisp = zonalWindVelocity * fallBackTime

        return zonalDisp
        

    ### North/West displacement (+ve is North)
    def _meridionalDisplacement(self, meridionalWindVelocity, fallBackTime):

        meridionalDisp = meridionalWindVelocity * fallBackTime

        return meridionalDisp


    ### East/West drift (+ve is east)
    def UpdateZonalDrift(self, altitude, density, windVelocity):

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


    ### East/West drift (+ve is east)
    def UpdateMeridionalDrift(self, altitude, density, windVelocity):

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