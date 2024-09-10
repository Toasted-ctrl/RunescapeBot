import pandas as pd
import os
import datetime
from sqlalchemy import create_engine
from dotenv import load_dotenv, dotenv_values

#load redentials for usage in engine
load_dotenv()
db_database = os.getenv("db_database")
db_password = os.getenv("db_password")
db_port_id = os.getenv("db_port_id")
db_hostname = os.getenv("db_hostname")
db_user = os.getenv("db_user")
db_method_db = os.getenv("db_method_db")
db_method_conn = os.getenv("db_method_conn")

#create engine to retrieve data from DB
engine = create_engine(f"{db_method_db}+{db_method_conn}://{db_user}:{db_password}@{db_hostname}:{db_port_id}/{db_database}")

#create function to retrieve player current hiscore stats
def playerCurrentHiscores(insertedPlayerName, insertedDate):

    playerCurrentHiscores_date = str(insertedDate)

    #sql for DataFrame creation
    sql_playerCurrentHiscores = str(f"""SELECT skill AS "Skill", level AS "Level", experience AS "Experience" FROM main_runescape_hiscores WHERE player_name = '{insertedPlayerName}' AND datesync_date = '{playerCurrentHiscores_date}'""")

    #create DataFrame
    df_playerCurrentHiscores = pd.read_sql(sql=sql_playerCurrentHiscores, con=engine)

    #if DataFrame empty, return 0
    if df_playerCurrentHiscores.empty:

        return([0])
    
    #if DataFrame not empty, return 1 and DataFrame
    elif not df_playerCurrentHiscores.empty:

        return(1, df_playerCurrentHiscores)
    
    #if unexpected error occured, return 2
    else:

        return([2])

#create function to retrieve player current activities stats
def playerCurrentActivities(insertedPlayerName, insertedDate):

    playerCurrentActivities_date = str(insertedDate)

    #sql for DataFrame creation
    sql_playerCurrentActivities = str(f"""SELECT activity AS "Activity", rank AS "Rank", score AS "Score" FROM main_runescape_achievements WHERE player_name = '{insertedPlayerName}' AND datesync_date = '{playerCurrentActivities_date}'""")

    #create DataFrame
    df_playerCurrentActivities = pd.read_sql(sql=sql_playerCurrentActivities, con=engine)

    #if DataFrame empty, return 0
    if df_playerCurrentActivities.empty:

        return([0])

    #if DataFrame not empty, return 1 and DataFrame
    elif not df_playerCurrentActivities.empty:

        return(1, df_playerCurrentActivities)
    
    #if unexpected error, return 2
    else:

        return([2])

#create function to retrieve player current combat stats and quest progression
def playerCurrentStatus(insertedPlayerName, insertedDate):

    playerCurrentStatus_date = str(insertedDate)
    
    #sql query for DataFrame creation
    sql_playerCurrentStatus = str(f"SELECT combat_level, quests_completed, quests_started, quests_not_started FROM main_runescape_status WHERE player_name = '{insertedPlayerName}' AND datesync_date = '{playerCurrentStatus_date}'")

    #create DataFrame
    df_playerCurrentStatus = pd.read_sql(sql=sql_playerCurrentStatus, con=engine)

    #if DataFrame empty, return 0
    if df_playerCurrentStatus.empty:

        return([0])
    
    #if DataFrame not empty, create new DataFrame and return 1 and final DataFrame
    elif not df_playerCurrentStatus.empty:

        combatLevel = df_playerCurrentStatus.iloc[0]['combat_level']
        quests_completed = df_playerCurrentStatus.iloc[0]['quests_completed']
        quests_started = df_playerCurrentStatus.iloc[0]['quests_started']
        quests_not_started = df_playerCurrentStatus.iloc[0]['quests_not_started']

        df_data = [['Combat level', combatLevel], ['Quests completed', quests_completed], ['Quests started', quests_started], ['Quests not started', quests_not_started]]

        df_playerCurrentStatus_Final = pd.DataFrame(df_data, columns=['Combat/Quests', 'Level/Score'])

        return(1, df_playerCurrentStatus_Final)

    #if unexpected error, return 2
    else:

        return([2])

#create function to retrieve player last achievements
def playerLastAchievements(insertedPlayerName, insertedDate):

    playerLastAchievements_date = str(insertedDate)

    #sql query for DataFrame creation
    sql_playerLastAchievements = str(f"""SELECT event_date AS "Event Date", event_text AS "Event Text" FROM main_runescape_activities_processed WHERE player_name = '{insertedPlayerName}' ORDER BY "event_datetime_numeric" DESC LIMIT 5""")

    #create DataFrame
    df_playerLastAchievements = pd.read_sql(sql=sql_playerLastAchievements, con=engine)

    #if DataFrame empty, return 0
    if df_playerLastAchievements.empty:

        return([0])
    
    #if DataFrame not empty, return 1 and DataFrame
    elif not df_playerLastAchievements.empty:

        return(1, df_playerLastAchievements)
    
    #if unexpected error, return 2
    else:

        return([2])