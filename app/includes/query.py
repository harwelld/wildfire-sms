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
    sql = 'SELECT user_name, user_phone, user_distance, ' \
          'ST_Y(geom) as longitude, ST_X(geom) as latitude, modified ' \
          'FROM customer;'
    customers = executeSQL(sql, None, getDBConnection(), fetchAllFlag=True)
    return customers


def insertFireData(incident):
    """Inserts new fire records as the data feed is parsed"""
    sql = 'CALL public.insertnewfire(%s, %s, %s, %s, %s);'
    params = (
        incident['name'],
        incident['type'],
        incident['summary'],
        incident['state'],
        incident['updated'],
        incident['lat'],
        incident['lng'],
        incident['size'],
        incident['url'],
        incident['id'],
        incident['contained']
    )
    executeSQL(sql, params, getDBConnection())

if __name__ == '__main__':
    pass
    # customer = {'username': 'Dyl', 'phone': '845899', 'distance': '5', 'latitude': '46.5966414', 'longitude': '-132.66838'}
    # registerNewCustomer(customer)
    # print(getCustomers())
