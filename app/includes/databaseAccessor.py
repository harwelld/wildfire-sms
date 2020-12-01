import json
from app.includes.databaseUtility import getDBConnection, executeSQL


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


def getCustomers():
    """Returns all customer data and locations from customer table"""
    sql = """SELECT user_name, '(XXX)XXX-' || RIGHT(user_phone, 4) as userphone, """
    sql +="""user_distance, ST_Y(geom) as longitude, ST_X(geom) as latitude, modified """
    sql +="""FROM customer;"""
    customers = executeSQL(sql, None, getDBConnection(), fetchAllFlag=True)
    return customers


def insertIncident(incident, useDotEnvFlag=False):
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
    

def getIncidentIds(useDotEnvFlag=False):
    """Returns all incident ids from inciweb table"""
    sql = 'SELECT feed_id FROM inciweb;'
    incidents = executeSQL(sql, None, getDBConnection(useDotEnvFlag), fetchAllFlag=True)
    return incidents


def getDistanceBetweenPoints(lng1, lat1, lng2, lat2, useDotEnvFlag=False):
    sql = 'SELECT public.getdistancebetweenpoints(%s, %s, %s, %s);'
    params = (lng1, lat1, lng2, lat2)
    distance = executeSQL(sql, params, getDBConnection(useDotEnvFlag), fetchAllFlag=True)
    return distance


if __name__ == '__main__':
    pass
