#importing psycopg2 for connection to and interaction with db
import psycopg2

#import os to be able to fetch .env file including db credentials
import os

#import dotenv modules to extract db credentials from .env file
from dotenv import load_dotenv, dotenv_values

#load dotenv file
load_dotenv()

#list db credentials
db_database = os.getenv("db_database")
db_user = os.getenv("db_user")
db_password = os.getenv("db_password")
db_hostname = os.getenv("db_hostname")
db_port_id = os.getenv("db_port_id")

conn = None
cursor = None

#creating function to retrieve admin rights for discord user
def retrieveAdminRights (insertedDiscordUsername):

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
            tracking_addPlayer = 0
            tracking_removePlayer = 0
            tracking_modifyPlayer = 0
            admin_addUser = 0
            admin_removeUser = 0
            admin_modifyUser = 0

        #if retrieved list has content, do below
        else:
            userHasAdminRights = 1
            tracking_addPlayer = discordUserAdminRights[1]
            tracking_removePlayer = discordUserAdminRights[2]
            tracking_modifyPlayer = discordUserAdminRights[3]
            admin_addUser = discordUserAdminRights[4]
            admin_removeUser = discordUserAdminRights[5]
            admin_modifyUser = discordUserAdminRights[6]

        return (userHasAdminRights, tracking_addPlayer, tracking_removePlayer, tracking_modifyPlayer, admin_addUser, admin_removeUser, admin_modifyUser)

    #create exception for if 'try' fails
    except Exception as error_1:
        print(error_1)

    #final code that needs to be executed at all time when the function is called
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()