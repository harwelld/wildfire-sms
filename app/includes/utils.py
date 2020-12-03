import time

def getTime():
    """Fetches current date and time for logging"""
    date_time = time.strftime('%Y%m%d') + '_' + time.strftime('%H%M%S')
    return date_time


def logger(log_path, log_message):
    """Opens and appends a message to a specified log file"""
    with open(log_path, 'a') as log:
        log.write(log_message + '\n')
