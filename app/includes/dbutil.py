# -----------------------------------------------------------------------------
# Name:        dbutil.py
#
# Purpose:     Database helper functions
#
# Author:      Dylan Harwell - UW Madison
#
# Created:     12/01/2020
# -----------------------------------------------------------------------------

import psycopg2
from psycopg2.extras import RealDictCursor
from os import getenv
from dotenv import find_dotenv, load_dotenv
from app import app


def getDBConnection(useDotEnvFlag=False):
    """
    Returns PostgreSQL connection or None if failure to connect
    If using useDotEnvFlag, the calling module must load_dotenv()
    """
    try:
        cnxn = psycopg2.connect(
            dbname = getenv('DB_NAME') if useDotEnvFlag else app.config['DB_NAME'],
            user = getenv('DB_USER') if useDotEnvFlag else app.config['DB_USER'],
            password = getenv('DB_PASS') if useDotEnvFlag else app.config['DB_PASS'],
            host =  getenv('DB_HOST') if useDotEnvFlag else app.config['DB_HOST'],
            port = getenv('DB_PORT') if useDotEnvFlag else app.config['DB_PORT']
        )
        print('PostgreSQL connection established')
        return cnxn
    except (Exception, psycopg2.Error) as e:
        print(f"Error connecting to PostgreSQL:  {str(e)}")
        return None


def executeSQL(sql, params, connection, fetchAllFlag=False):
    """Executes paramaterized SQL with optional flag for return records"""
    try:
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute(sql, params)
        connection.commit()
        if fetchAllFlag:
            return cursor.fetchall()
    except (Exception, psycopg2.Error) as e:
        print (f"PostgreSQL error: {str(e)}")
        return None
    finally:
        connection.close()
        print('PostgreSQL connection closed')


###############################################################################
###############################################################################
if __name__ == '__main__':
    pass
