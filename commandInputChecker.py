import re

def checkInputDate(insertedDate):
    
    if re.match('^[0-9]{4}-[0-1]{1}[0-9]{1}-[0-3]{1}[0-9]{1}$', insertedDate):
        return (1)
    else:
        return (0)

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

def checkInputString(insertedString):

    char_list = ['@', '!', '[', ']', '{', '}', '(', ')', ',', '/', '?', '+', '&', '$', '#', ';', ':', '*']

    result = any(i in insertedString for i in char_list)

    if result == True:
        return(0)

    elif result == False:
        return(1)