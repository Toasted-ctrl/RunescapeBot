#importing psycopg2 for connection to and interaction with db
import psycopg2

#import os to be able to fetch .env file including db credentials
import os

#import dotenv modules to extract db credentials from .env file
from dotenv import load_dotenv, dotenv_values

#import create_engine from sqlalchemy in case a dataframe needs to be retrieved
from sqlalchemy import create_engine

#import pandas to create dataframe
import pandas as pd

#load dotenv file
load_dotenv()

#list db credentials
db_database = os.getenv("db_database")
db_user = os.getenv("db_user")
db_password = os.getenv("db_password")
db_hostname = os.getenv("db_hostname")
db_port_id = os.getenv("db_port_id")
db_method_db = os.getenv("db_method_db")
db_method_conn = os.getenv("db_method_conn")

engine = create_engine(f"{db_method_db}+{db_method_conn}://{db_user}:{db_password}@{db_hostname}:{db_port_id}/{db_database}")

conn = None
cursor = None

#creating function to retrieve admin rights for discord user
def retrieveAdminRights(insertedDiscordUsername):

    try:
        #connect to db
        conn = psycopg2.connect(
            database = db_database,
            user = db_user,
            password = db_password,
            host = db_hostname,
            port = db_port_id
        )

        #creating curos
        cursor = conn.cursor()

        #creating query to fetch access rights of user
        fetchQuery_discordUserAdminRights = "SELECT * FROM main_runescape_admin WHERE discord_username = %s"

        #executing query with provided discord user
        cursor.execute(fetchQuery_discordUserAdminRights, [insertedDiscordUsername])

        #fetching all admin rights related to discord user
        discordUserAdminRights = cursor.fetchone()

        #if retrieved list has no content, do below:
        if discordUserAdminRights == None:
            userHasAdminRights = 0
            admin_type = 0
            edit_admin = 0
            edit_admin_global = 0
            edit_admin_super = 0

        #if retrieved list has content, do below
        else:
            userHasAdminRights = 1
            admin_type = discordUserAdminRights[1]
            edit_admin = discordUserAdminRights[2]
            edit_admin_global = discordUserAdminRights[3]
            edit_admin_super = discordUserAdminRights[4]

        return (userHasAdminRights, admin_type, edit_admin, edit_admin_global, edit_admin_super)

    #create exception for if 'try' fails
    except Exception as error_1:
        print(error_1)

    #final code that needs to be executed at all time when the function is called
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

#function to check if player exists in tracked list
def checkPlayerExistsInTrackedList(insertedPlayerName):

    try:
        conn = psycopg2.connect(
            database = db_database,
            host = db_hostname,
            password = db_password,
            user = db_user,
            port = db_port_id
        )

        #creater cursor
        cursor = conn.cursor()

        #query to check if player_name exists in database
        fetchQuery_playerInTrackedList = "SELECT FROM main_runescape_tracked_usernames WHERE player_name = %s"

        #execute query
        cursor.execute(fetchQuery_playerInTrackedList, [insertedPlayerName])

        #fetch single line from DB
        playerInList = cursor.fetchone()

        #if query returns 0 rows, return 0, else return 1
        if playerInList == None:
            playerExistsInTracking = 0
        else:
            playerExistsInTracking = 1
        
        return (playerExistsInTracking)

    #throw exception error if 'try' failed
    except Exception as error_2:
        print(error_2)

    #always execute if parts of function fail
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

#function to add players to tracked list
def addPlayerToTrackedList(insertedPlayerName):

    try:
        #create db connection
        conn = psycopg2.connect(
            database = db_database,
            host = db_hostname,
            password = db_password,
            port = db_port_id,
            user = db_user
        )

        #create cursor
        cursor = conn.cursor()

        #create query for entering new player name in tracked_usernames
        addQuery_playerInTrackedList = "INSERT INTO main_runescape_tracked_usernames (player_name, count) VALUES (%s, 1)"

        #execute query
        cursor.execute(addQuery_playerInTrackedList, [insertedPlayerName])

        #commit change
        conn.commit()

    #throw exception if 'try' fails
    except Exception as error_3:
        print(error_3)

    #always execute:
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

def removePlayerFromTrackedList(insertedPlayerName):

    try:
        #create connection to db
        conn = psycopg2.connect(
            database = db_database,
            host = db_hostname,
            port = db_port_id,
            user = db_user,
            password = db_password
        )

        #create cursos
        cursor = conn.cursor()

        #create query to remove player name from db
        removeQuery_playerInTrackedList = "DELETE FROM main_runescape_tracked_usernames WHERE player_name = %s"

        #execute query
        cursor.execute(removeQuery_playerInTrackedList, [insertedPlayerName])

        #commit change
        conn.commit() 

    #throw error if 'try' fails
    except Exception as error_4:
        print(error_4)

    #execute at all times
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

#function for superadmin to add new admins
def addAdminToAdminList(insertedDiscordName):

    try:
        #create db connection
        conn = psycopg2.connect(
            database = db_database,
            host = db_hostname,
            port = db_port_id,
            password = db_password,
            user = db_user
        )

        #create cursor
        cursor = conn.cursor()

        #create query to add user as admin
        insertQuery_admin = "INSERT INTO main_runescape_admin (discord_username, admin_type, edit_admin, edit_admin_global, edit_admin_super) VALUES (%s, 'ADMIN', 1, 0, 0)"

        #execute query
        cursor.execute(insertQuery_admin, [insertedDiscordName])

        #commit changes
        conn.commit()
    
    #throw error if 'try' fails
    except Exception as error_5:
        print(error_5)

    #always execute
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()
    
#function where user can be removed as admin
def removeAdminFromAdminList(insertedDiscordName):

    try:
        #initiate db connection
        conn = psycopg2.connect(
            database = db_database,
            host = db_hostname,
            user = db_user,
            password = db_password,
            port = db_port_id
        )

        #create cursor
        cursor = conn.cursor()

        #query to remove admin
        removeQuery_admin = "DELETE FROM main_runescape_admin WHERE discord_username = %s"

        #execute query
        cursor.execute(removeQuery_admin, [insertedDiscordName])

        #commit changes
        conn.commit()

    #throw error if 'try' fails
    except Exception as error_6:
        print(error_6)

    #execute at all times
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

#function to add global admins
def addGlobalAdminToAdminList(insertedDiscordName):

    try:
        #initiate db connection
        conn = psycopg2.connect(
            database = db_database,
            host = db_hostname,
            password = db_password,
            user = db_user,
            port = db_port_id
        )

        #create cursor
        cursor = conn.cursor()

        #query to add global admin
        addQuery_adminGlobal = "INSERT INTO main_runescape_admin (discord_username, admin_type, edit_admin, edit_admin_global, edit_admin_super) VALUES (%s, 'GLOBAL ADMIN', 1, 1, 0)"

        #execute query
        cursor.execute(addQuery_adminGlobal, [insertedDiscordName])

        #commit changes
        conn.commit()

    #throw error if 'try' fails
    except Exception as error_7:
        print(error_7)

    #execute at all times
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

#function to remove global admin
def removeGlobalAdminFromAdminList(insertedDiscordName):

    try:
        #initiate db connection
        conn = psycopg2.connect(
            database = db_database,
            host = db_hostname,
            password = db_password,
            user = db_user,
            port = db_port_id
        )

        #create cursor
        cursor = conn.cursor()

        #query to remove global admin
        removeQuery_adminGlobal = "DELETE FROM main_runescape_admin WHERE discord_username = %s"

        #execute query
        cursor.execute(removeQuery_adminGlobal, [insertedDiscordName])

        #commit changes
        conn.commit()

    #throw error if 'try' fails
    except Exception as error_8:
        print(error_8)

    #execute at all times
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

#function to retrieve list of flagged users
def checkFlagged():

    #sql for retrieving dataframe
    sql_checkFlagged = str(f"SELECT * FROM main_runescape_flagged_usernames ORDER BY player_name")

    #create dataframe
    df_checkFlagged = pd.read_sql(sql=sql_checkFlagged, con=engine)

    #if dataframe is empty, return 0
    if df_checkFlagged.empty:
        
        return([0])

    #if dataframe is not empty, return number of flagged users and list of flagged users
    else:

        numberOfFlaggedUsers = int(len(df_checkFlagged['count']))
        flaggedUsers_list = df_checkFlagged['player_name'].tolist()

        return([numberOfFlaggedUsers], flaggedUsers_list)
    
#function to check if player exists in tracked list
def checkPlayerExistInFlaggedList(insertedPlayerName):

    try:
        conn = psycopg2.connect(
            database = db_database,
            host = db_hostname,
            password = db_password,
            user = db_user,
            port = db_port_id
        )

        #creater cursor
        cursor = conn.cursor()

        #query to check if player_name exists in database
        fetchQuery_playerInFlaggedList = "SELECT FROM main_runescape_flagged_usernames WHERE player_name = %s"

        #execute query
        cursor.execute(fetchQuery_playerInFlaggedList, [insertedPlayerName])

        #fetch single line from DB
        playerInList = cursor.fetchone()

        #if query returns 0 rows, return 0, else return 1
        if playerInList == None:
            playerExistsInFlagged = 0
        else:
            playerExistsInFlagged = 1
        
        return (playerExistsInFlagged)
    
    #throw exception error if 'try' failed
    except Exception as error_checkPlayerExistsInFlaggedList:
        print(error_checkPlayerExistsInFlaggedList)

    #always execute if parts of function fail
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

#function to check if player exists in tracked list
def checkPlayerExistInHiScores(insertedPlayerName):

    try:
        conn = psycopg2.connect(
            database = db_database,
            host = db_hostname,
            password = db_password,
            user = db_user,
            port = db_port_id
        )

        #creater cursor
        cursor = conn.cursor()

        #query to check if player_name exists in database
        fetchQuery_playerInHiscores = "SELECT FROM main_runescape_hiscores WHERE player_name = %s"

        #execute query
        cursor.execute(fetchQuery_playerInHiscores, [insertedPlayerName])

        #fetch single line from DB
        playerInList = cursor.fetchone()

        #if query returns 0 rows, return 0, else return 1
        if playerInList == None:
            playerExistsInHiscore = 0
        else:
            playerExistsInHiscore = 1
        
        return (playerExistsInHiscore)
    
    #throw exception error if 'try' failed
    except Exception as error_checkPlayerExistsInHiscore:
        print(error_checkPlayerExistsInHiscore)

    #always execute if parts of function fail
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

