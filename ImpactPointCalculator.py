### Impact Point Calculator ###

import numpy as np




##### Screening Methodology Section 6 #####
##### Not currently used in place of latitude and longitide conversions below


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

# Calculates location of the impavt point in latitude & longitude
def debrisImpactPoint(rocketLongitude, rocketLatitude, zonalDrift, meridionalDrift):

    # Convert zonalDrift into longitude diff - depends on current latitude
    longDiff = _convertMetersToLongitudeDiff(rocketLatitude, zonalDrift)

    # Convert meridionalDrift into latitudinal diff
    latDiff = _convertMetersToLatitudeDiff(meridionalDrift)

    # Apply the offsets to the original rocket latitude / longitudes
    newLongitude = rocketLongitude + longDiff
    newLatitude  = rocketLatitude  + latDiff

    return newLatitude, newLongitude






##### Tools for polygon boundary analysis


def _getOffsetGranularity(coordA, coordB):

    Granularity = 10#m TODO: Check 420 Appendix B for a granularity requirement
    
    """
    An applicant shall satisfy the map and plotting data requirements for a downrange area of appendix A, paragraph (b).
    """

    # convert lat to meters

    # convert long to meters

    # find a percentage granularity that matches the expected gran in meters

    return 0.1 # for now test with this





def _getPointsOnALine(coordA, coordB):

    # index 0 is latitude
    # index 1 is longitude
    pointsOnAline = [[],[]]
    
    # Get percentage offset to increment by
    granularity = _getOffsetGranularity(coordA, coordB)

    # Get a start location to apply the offset to
    originLat  = coordA[0]
    originLong = coordA[1]
    
    latDiff  = coordA[0] - coordB[0]
    longDiff = coordA[1] - coordB[1]

    # Append the offset locations to the array
    # 
    offset = 0
    while offset < 1: # maybe <=

        newLatitude  = originLat  + latDiff*offset
        newLongitude = originLong + longDiff*offset
        
        pointsOnALine[0].append(newLatitude)
        pointsOnALine[1].append(newLongitude)

        offset += granularity 


    return pointsOnALine




# BUG: If this polygon has a vertrx that goes tiward the arbitrary centre, this check will include coordinates outside the region, leading to a false negative.
def isCoordinateInPolygon(polygonVertices, coordinate):

    isInside = False

    # Find "centre" of polygon - avg latitude & avg longitude
    centreLat  = sum(polygonVertices[0])/len(polygonVertices[0])
    centreLong = sum(polygonVertices[1])/len(polygonVertices[1])
    
    # Check the coordinate is not bang on centre
    if (centreLat == coordinate[0]) and (centreLong == coordinate[1]):
        isInside = True
    
    # Check locations along each line of the polygon
    # This loop checks points between idx & idx+1 but needs to also check 0 against -1
    maxVertexIdx = len(polygonVertices[0])-1
    for vertexIdx in range(maxCoordIdx):
        coordA = [polygonVertices[0][vertexIdx], polygonVertices[1][vertex]]
        if vertexIdx == maxVertexIdx:
            coordB = [polygonVertices[0][0], polygonVertices[1][0]]
        else:
            coordB = [polygonVertices[0][vertexIdx+1], polygonVertices[1][vertex+1]]
        
        # Get an array of points between the vertices
        pointsOnALine = _getPointsOnALine(coordA, coordB)
        
        # Check that the impact ciirdinate does not land between each point on the line
        maxCoordIdx = len(pointsOnALine[0])
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

    