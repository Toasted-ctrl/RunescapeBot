import re

def checkInputDate(insertedDate):
    
    if re.match('^[0-9]{4}-[0-1]{1}[0-9]{1}-[0-3]{1}[0-9]{1}$', insertedDate):
        insertedDate_checkFormat = 1
    else:
        insertedDate_checkFormat = 0

    return (insertedDate_checkFormat)

def checkDateOrder(firstInsertedDate, secondInsertedDate):

    if firstInsertedDate < secondInsertedDate:
        dateStatus = 1
        firstDate = firstInsertedDate
        secondDate = secondInsertedDate

    elif firstInsertedDate > secondInsertedDate:
        dateStatus = 2
        firstDate = secondInsertedDate
        secondDate = firstInsertedDate

    elif firstInsertedDate == secondInsertedDate:
        dateStatus = 0
        firstDate = firstInsertedDate
        secondDate = secondInsertedDate

    return (dateStatus, firstDate, secondDate)
