# -----------------------------------------------------------------------------
# Name:        utils.py
#
# Purpose:     Helper functions
#
# Author:      Dylan Harwell - UW Madison
#
# Created:     12/01/2020
# -----------------------------------------------------------------------------

import time
from app.includes.dbaccessor import getAllCustomers

def getTime():
    """Fetches current date and time for logging"""
    date_time = time.strftime('%Y%m%d') + '_' + time.strftime('%H%M%S')
    return date_time


def logger(log_path, log_message):
    """Opens and appends a message to a specified log file"""
    with open(log_path, 'a') as log:
        log.write(log_message + '\n')


def isFieldUnique(value, fieldName):
    customers = getAllCustomers(hidePhoneNumber=False)
    values = [customer[fieldName] for customer in customers]
    if value not in values:
        return True
    else:
        return False


###############################################################################
###############################################################################
if __name__ == '__main__':
    pass
