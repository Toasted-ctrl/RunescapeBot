#!/usr/bin/python3

#importing module to create get requests to api
import requests

#importing module to create datetime timestamp
import datetime

#importing database connection module
import psycopg2

#importing os to use with dotenv
import os

#importing dotenv modules to load db credentials
from dotenv import load_dotenv, dotenv_values

#load dotenv file with db credentials
load_dotenv()

#list db credentials
db_database = os.getenv("db_database")
db_user = os.getenv("db_user")
db_password = os.getenv("db_password")
db_hostname = os.getenv("db_hostname")
db_port_id = os.getenv("db_port_id")

conn = None
cur = None

try:

    #connect to db
    conn = psycopg2.connect(
        database = db_database,
        user = db_user,
        password = db_password,
        host = db_hostname,
        port = db_port_id
    )

    #create cursor
    cursor = conn.cursor()

    #retrieve list of usernames that need to be looked up from db
    fetch_playerNames_query = "SELECT player_name FROM main_runescape_tracked_usernames"

    #execute query
    cursor.execute(fetch_playerNames_query)

    #list fetched playernames
    fetchedPlayerNames = cursor.fetchall()

    #close cursor and connection
    cursor.close()
    conn.close()

    #for loop for every fetchedPlayerName in list
    for fetchedPlayerName in fetchedPlayerNames:
        userName = fetchedPlayerName[0]

        #creating parameters for API get request
        playerName = userName
        paramPlayerName = {
            "user" : {playerName},
            "activities" : 20
        }

        #get request from API
        response = requests.get('https://apps.runescape.com/runemetrics/profile/profile?', params=paramPlayerName)
        
        print("------ API call details ------")
        print('\n')
        print(response.status_code)
        print("URL used for API call: " + response.url)

        #creating datetime timestamp
        current_date_timestamp = datetime.datetime.now()

        #creating datestamp
        current_date = datetime.date.today()

        #if error exists in response, attempt below
        if "error" in response.json():
            print("User does not have a profile.")
            print('\n')

            try:
                conn = psycopg2.connect(
                    host = db_hostname,
                    dbname = db_database,
                    user = db_user,
                    password = db_password,
                    port = db_port_id
                    )

                #create cursor in order to interact with db
                cur = conn.cursor()

                #create insert script and values to insert for quest and combat stats
                insert_script_flagged_username = 'INSERT INTO main_runescape_flagged_usernames (datesync_date, player_name, count) VALUES (%s, %s, %s)'
                insert_values_flagged_username = (current_date, userName, 1)
                cur.execute(insert_script_flagged_username, insert_values_flagged_username)

                #commit changes to main_runescape_status DB
                conn.commit()

            except Exception as error_3:
                print(error_3)

            finally:
                if cur is not None:
                    cur.close()
                if conn is not None:
                    conn.close()

        #if request.get does not result in 'error', attempt below
        else:

            try:

                #create quest progression objects using json response
                questsStarted = response.json()['questsstarted']
                questsComplete = response.json()['questscomplete']
                questsNotStarted = response.json()['questsnotstarted']

                #create combat stats objects using json response
                magicExp = response.json()['magic']
                meleeExp = response.json()['melee']
                rangedExp = response.json()['ranged']
                combatLevel = response.json()['combatlevel']

                #connect to DB
                conn = psycopg2.connect(
                    host = db_hostname,
                    dbname = db_database,
                    user = db_user,
                    password = db_password,
                    port = db_port_id
                )

                #create cursor in order to interact with db
                cur = conn.cursor()

                #create insert script and values to insert for quest and combat stats
                insert_script_playerStats = 'INSERT INTO main_runescape_status (datesync_date, datesync_datetime, player_name, combat_level, ranged_exp, magic_exp, melee_exp, quests_started, quests_completed, quests_not_started) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                insert_values_platerStats = (current_date, current_date_timestamp, userName, combatLevel, rangedExp, magicExp, meleeExp, questsStarted, questsComplete, questsNotStarted)
                cur.execute(insert_script_playerStats, insert_values_platerStats)

                #commit changes to main_runescape_status DB
                conn.commit()

                #api call returns 20 most recent achievments and event logs. Defining range and create for loop to cycle through these achievements
                for i in range(20):
                    mostRecentEvent_date = response.json()['activities'][i]['date']
                    mostRecentEvent_details = response.json()['activities'][i]['details']
                    mostRecentEvent_text = response.json()['activities'][i]['text']

                    #create insert script and values to insert for achievements and event logs
                    insert_script_playerActivites = 'INSERT INTO main_runescape_activities_imp (datesync_date, datesync_datetime, player_name, event_date, event_details, event_text) VALUES (%s, %s, %s, %s, %s, %s)'
                    insert_values_playerActivites = (current_date, current_date_timestamp, userName, mostRecentEvent_date, mostRecentEvent_details, mostRecentEvent_text)
                    cur.execute(insert_script_playerActivites, insert_values_playerActivites)

                    #commit changes to runescape_main_activities_imp
                    conn.commit()

            #printing error if anything within the try: function did not execute  
            except Exception as error_1:
                print(error_1)

            #creating finally functions to close the cursor and DB connection
            finally:
                if cur is not None:
                    cur.close()
                if conn is not None:
                    conn.close()
    
#printing error if anything within the try: function did not execute  
except Exception as error_2:
    print(error_2)

#creating finally functions to close the cursor and DB connection
finally:
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()