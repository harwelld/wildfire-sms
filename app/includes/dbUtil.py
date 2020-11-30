import psycopg2
from psycopg2.extras import RealDictCursor
from app import app

def getDBConnection():
    """Returns PostgreSQL connection or None if failure to connect"""
    try:
        cnxn = psycopg2.connect(
            dbname = app.config['DB_NAME'],
            user = app.config['DB_USER'],
            password = app.config['DB_PASS'],
            host = app.config['DB_HOST'],
            port = app.config['DB_PORT']
        )
        print('PostgreSQL connection established')
        return cnxn
    except (Exception, psycopg2.Error) as e:
        print(f"Error connecting to PostgreSQL:  {str(e)}")
        return None


def executeSQL(sql, params, connection, fetchAllFlag=False, fetchOneFlag=False):
    """Executes paramaterized SQL with optional flags for return records"""
    try:
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute(sql, params)
        connection.commit()
        if fetchAllFlag:
            return cursor.fetchall()
        if fetchOneFlag:
            return cursor.fetchone()
    except (Exception, psycopg2.Error) as e:
        print (f"PostgreSQL error: {str(e)}")
        return None


if __name__ == '__main__':
    pass
    ##cnxn = getDBConnection()
    ##print(executeSQL('SELECT * FROM customer;', None, cnxn, fetchOneFlag=True))
