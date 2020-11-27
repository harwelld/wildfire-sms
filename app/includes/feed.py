import requests

url = 'https://inciweb.nwcg.gov/feeds/json/esri/'
incidents = requests.get(url).json()['markers']
ids = []

for incident in incidents:
    if incident['id'] not in ids:
        ids.append(incident['id'])

print(len(ids))
