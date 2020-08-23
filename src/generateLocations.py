import requests
from random import randint
import math

with open("keys.txt", "r") as key:  # TODO: .gitignore the keys.txt file
    gmapKey = key.read()

def getCoordinates(location):
    parameters = "address={}&key={}".format(location.strip(","), gmapKey)
    response = requests.get("https://maps.googleapis.com/maps/api/geocode/json?" + parameters).json()

    return response['results'][0]['geometry']['location']['lat'], response['results'][0]['geometry']['location']['lng']


def getAllNearbyPOI(lat, lng):
    parameters = "key={}&location={}&radius={}".format(gmapKey, ",".join([str(lat), str(lng)]), 1800)  # 1609 meters in a mile
    response = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json?" + parameters).json()
    return response


def parseNearbyPOI(POIdict):
    POIlist = [] 
    attempts = 0
    while len(POIlist) < 6 and attempts < 20:
        randInteger = randint(0, 19)
        singlePOI = parseOnePOI(POIdict, randInteger)  # type is list

        if int(singlePOI[3]) >= 4:  # at least 4 star rating
            POIlist.append(singlePOI)

        attempts += 1

    if not POIlist:
        output = [parseOnePOI(POIdict, randInteger)]
        return output  # return a list to possibly index later
    else:
        return POIlist


def parseOnePOI(POIdict, value):  # not used in main
    try: # 0 
        name = POIdict['results'][int(value)]['name']
    except:
        name = "null"
    try: # 1
        address = POIdict['results'][int(value)]['vicinity']
    except:
        address = "null"
    try: # 2
        openbool = POIdict['results'][int(value)]['opening_hours']['open_now']
    except:
        openbool = "null"
    try: # 3
        rating = POIdict['results'][int(value)]['rating']
    except:
        rating = 0
    try: # 4
        lat = POIdict['results'][int(value)]['geometry']['location']['lat']
    except:
        raise NameError("lat does not exist")
    try: # 5
        lng = POIdict['results'][int(value)]['geometry']['location']['lng']
    except:
        raise NameError("lng does not exist")

    return [name, address, openbool, rating, lat, lng]  # index 0-5

def calcDistance(coord1, coord2):
    # haversine formula

    # radius of the earth
    radius = 6373.0 # in km, necessary for formula

    lat1 = math.radians(coord1[0])
    lon1 = math.radians(coord1[1])
    lat2 = math.radians(coord2[0])
    lon2 = math.radians(coord2[1])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    haversineOnCentralAngle = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2  # confused? me too
    someOtherNumber = 2 * math.atan2(math.sqrt(haversineOnCentralAngle), math.sqrt(1 - haversineOnCentralAngle))

    return 0.621371 * abs(someOtherNumber * radius) # convert to miles


def getPOIList(location, miles):
    destinationCoordinates = getCoordinates(location)  # destination coordinates

    totalDist = 0
    startLocation = destinationCoordinates  # not in loop, initial declaration
    masterCycledPOIlist = []  # contains all instances of sixPOIChoices
    returnDict = {}
    POIDataCounter = 0
    fullPOIdata = {}

    while totalDist < miles:
        renewableDistDict = {}  # used per generation
        renewableDistList = []
        index = 0
        coordList = []

        POIdict = getAllNearbyPOI(startLocation[0], startLocation[1])  # raw JSON

        sixPOIChoices = parseNearbyPOI(POIdict)  # choose random 6 POI nearby

        for singlePOI in sixPOIChoices:  # choose furthest POI to minimize running in circles
            if singlePOI not in masterCycledPOIlist:  # has a 0.07% chance of perfect repetition, ignoring repeat for now
                coordList.append(singlePOI[4])  # lat
                coordList.append(singlePOI[5])  # lng

                distOutput = calcDistance(startLocation, coordList)
                # distOutput is the distance between two consecutive POI

                # make dictionary to cross check furthest POI (index=0) of following list
                renewableDistDict[index] = distOutput
                # key: index of elements inside sixPOIChoices, value: distance from startLocation

                index = index + 1
                
                renewableDistList.append(distOutput)  # just a list to sort distances

                coordList.clear()

        renewableDistList.sort(reverse=True) # sorts in descending order
        farPOIdist = renewableDistList[0] # access the farthest POI
        
        totalDist = totalDist + farPOIdist # increments totalDist to approach parameter:miles

        for key in renewableDistDict:  # find key number corresp to farPOIdist
            if renewableDistDict[key] == farPOIdist:
                ptlat = sixPOIChoices[key][4] # pt - point
                ptlng = sixPOIChoices[key][5]
        
        POIdata = {} # data for each checkpoint
        for singlePOI in sixPOIChoices: 
            if singlePOI[4] == ptlat and singlePOI[5] == ptlng:     
                POIdata['name'] = singlePOI[0]
                POIdata['address'] = singlePOI[1]
                POIdata['currentlyOpen'] = singlePOI[2]
                POIdata['rating'] = singlePOI[3]

        fullPOIdata[POIDataCounter] = POIdata
        POIDataCounter += 1

        returnDict[startLocation[0], startLocation[1]] = farPOIdist # assign distance to startLocation to make it dist to next coord

        startLocation = ptlat, ptlng # assign new start location to make consecutive checkpoints

        # i dont want to land on the 6 choices that were given, in order to increase distance between user's start point and destination
        masterCycledPOIlist.append(sixPOIChoices)
        
    forIndex = 0
    distTravelled = 0
    # adding up all previous values, since distance in returnDict is distance between, so the last distance value must be:
    # parameter:miles - accumulated distance
    for key in returnDict: 
        if forIndex < len(returnDict)-1:
            distTravelled += returnDict[key]
            forIndex += 1
        else:
            returnDict[key] = miles - distTravelled


    return returnDict, fullPOIdata
# thats what took me the whole day lmao
# seems simple now but everything was stored in my head and hard to get to everythign without going insane :smiling_with_three_hearts:
# any q?
# so that info should help you on the JS end

if __name__ == "__main__":
    run = getPOIList("20 W 34th St, New York, NY 10001", 2)
    print(str(run[0])+"\n"+str(run[1]))
