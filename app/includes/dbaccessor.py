import json
from app.includes.dbutil import getDBConnection, executeSQL


###############################################################################
# Distance Calculation
###############################################################################

def distanceBetweenPointsInMiles(lng1, lat1, lng2, lat2, useDotEnvFlag=False):
    """Returns distance in miles between two coordinates in WGS84 geographic spatial reference"""
    sql = 'SELECT public.getdistancebetweenpoints(%s, %s, %s, %s);'
    params = (lng1, lat1, lng2, lat2)
    distanceResult = executeSQL(sql, params, getDBConnection(useDotEnvFlag), fetchAllFlag=True)
    for row in distanceResult:
        distanceMeters = row['getdistancebetweenpoints']
        distanceMiles = float(distanceMeters) * 0.00062
    return round(distanceMiles, 1)


###############################################################################
# Customer Table Operations
###############################################################################

def getAllCustomers(hidePhoneNumber=True, useDotEnvFlag=False):
    """Returns all customer data and locations from customer table"""
    if hidePhoneNumber:   
        sql = """SELECT user_id, user_name, '(XXX)XXX-' || RIGHT(user_phone, 4) as userphone, """
        sql +="""user_distance, ST_Y(geom) as latitude, ST_X(geom) as longitude, modified """
        sql +="""FROM customer;"""
    else:
        sql = """SELECT user_id, user_name, user_phone, """
        sql +="""user_distance, ST_Y(geom) as latitude, ST_X(geom) as longitude, modified """
        sql +="""FROM customer;"""
    customers = executeSQL(sql, None, getDBConnection(useDotEnvFlag), fetchAllFlag=True)
    return customers


def registerNewCustomer(customer):
    """Inserts a new customer in the customer table"""
    sql = 'CALL public.registernewcustomer(%s, %s, %s, %s, %s);'
    params = (
        customer['username'],
        customer['phone'],
        int(customer['distance']),
        float(customer['longitude']),
        float(customer['latitude'])
    )
    executeSQL(sql, params, getDBConnection())


###############################################################################
# Inciweb Table Operations
###############################################################################

def getAllIncidentIds(useDotEnvFlag=False):
    """Returns all incident ids from inciweb table"""
    sql = 'SELECT feed_id FROM inciweb;'
    incidents = executeSQL(sql, None, getDBConnection(useDotEnvFlag), fetchAllFlag=True)
    return incidents


def insertIncidentRecord(incident, useDotEnvFlag=False):
    """Inserts a new incident record into inciweb table"""
    sql = 'CALL public.insertnewincident(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'
    params = (
        str(incident['name']),
        str(incident['type']),
        str(incident['summary']),
        str(incident['state']),
        str(incident['updated']),
        float(incident['lat']),
        float(incident['lng']),
        str(incident['size']),
        str(incident['url']),
        str(incident['id']),
        str(incident['contained'])
    )
    executeSQL(sql, params, getDBConnection(useDotEnvFlag))


###############################################################################
# Sms History Table Operations
###############################################################################

def getAllSmsHistory(useDotEnvFlag=False):
    """Returns all sms history records"""
    sql = 'SELECT inc_id, cust_id, distance, msg_sid, modified FROM sms_history;'
    sms_history = executeSQL(sql, None, getDBConnection(useDotEnvFlag), fetchAllFlag=True)
    return sms_history


def insertSmsHistoryRecord(history, useDotEnvFlag=False):
    """Inserts a new history record into sms_history table"""
    sql = 'CALL public.insertnewhistory(%s, %s, %s, %s);'
    params = (
        int(history['feed_id']),
        int(history['cust_id']),
        float(history['distance']),
        str(history['msg_sid'])
    )
    executeSQL(sql, params, getDBConnection(useDotEnvFlag))



###############################################################################
if __name__ == '__main__':
    pass
