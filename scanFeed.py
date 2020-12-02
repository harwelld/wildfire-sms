import json
import sys
import requests
from os import getenv
from twilio.rest import Client
from dotenv import load_dotenv
from app.includes.dbaccessor import getIncidentIds, insertIncident, getDistanceBetweenPoints

load_dotenv()

account_sid = getenv('TWILIO_ACCOUNT_SID')
auth_token = getenv('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

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

message = client.messages \
    .create(
         body=f"This is a test from Dylan's wildfire-sms-notification-service! The {incident1['name']} incident is {distanceMiles:.2f} miles from your location. " \
              f"For more information about this incident, please visit https://inciweb.nwcg.gov{incident1['url']}",
         from_=getenv('TWILIO_PHONE_NUMBER'),
         to='+15056900343'
     )

print(message.sid)