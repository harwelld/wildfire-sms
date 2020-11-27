import psycopg2
from psycopg2.extras import RealDictCursor
from os import getenv
from dotenv import load_dotenv
load_dotenv()


def getDBConnection():
    """Returns PostgreSQL connection or None if failure to connect"""
    try:
        cnxn = psycopg2.connect(
            user = getenv('DB_USER'),
            password = getenv('DB_PASS'),
            host = getenv('BD_HOST'),
            port = getenv('DB_PORT'),
            database = getenv('DB_NAME')
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
    finally:
        if (connection):
            connection.close()
        if (cursor):
            cursor.close() 
        print("PostgreSQL connection closed")


if __name__ == '__main__':
    pass
    ##cnxn = getDBConnection()
    ##print(executeSQL('SELECT * FROM customer;', None, cnxn, fetchOneFlag=True))
