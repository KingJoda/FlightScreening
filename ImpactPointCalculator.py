### Impact Point Calculator ###

import numpy as np


#### Screening Methodology Point 6 - currently unused

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





### Longitude / latitude diff calculations

# Calculates the difference in longitude from meters
def _convertMetersToLongitudeDiff(rocketLatitude, zonalDrift):
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
def _convertMetersToLatitudeDiff(meridionalDrift):
    # NOTE: Latitude diff should be the same at any longitude as 
    # all longitudes have the same radius
    
    # Assumes radius of 6,371,000,000m (6.371E9)
    globalRadius = 6.371E9

    latOffset = (360/(np.pi * globalRadius**2)) * meridionalDrift

    return latOffset

# Calculates great-circle diameter at a given height
def debrisImpactPoint(rocketLongitude, rocketLatitude, zonalDrift, meridionalDrift):

    # Convert zonalDrift into longitude diff - depends on current latitude
    longDiff = _convertMetersToLongitudeDiff(rocketLatitude, zonalDrift)

    # Convert meridionalDrift into latitudinal diff
    latDiff = _convertMetersToLatitudeDiff(meridionalDrift)

    # Apply the offsets to the original rocket latitude / longitudes
    newLongitude = rocketLongitude + longDiff
    newLatitude  = rocketLatitude  + latDiff

    return newLatitude, newLongitude






### Bit for (bad) polygon logic

LineGranularity = 10 #m

def _getGranularityFromMeters(coordA, coordB):

    Granularity = 10#m TODO: Check 420 Appendix B for a granularity requirement
    percentageGran = 0.1
    
    """
    An applicant shall satisfy the map and plotting data requirements for a downrange area of appendix A, paragraph (b).
    """

    # Convert Latitudinal distance to m

    # Convert Longitudinal distance to m

    # Calculate total displacement

    # Find what percentage of the displacement gives the correct granularity in meters

    return percentageGran

def _getPointsOnALine(coordA, coordB):

    # Index 0 is a list of latitudinal locations
    # Index 1 is a list of longitudinal locations
    listOfPoints = [[],[]]

    # Granularity needs to be a percentage to ensure even number of points 
    # between A & B. This percentage can be calculated based on the total 
    # displacement to ensure a minimum granularity
    # TODO: Check Appendix B to part 420 for guidance
    granularity = _getGranularityFromMeters(coordA, coordB) # decimal, not percent

    latOrigin  = coordA[0]
    longOrigin = coordA[1]

    latDiff  = coordA[0] - coordB[0]
    longDiff = coordA[1] - coordB[1]

    # Explain how this is working
    offset = 0

    while offset < 1:

        newLatitude  = latOrigin  + latDiff*offset
        newLongitude = longOrigin + longDiff*offset

        listOfPoints[0].append(newLatitude)
        listOfPoints[1].append(newLongitude)

        offset += granularity

    return listOfPoints





# BUG: If the polygon has any inward pointing vertices, this will take into account some out of boundry locations.
# Could report a false negative - not dangerous, just a waste of time
def isCoordinateInPolygon(polygonVertices, coordinate):

    isInside = False

    # Find "centre" of polygon - avg latitude & avg longitude
    centreLat  = sum(polygonVertices[0])/len(polygonVertices[0])
    centreLong = sum(polygonVertices[1])/len(polygonVertices[1])

    # Check the coordinate is not bang on centre
    if (centreLat == coordinate[0]) and (centreLong == coordinate[1]):
        isInside = True
    
    # For a line between 2 points, get an array of coordinates describing the line
    # This loop will access idx & idx+1 so range needs to be decremented
    # -1 to take into account 0 indexing, -1 to avoid going out of band
    maxVertexIdx = len(polygonVertices[0]) -2
    for idx in range(maxVertexIdx):
        # NOTE: Assumes the vertices are in order - may need to compare all
        # Get 2 adjacent coordinates
        coordA = [polygonVertices[0][idx],   polygonVertices[1][idx]]
        coordB = [polygonVertices[0][idx+1], polygonVertices[1][idx+1]]

        # Get an array of locations to check
        pointsOnALine = _getPointsOnALine(coordA, coordB)

        # Loop over the coordinates & ensure the point is not in the range
        maxCoordIdx = len(pointsOnALine[0])-1
        for coordIdx in range(maxCoordIdx):
            coord = [pointsOnALine[0][coordIdx], pointsOnALine[1][coordIdx]]
            minLat  = min([coord[0], centreLat])
            maxLat  = max([coord[0], centreLat])
            minLong = min([coord[1], centreLong])
            maxLong = max([coord[1], centreLong])

            if ((minLat  >= coordinate[0]) and (maxLat  <= coordinate[0]) and
                (minLong >= coordinate[1]) and (maxLong <= coordinate[1])):
                isInside = True

    return isInside
    