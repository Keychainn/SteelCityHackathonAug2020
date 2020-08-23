import requests

with open("keys.txt", "r") as key: #TODO: .gitignore the keys.txt file
    gmapKey = key.read()
def getPOIList(location, miles):
    parameters = "address={}&key={}".format(location.strip(","),gmapKey)
    resp = requests.get("https://maps.googleapis.com/maps/api/geocode/json?"+parameters)

    rawJSON = resp.json()

    lat = rawJSON['results'][0]['geometry']['location']['lat']
    lng = rawJSON['results'][0]['geometry']['location']['lng']

    parameters = "key={}&location={}&radius={}".format(gmapKey, str(lat)+","+str(lng), 1800) #1609 meters in a mile
    print("https://maps.googleapis.com/maps/api/place/nearbysearch/json?"+parameters)

getPOIList("20 W 34th St, New York, NY 10001",3)