import json
import requests
from os import getenv, path
from twilio.rest import Client
from dotenv import load_dotenv
from app.includes.utils import *
from app.includes.dbaccessor import *


def main():
    """
    Scans the InciWeb data feed to identify new incidents and insert them
    into the database. For each new incident, determines if the incident is
    within any customer's notification range. If an incident is within a
    customer's notification range, the Twilio API will send them a notification.
    For the prototype phase of the application, this script is designed to be
    run as a scheduled task (every 15 minutes?).

    TODO: Include in the Flask server, run on timer in a non-blocking way
    """
    load_dotenv()
    account_sid = getenv('TWILIO_ACCOUNT_SID')
    auth_token = getenv('TWILIO_AUTH_TOKEN')
    client = Client(account_sid, auth_token)

    url = 'https://inciweb.nwcg.gov/feeds/json/esri/'
    incidentsFromFeed = requests.get(url).json()['markers']

    logsDir = 'C:\\Users\\Dylan\\wildfire-sms\\logs'
    logName = 'scanFeed.log'
    logFile = path.join(logsDir, logName)
    logMessage = f"Scanning feed: {getTime()}"
    logger(logFile, logMessage)
    
    # Compare data in feed to incidents in databse and identify new incidents
    newIncidents = findNewIncidents(incidentsFromFeed, getIncidentsIdsFromDB())

    if newIncidents:
        logMessage = f"{len(newIncidents)} new incident(s) found"
        logger(logFile, logMessage)
        print(logMessage)

        # Retrieve all customer data with phone numbers
        customers = getAllCustomers(hidePhoneNumber=False, useDotEnvFlag=True)
        
        # Insert new incidents into database
        insertResult = addNewIncidents(newIncidents)
        added = insertResult[0]

        # Parse inserted incidents
        for incident in added:
            logMessage = f"Inserted incident {incident['id']} into database"
            logger(logFile, logMessage)
            print(logMessage)

            incLat = incident['lat']
            incLng = incident['lng']

            # Parse customers and calculate distance from new incident
            for customer in customers:
                custLat = str(customer['latitude'])
                custLng = str(customer['longitude'])
                custDist = customer['user_distance']
                distanceMiles = distanceBetweenPointsInMiles(incLng, incLat, custLng, custLat, useDotEnvFlag=True)

                # Check if incident is within customer's notification distance
                if distanceMiles <= custDist:
                    logMessage = f"{customer['user_name']} is {str(distanceMiles)} miles from incident {incident['id']}"
                    logger(logFile, logMessage)
                    print(logMessage)

                    # Notify user of incident with sms
                    cust_phone = customer['user_phone']
                    smsResult = notifyCustomer(incident, distanceMiles, cust_phone)

                    if smsResult['error']:
                        logMessage = f"An error occured sending notification to user: {customer['user_name']}, incident id: {incident['id']}"
                        logger(logFile, logMessage)
                        print(logMessage)
                        print(smsResult['exception'])

                    else:
                        logMessage = f"Notification sent to user: {customer['user_name']}, message sid: {smsResult['msg_sid']}"
                        logger(logFile, logMessage)
                        print(logMessage)

                        # Caputure sms history and insert into database
                        smsHistory = {}
                        smsHistory['feed_id'] = incident['id']
                        smsHistory['cust_id'] = customer['user_id']
                        smsHistory['distance'] = distanceMiles
                        smsHistory['msg_sid'] = smsResult['msg_sid']
                        try:
                            insertSmsHistoryRecord(smsHistory, useDotEnvFlag=True)
                            logMessage = 'Sms history record inserted'
                            logger(logFile, logMessage)
                            print(logMessage)
                        except Exception as e:
                            logMessage = f"Failed to insert sms history record: {str(e)}"
                            logger(logFile, logMessage)
                            print(logMessage)
                            continue

        # Check for any new incidents that failed to be inserted into database          
        failed = insertResult[1]
        if failed:
            for incident in failed:
                logMessage = f"Failed to insert new incident {incident['id']} into database"
                logger(logFile, logMessage)
                print(logMessage)

        logMessage = 'Finished processing new incidents\n'
        logger(logFile, logMessage)
        print(logMessage)

    else:
        logMessage = 'No new incidents found\n'
        logger(logFile, logMessage)
        print(logMessage)


###############################################################################
# Feed Scanner Helper Functions
###############################################################################

def getIncidentsIdsFromDB():
    """Get a list of all incident ids currenty in database"""
    idsFromDB = []
    for row in getAllIncidentIds(useDotEnvFlag=True):
        row = json.loads(json.dumps(row))
        for r in row:
            if row[r] not in idsFromDB:
                idsFromDB.append(row[r])
    return idsFromDB


def findNewIncidents(incidentsFromFeed, idsFromDB):
    """Check for new incidents in feed that are not in database"""
    newIncidents = []
    for row in incidentsFromFeed:
        if row['id'] not in idsFromDB:
            newIncidents.append(row)
    return newIncidents


def addNewIncidents(newIncidents):
    """Insert new incidents into database"""
    added = []
    failed = []
    for incident in newIncidents:
        try:
            insertIncidentRecord(incident, useDotEnvFlag=True)
            added.append(incident)
        except:
            failed.append()
            continue
    return (added, failed)


def notifyCustomer(incident, distance, customerPhone):
    smsResult = {'error': None, 'exception': None}
    try:
        message = client.messages \
            .create(
                body=f"Wildfire-sms: {incident['name']} approximately {distance} miles from your location. " \
                     f"For more information, please visit https://inciweb.nwcg.gov{incident['url']}",
                from_=getenv('TWILIO_PHONE_NUMBER'),
                to=f"+1{customerPhone}"
            )
        smsResult['msg_sid'] = message.sid
        smsResult['status'] = message.status
    except Exception as e:
        smsResult['error'] = -1
        smsResult['exception'] = str(e)
    return smsResult


###############################################################################
if __name__ == '__main__':
    main()
