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

#create currentDate datestamp for later filtering of dataframes
currentDate = str(datetime.date.today())

#create function to retrieve player current hiscore stats
def playerCurrentHiscores(insertedPlayerName):

    #sql for dataframe creation
    sql_playerCurrentHiscores = str(f"SELECT * FROM main_runescape_hiscores WHERE player_name = '{insertedPlayerName}' AND datesync_date = '{currentDate}'")

    #create dataframe
    df_playerCurrentHiscores = pd.read_sql(sql=sql_playerCurrentHiscores, con=engine)

    #objects to include in return
    skill_0 = df_playerCurrentHiscores.iloc[0]['skill']
    rank_0 = df_playerCurrentHiscores.iloc[0]['rank']
    level_0 = df_playerCurrentHiscores.iloc[0]['level']
    experience_0 = df_playerCurrentHiscores.iloc[0]['experience']

    skill_1 = df_playerCurrentHiscores.iloc[1]['skill']
    rank_1 = df_playerCurrentHiscores.iloc[1]['rank']
    level_1 = df_playerCurrentHiscores.iloc[1]['level']
    experience_1 = df_playerCurrentHiscores.iloc[1]['experience']

    #return values for when function is called from other program
    return(skill_0, rank_0, level_0, experience_0,
           skill_1, rank_1, level_1, experience_1)

#create function to retrieve player current activities stats
def playerCurrentActivities(insertedPlayerName):

    #sql for dataframe creation
    sql_playerCurrentActivities = str(f"SELECT * FROM main_runescape_achievements WHERE player_name = '{insertedPlayerName}' AND datesync_date = '{currentDate}'")

    #create dataframe
    df_playerCurrentActivities = pd.read_sql(sql=sql_playerCurrentActivities, con=engine)

    #objects to include in return
    activity_0 = df_playerCurrentActivities.iloc[0]['activity']
    rank_0 = df_playerCurrentActivities.iloc[0]['rank']
    score_0 = df_playerCurrentActivities.iloc[0]['score']
    activity_1 = df_playerCurrentActivities.iloc[1]['activity']
    rank_1 = df_playerCurrentActivities.iloc[1]['rank']
    score_1 = df_playerCurrentActivities.iloc[1]['score']
    activity_2 = df_playerCurrentActivities.iloc[2]['activity']
    rank_2 = df_playerCurrentActivities.iloc[2]['rank']
    score_2 = df_playerCurrentActivities.iloc[2]['score']

    #return values for when function is called from other program
    return (activity_0, rank_0, score_0, 
            activity_1, rank_1, score_1, 
            activity_2, rank_2, score_2)

#create function to retrieve player current combat stats and quest progression
def playerCurrentStatus(insertedPlayerName):
    
    #sql query
    sql_playerCurrentStatus = str(f"SELECT * FROM main_runescape_status WHERE player_name = '{insertedPlayerName}' AND datesync_date = '{currentDate}'")

    #create dataframe
    df_playerCurrentStatus = pd.read_sql(sql=sql_playerCurrentStatus, con=engine)

    if df_playerCurrentStatus.empty:
        df_playerCurrentStatus_checkContent = 0
    else:
        df_playerCurrentStatus_checkContent = 1

    #if checkValue is 1, retrieve all status stats from database
    if df_playerCurrentStatus_checkContent == 1:

        combatLevel = str(df_playerCurrentStatus.iloc[0]['combat_level'])
        questsCompleted = str(df_playerCurrentStatus.iloc[0]['quests_completed'])
        questsStarted = str(df_playerCurrentStatus.iloc[0]['quests_started'])
        questsNotStarted = str(df_playerCurrentStatus.iloc[0]['quests_not_started'])

        #return values for when function is called from other program
        #return ([df_playerCurrentStatus_checkContent, df_playerCurrentStatus_checkContent],
                #[combatLevel, questsCompleted, questsStarted, questsNotStarted])
    
        return ([df_playerCurrentStatus_checkContent, combatLevel, questsCompleted, questsStarted, questsNotStarted])
    
    else: ##should probably have a closer look at this later since we're just sending the same value 4x (two tuples)
        #return ([df_playerCurrentStatus_checkContent, df_playerCurrentStatus_checkContent],
                #[df_playerCurrentStatus_checkContent, df_playerCurrentStatus_checkContent])

        return ([df_playerCurrentStatus_checkContent])

#create function to retrieve player last achievements
def playerLastAchievements(insertedPlayerName):

    #sql query
    sql_playerLastAchievements = str(f"SELECT * FROM main_runescape_activities_processed WHERE player_name = '{insertedPlayerName}'")

    #create dataframe
    df_playerLastAchievements = pd.read_sql(sql=sql_playerLastAchievements, con=engine)

    eventDateTime_0 = df_playerLastAchievements[['event_datetime_numeric', 'event_text']].sort_values('event_datetime_numeric', ascending=False).iloc[0]['event_datetime_numeric']
    eventText_0 = df_playerLastAchievements[['event_datetime_numeric', 'event_text']].sort_values('event_datetime_numeric', ascending=False).iloc[0]['event_text']

    eventDateTime_1 = df_playerLastAchievements[['event_datetime_numeric', 'event_text']].sort_values('event_datetime_numeric', ascending=False).iloc[1]['event_datetime_numeric']
    eventText_1 = df_playerLastAchievements[['event_datetime_numeric', 'event_text']].sort_values('event_datetime_numeric', ascending=False).iloc[1]['event_text']

    eventDateTime_2 = df_playerLastAchievements[['event_datetime_numeric', 'event_text']].sort_values('event_datetime_numeric', ascending=False).iloc[2]['event_datetime_numeric']
    eventText_2 = df_playerLastAchievements[['event_datetime_numeric', 'event_text']].sort_values('event_datetime_numeric', ascending=False).iloc[2]['event_text']

    eventDateTime_3 = df_playerLastAchievements[['event_datetime_numeric', 'event_text']].sort_values('event_datetime_numeric', ascending=False).iloc[3]['event_datetime_numeric']
    eventText_3 = df_playerLastAchievements[['event_datetime_numeric', 'event_text']].sort_values('event_datetime_numeric', ascending=False).iloc[3]['event_text']
    
    eventDateTime_4 = df_playerLastAchievements[['event_datetime_numeric', 'event_text']].sort_values('event_datetime_numeric', ascending=False).iloc[4]['event_datetime_numeric']
    eventText_4 = df_playerLastAchievements[['event_datetime_numeric', 'event_text']].sort_values('event_datetime_numeric', ascending=False).iloc[4]['event_text']

    #return values for when function is called from other program
    return (eventDateTime_0, eventText_0, 
            eventDateTime_1, eventText_1, 
            eventDateTime_2, eventText_2, 
            eventDateTime_3, eventText_3, 
            eventDateTime_4, eventText_4)