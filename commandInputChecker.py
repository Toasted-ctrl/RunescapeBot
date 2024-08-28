import re
import os
import datetime
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv, dotenv_values

load_dotenv()

db_database = os.getenv("db_database")
db_password = os.getenv("db_password")
db_user = os.getenv("db_user")
db_hostname = os.getenv("db_hostname")
db_port_id = os.getenv("db_port_id")
db_method_db = os.getenv("db_method_db")
db_method_conn = os.getenv("db_method_conn")

engine = create_engine(f"{db_method_db}+{db_method_conn}://{db_user}:{db_password}@{db_hostname}:{db_port_id}/{db_database}")

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

    char_list = ['@', '!', '[', ']', '{', '}', '(', ')', ',', '/', '?', '&', '$', '#', ';', ':', '*', '_']

    result = any(i in insertedString for i in char_list)

    if result == True:
        return([0])

    elif result == False:

        returnString = insertedString.replace('+', ' ')

        return(1, returnString)

checkInputString
    
def checkDatabasePresence(insertedPlayerName):

    #create currentDate datestamp, to allow filtering dataframes with today's date
    currentDateNum = datetime.date.today()
    currentDate = str(currentDateNum)

    string_hiscores = str(f"SELECT * FROM main_runescape_hiscores WHERE player_name = '{insertedPlayerName}' AND datesync_date ='{currentDate}'")
    string_status = str(f"SELECT * FROM main_runescape_status WHERE player_name = '{insertedPlayerName}' AND datesync_date ='{currentDate}'")
    string_achievements = str(f"SELECT * FROM main_runescape_achievements WHERE player_name = '{insertedPlayerName}' AND datesync_date ='{currentDate}'")
    string_activities = str(f"SELECT * FROM main_runescape_activities_processed WHERE player_name = '{insertedPlayerName}'")

    df_hiscores = pd.read_sql(sql=string_hiscores, con=engine)
    df_status = pd.read_sql(sql=string_status, con=engine)
    df_achievements = pd.read_sql(sql=string_achievements, con=engine)
    df_activities = pd.read_sql(sql=string_activities, con=engine)

    if df_hiscores.empty:
        hiscores_present = 0
    else: 
        hiscores_present = 1

    if df_status.empty:
        status_present = 0
    else: 
        status_present = 1

    if df_achievements.empty:
        achievements_present = 0
    else: 
        achievements_present = 1

    if df_activities.empty:
        activities_present = 0
    else: 
        activities_present = 1

    return (hiscores_present, status_present, achievements_present, activities_present)