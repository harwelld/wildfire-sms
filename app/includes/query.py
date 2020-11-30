from app.includes.dbUtil import getDBConnection, executeSQL


def registerNewCustomer(customer):
    """Register a new customer in the database"""
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
    """Returns all customer data and location as json object"""
    sql = """SELECT user_name, '(XXX)XXX-' || RIGHT(user_phone, 4) as userphone, """
    sql +="""user_distance, ST_Y(geom) as longitude, ST_X(geom) as latitude, modified """
    sql +="""FROM customer;"""
    customers = executeSQL(sql, None, getDBConnection(), fetchAllFlag=True)
    return customers


def insertFireData(incident):
    """Inserts new fire records as the data feed is parsed"""
    sql = 'CALL public.insertnewfire(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'
    params = (
        str(incident['name']),
        str(incident['type']),
        str(incident['summary']),
        str(incident['state']),
        str(incident['updated']),
        str(incident['size']),
        str(incident['url']),
        str(incident['id']),
        str(incident['contained']),
        float(incident['lng']),
        float(incident['lat'])
    )
    executeSQL(sql, params, getDBConnection())
    

def getIncidents():
    """Returns all incident data and location as json object"""
    sql = """SELECT inc_name, inc_type, ST_Y(geom) as longitude, ST_X(geom) as latitude """
    sql +="""FROM inciweb;"""
    incidents = executeSQL(sql, None, getDBConnection(), fetchAllFlag=True)
    return incidents


if __name__ == '__main__':
    pass
    # print(getIncidents())
    # customer = {'username': 'Dyl', 'phone': '845899', 'distance': '5', 'latitude': '46.5966414', 'longitude': '-132.66838'}
    # registerNewCustomer(customer)
    # print(getCustomers())
    #fire = {"name":"Cameron Peak Fire","type":"Wildfire","summary":"The Southern Area Gold Type 2 Incident Management Team assumed...","state":"COLORADO","updated":"2020-11-29 20:21:28","lat":"40.609","lng":"-105.879","size":"208,913 Acres","url":"/incident/6964/","id":"6964","contained":"94"}
    #insertFireData(fire)
