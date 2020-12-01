import json
import sys
import requests
from app.includes.databaseAccessor import getIncidentIds, insertIncident, getDistanceBetweenPoints


# Get a list of all incident ids currently in database
idsFromDB = []
for row in getIncidentIds(useDotEnvFlag=True):
    row = json.loads(json.dumps(row))
    for r in row:
        if row[r] not in idsFromDB:
            idsFromDB.append(row[r])


# Get a list of all incidents from InciWeb feed
url = 'https://inciweb.nwcg.gov/feeds/json/esri/'
incidentsFromFeed = requests.get(url).json()['markers']
newIncidents = []
for row in requests.get(url).json()['markers']:
    if row['id'] not in idsFromDB:
        newIncidents.append(row)


# Insert new incidents into database
if newIncidents:
    print(f"{len(newIncidents)} new incident(s) found")
    for incident in newIncidents:
        try:
            insertIncident(incident, useDotEnvFlag=True)
            print(f"Incident {incident['id']} added to database")
        except Exception as e:
            print(f"Failed to insert incident {incident['id']}: {str(e)}")
else:
    print('No new incidents')

incident1 = incidentsFromFeed[0]
incident2 = incidentsFromFeed[1]
distance = getDistanceBetweenPoints(incident1['lng'], incident1['lat'], incident2['lng'], incident2['lat'], useDotEnvFlag=True)
for row in distance:
    distanceMeters = row['getdistancebetweenpoints']
    distanceMiles = float(distanceMeters) * 0.00062
print(distanceMiles)