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
engine = create_engine(db_method_db + "+" + db_method_conn + "://" + db_user + ":" + db_password + "@" + db_hostname + ":" + db_port_id + "/" + db_database)

#create currentDate datestamp for later filtering of dataframes
currentDate = str(datetime.date.today())

#create function to retrieve player current hiscore stats
def playerCurrentHiscores(insertedPlayerName):

    #retrieve data from DB
    df_retrieve_playerCurrentHiscores = pd.read_sql_table('main_runescape_hiscores', engine)

    #create new dataframe by using .loc with insertedPlayerName on player_name and currentDate on datesync_date
    df_processed_playerCurrentHiscores = df_retrieve_playerCurrentHiscores.loc[(df_retrieve_playerCurrentHiscores['player_name'] == insertedPlayerName) & (df_retrieve_playerCurrentHiscores['datesync_date'] == currentDate)]

    skill_0 = df_processed_playerCurrentHiscores.iloc[0]['skill']
    rank_0 = df_processed_playerCurrentHiscores.iloc[0]['rank']
    level_0 = df_processed_playerCurrentHiscores.iloc[0]['level']
    experience_0 = df_processed_playerCurrentHiscores.iloc[0]['experience']

    skill_1 = df_processed_playerCurrentHiscores.iloc[1]['skill']
    rank_1 = df_processed_playerCurrentHiscores.iloc[1]['rank']
    level_1 = df_processed_playerCurrentHiscores.iloc[1]['level']
    experience_1 = df_processed_playerCurrentHiscores.iloc[1]['experience']

    #return values for when function is called from other program
    return(skill_0, rank_0, level_0, experience_0,
           skill_1, rank_1, level_1, experience_1)

#create function to retrieve player current activities stats
def playerCurrentActivities(insertedPlayerName):

    #retrieve data from DB
    df_retrieve_playerCurrentActivities = pd.read_sql_table('main_runescape_achievements', engine)

    #create new dataframe by using .loc with insertedPlayerName on player_name and currentDate on datesync_date
    df_processed_playerCurrentActivities = df_retrieve_playerCurrentActivities[(df_retrieve_playerCurrentActivities['player_name'] == insertedPlayerName) & (df_retrieve_playerCurrentActivities['datesync_date'] == currentDate)]

    activity_0 = df_processed_playerCurrentActivities.iloc[0]['activity']
    rank_0 = df_processed_playerCurrentActivities.iloc[0]['rank']
    score_0 = df_processed_playerCurrentActivities.iloc[0]['score']
    activity_1 = df_processed_playerCurrentActivities.iloc[1]['activity']
    rank_1 = df_processed_playerCurrentActivities.iloc[1]['rank']
    score_1 = df_processed_playerCurrentActivities.iloc[1]['score']
    activity_2 = df_processed_playerCurrentActivities.iloc[2]['activity']
    rank_2 = df_processed_playerCurrentActivities.iloc[2]['rank']
    score_2 = df_processed_playerCurrentActivities.iloc[2]['score']

    #return values for when function is called from other program
    return (activity_0, rank_0, score_0, 
            activity_1, rank_1, score_1, 
            activity_2, rank_2, score_2)

#create function to retrieve player current combat stats and quest progression
def playerCurrentStatus(insertedPlayerName):
    
    #retrieve data from DB
    df_retrieve_playerCurrentStatus = pd.read_sql_table('main_runescape_status', engine)

    #create new dataframe by using .loc with insertedPlayerName on player_name and currentDate on datesync_date
    df_processed_playerCurrentStatus = df_retrieve_playerCurrentStatus[(df_retrieve_playerCurrentStatus['player_name'] == insertedPlayerName) & (df_retrieve_playerCurrentStatus['datesync_date'] == currentDate)]

    checkValue = df_processed_playerCurrentStatus.shape[0]
    if checkValue > 0:
        checkValue_return = 1
    else:
        checkValue_return = 0

    #if checkValue is 1, retrieve all status stats from database
    if checkValue_return == 1:

        combatLevel = str(df_processed_playerCurrentStatus.iloc[0]['combat_level'])
        questsCompleted = str(df_processed_playerCurrentStatus.iloc[0]['quests_completed'])
        questsStarted = str(df_processed_playerCurrentStatus.iloc[0]['quests_started'])
        questsNotStarted = str(df_processed_playerCurrentStatus.iloc[0]['quests_not_started'])

        #return values for when function is called from other program
        return ([checkValue_return, checkValue_return],
                [combatLevel, questsCompleted, questsStarted, questsNotStarted])
    
    else: ##should probably have a closer look at this later since we're just sending the same value 4x (two tuples)
        return ([checkValue_return, checkValue_return],
                [checkValue_return, checkValue_return])

#create function to retrieve player last achievements
def playerLastAchievements(insertedPlayerName):

    #retrieve data from DB
    df_retrievePlayerLastFiveAchievements = pd.read_sql_table('main_runescape_activities_processed', engine)

    #create new dataframe by using .loc with insertedPlayerName on player_name and currentDate on datesync_date
    df_processedPlayerLastFiveAchievements = df_retrievePlayerLastFiveAchievements[(df_retrievePlayerLastFiveAchievements['player_name'] == insertedPlayerName)]

    eventDateTime_0 = df_processedPlayerLastFiveAchievements[['event_datetime_numeric', 'event_text']].sort_values('event_datetime_numeric', ascending=False).iloc[0]['event_datetime_numeric']
    eventText_0 = df_processedPlayerLastFiveAchievements[['event_datetime_numeric', 'event_text']].sort_values('event_datetime_numeric', ascending=False).iloc[0]['event_text']

    eventDateTime_1 = df_processedPlayerLastFiveAchievements[['event_datetime_numeric', 'event_text']].sort_values('event_datetime_numeric', ascending=False).iloc[1]['event_datetime_numeric']
    eventText_1 = df_processedPlayerLastFiveAchievements[['event_datetime_numeric', 'event_text']].sort_values('event_datetime_numeric', ascending=False).iloc[1]['event_text']

    eventDateTime_2 = df_processedPlayerLastFiveAchievements[['event_datetime_numeric', 'event_text']].sort_values('event_datetime_numeric', ascending=False).iloc[2]['event_datetime_numeric']
    eventText_2 = df_processedPlayerLastFiveAchievements[['event_datetime_numeric', 'event_text']].sort_values('event_datetime_numeric', ascending=False).iloc[2]['event_text']

    eventDateTime_3 = df_processedPlayerLastFiveAchievements[['event_datetime_numeric', 'event_text']].sort_values('event_datetime_numeric', ascending=False).iloc[3]['event_datetime_numeric']
    eventText_3 = df_processedPlayerLastFiveAchievements[['event_datetime_numeric', 'event_text']].sort_values('event_datetime_numeric', ascending=False).iloc[3]['event_text']
    
    eventDateTime_4 = df_processedPlayerLastFiveAchievements[['event_datetime_numeric', 'event_text']].sort_values('event_datetime_numeric', ascending=False).iloc[4]['event_datetime_numeric']
    eventText_4 = df_processedPlayerLastFiveAchievements[['event_datetime_numeric', 'event_text']].sort_values('event_datetime_numeric', ascending=False).iloc[4]['event_text']

    #return values for when function is called from other program
    return (eventDateTime_0, eventText_0, 
            eventDateTime_1, eventText_1, 
            eventDateTime_2, eventText_2, 
            eventDateTime_3, eventText_3, 
            eventDateTime_4, eventText_4)