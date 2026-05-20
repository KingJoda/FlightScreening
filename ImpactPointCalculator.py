### Impact Point Calculator ###

import numpy as np




### Calculates the distance of the displacement from the point of boom
def _impactDistance(zonalDrift, meridionalDrift):

    distance = np.sqrt((zonalDrift**2)*(meridionalDrift**2))

    return distance

### Impact Angle (cone of boom)
def _impactAngle(zonalDrift, meridionalDrift):

    alpha = np.atan2(zonalDrift, meridionalDrift)

    return alpha

### Calculates the offset from a given trajectory location that debris is expected to impact the ground
def _impactDisplacement(zonalDrift, meridionalDrift):
    
    # Calculate the distance & angle of displacement
    distance = _impactDistance(zonalDrift, meridionalDrift)
    angle    = _impactAngle(zonalDrift, meridionalDrift)

    # NOTE: That is the angle from North

    # I don't think this is needed as I actually want to convert the drifts from meters to long / lat deltas



# Calculates the difference in longitude from meters
def _getLongDiff(rocketLatitude, zonalDrift):
    # Assumes radius of 6,371,000,000m (6.371E9)
    globalRadius = 6.371E9

    # Step 1:
    #   Find the radius of the latitudal line
    #   This can be done by doing some old school right angle logic
    #     new radius = sqrt(b**2 - h**2) where
    #       b = 2*RADIUS_OF_EARTH*sin(latitude angle from equator /2)
    #       h = RADIUS_OF_EARTH*sin(latitude angle from equator)

    # TODO: Parameter names should not be b & h...
    b = 2*globalRadius*np.sin(rocketLatitude/2)
    h = globalRadius*np.sin(rocketLatitude)
    radAtLat = np.sqrt(b**2 - h**2)

    # Step 2:
    #   Convert the drift from meters to degrees
    #       pi*r**2 for 360 degs

    longOffset = (360/(np.pi * radAtLat**2)) * zonalDrift

    return  longOffset

# Calculates differnece in latitude from meters
def _getLatDiff(meridionalDrift):
    # NOTE: Latitude diff should be the same at any longitude as 
    # all longitudes have the same radius
    
    # Assumes radius of 6,371,000,000m (6.371E9)
    globalRadius = 6.371E9

    latOffset = (360/(np.pi * globalRadius**2)) * meridionalDrift

    return latOffset

# Calculates great-circle diameter at a given height
def debrisImpactPoint(rocketLongitude, rocketLatitude, zonalDrift, meridionalDrift):

    # Convert zonalDrift into longitude diff - depends on current latitude
    longDiff = _getLongDiff(rocketLatitude, zonalDrift)

    # Convert meridionalDrift into latitudinal diff
    latDiff = _getLatDiff(meridionalDrift)

    # Apply the offsets to the original rocket latitude / longitudes
    newLongitude = rocketLongitude + longDiff
    newLatitude  = rocketLatitude  + latDiff

    return newLatitude, newLongitude



# Truthfully, I guessed how to do this bit, please tell me how to do this properly
def isCoordinateInPolygon(polygonVertices, coordinate):

    isInside = False

    # Find "centre" of polygon - avg latitude & avg longitude
    centreLat  = sum(polygonVertices[0])/len(polygonVertices[0])
    centreLong = sum(polygonVertices[1])/len(polygonVertices[1])

    # Check the coordinate is not bang on centre
    if (centreLat == coordinate[0]) and (centreLong == coordinate[1]):
        isInside = True

    # For each vertex in the polygon, check the coordinate is not between any of the lat/long values
    maxCoordIdx = len(polygonVertices[0]) -1
    for coordIdx in range(maxCoordIdx):
        coord = [polygonVertices[0][coordIdx], polygonVertices[1][coordIdx]]
        minLat  = min([coord[0], centreLat])
        maxLat  = max([coord[0], centreLat])
        minLong = min([coord[1], centreLong])
        maxLong = max([coord[1], centreLong])

        if ((minLat  >= coordinate[0]) and (maxLat  <= coordinate[0]) and
            (minLong >= coordinate[1]) and (maxLong <= coordinate[1])):
            isInside = True

    return isInside
    