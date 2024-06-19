from sqlalchemy import create_engine
from datetime import timedelta
import datetime
import os
from dotenv import load_dotenv, dotenv_values
import pandas as pd

#load credentials for usage in engine
load_dotenv()
db_database = os.getenv("db_database")
db_password = os.getenv("db_password")
db_port_id = os.getenv("db_port_id")
db_hostname = os.getenv("db_hostname")
db_user = os.getenv("db_user")
db_method_db = os.getenv("db_method_db")
db_method_conn = os.getenv("db_method_conn")

#create currentDate datestamp, to allow filtering dataframes with today's date
currentDateNum = datetime.date.today()
currentDate = str(currentDateNum)

#create engine to retrieve data from DB
engine = create_engine(db_method_db + "+" + db_method_conn + "://" + db_user + ":" + db_password + "@" + db_hostname + ":" + db_port_id + "/" + db_database)

#create function to compare player combat stats and quest progression
def compareCurrentPlayerStatus(insertedPlayerNameP1, insertedPlayerNameP2):
    
    #retrieve data from DB
    df_retrieveCurrentStatus = pd.read_sql_table('main_runescape_status', engine)

    #create new dataframe for P1 > use .loc with with currentDate on datesync_date and insertedPlayerNameP1 on player_name
    df_currentStatusSorted_p1 = df_retrieveCurrentStatus.loc[(df_retrieveCurrentStatus['player_name'] == insertedPlayerNameP1) & (df_retrieveCurrentStatus['datesync_date'] == currentDate)]

    #create check value to verify presence of values in status dataframe for P1
    checkValueP1 = df_currentStatusSorted_p1.shape[0]
    if checkValueP1 > 0:
        checkValueP1_return = 1
    else:
        checkValueP1_return = 0

    #create new dataframe for P2 > use .loc with with currentDate on datesync_date and insertedPlayerNameP2 on player_name
    df_currentStatusSorted_p2 = df_retrieveCurrentStatus.loc[(df_retrieveCurrentStatus['player_name'] == insertedPlayerNameP2) & (df_retrieveCurrentStatus['datesync_date'] == currentDate)]

    #create check value to verify presence of values in status dataframe for P2
    checkValueP2 = df_currentStatusSorted_p2.shape[0]
    if checkValueP2 > 0:
        checkValueP2_return = 1
    else:
        checkValueP2_return = 0

    #if both check values return 1, fetch data from both dataframes
    if checkValueP1_return == 1 and checkValueP2_return == 1:

        #creating P1 stat opjects
        p1_combatLevel = str(df_currentStatusSorted_p1.iloc[0]['combat_level'])
        p1_questsCompleted = str(df_currentStatusSorted_p1.iloc[0]['quests_completed'])
        p1_questsStarted = str(df_currentStatusSorted_p1.iloc[0]['quests_started'])
        p1_questsNotStarted = str(df_currentStatusSorted_p1.iloc[0]['quests_not_started'])

        #creating P2 stat opjects
        p2_combatLevel = str(df_currentStatusSorted_p2.iloc[0]['combat_level'])
        p2_questsCompleted = str(df_currentStatusSorted_p2.iloc[0]['quests_completed'])
        p2_questsStarted = str(df_currentStatusSorted_p2.iloc[0]['quests_started'])
        p2_questsNotStarted = str(df_currentStatusSorted_p2.iloc[0]['quests_not_started'])

        return ([checkValueP1_return, checkValueP2_return],
                [p1_combatLevel, p1_questsCompleted, p1_questsStarted, p1_questsNotStarted], 
                [p2_combatLevel, p2_questsCompleted, p2_questsStarted, p2_questsNotStarted])
    
    #return else if either checkValueP1_return or checkValueP2_return, or both, are 0
    else:
        return ([checkValueP1_return, checkValueP2_return],  ##probaly need to adjust this later since now we're sending both values twice. Works for now though.
                [checkValueP1_return, checkValueP2_return])

#create function to compare player levels
def compareCurrentPlayerSkills(insertedPlayerNameP1, insertedPlayerNameP2):

    #retrieve data from DB
    df_retrieveCurrentSkills = pd.read_sql_table('main_runescape_hiscores', engine)

    #create new dataframe for P1 > use .loc with with currentDate on datesync_date and insertedPlayerNameP1 on player_name
    df_currentSkillSorted_p1 = df_retrieveCurrentSkills.loc[(df_retrieveCurrentSkills['player_name'] == insertedPlayerNameP1) & (df_retrieveCurrentSkills['datesync_date'] == currentDate)]

    #create new dataframe for P2 > use .loc with with currentDate on datesync_date and insertedPlayerNameP2 on player_name
    df_currentSkillSorted_p2 = df_retrieveCurrentSkills.loc[(df_retrieveCurrentSkills['player_name'] == insertedPlayerNameP2) & (df_retrieveCurrentSkills['datesync_date'] == currentDate)]

    #Merge tables on skill
    df_currentSkillMerged = pd.merge(df_currentSkillSorted_p1, df_currentSkillSorted_p2, on = 'skill', how='inner')

    #calculate experience_diff between players
    df_currentSkillMerged['experience_diff'] = df_currentSkillMerged['experience_x'] - df_currentSkillMerged['experience_y']

    #calculate level_diff between players
    df_currentSkillMerged['level_diff'] = df_currentSkillMerged['level_x'] - df_currentSkillMerged['level_y']

    #calculate rank_diff between players
    df_currentSkillMerged['rank_diff'] = df_currentSkillMerged['rank_x'] - df_currentSkillMerged['rank_y']

    #creating objects to insert into return statement
    entry_00_skill = str(df_currentSkillMerged.iloc[0]['skill'])
    entry_00_rank_P1 = str(df_currentSkillMerged.iloc[0]['rank_x'])
    entry_00_rank_P2 = str(df_currentSkillMerged.iloc[0]['rank_y'])
    entry_00_level_P1 = str(df_currentSkillMerged.iloc[0]['level_x'])
    entry_00_level_P2 = str(df_currentSkillMerged.iloc[0]['level_y'])
    entry_00_experience_P1 = str(df_currentSkillMerged.iloc[0]['experience_x'])
    entry_00_experience_P2 = str(df_currentSkillMerged.iloc[0]['experience_y'])
    entry_00_experience_diff = str(df_currentSkillMerged.iloc[0]['experience_diff'])

    entry_01_skill = str(df_currentSkillMerged.iloc[1]['skill'])
    entry_01_rank_P1 = str(df_currentSkillMerged.iloc[1]['rank_x'])
    entry_01_rank_P2 = str(df_currentSkillMerged.iloc[1]['rank_y'])
    entry_01_level_P1 = str(df_currentSkillMerged.iloc[1]['level_x'])
    entry_01_level_P2 = str(df_currentSkillMerged.iloc[1]['level_y'])
    entry_01_experience_P1 = str(df_currentSkillMerged.iloc[1]['experience_x'])
    entry_01_experience_P2 = str(df_currentSkillMerged.iloc[1]['experience_y'])
    entry_01_experience_diff = str(df_currentSkillMerged.iloc[1]['experience_diff'])

    return ([entry_00_skill, entry_00_rank_P1, entry_00_rank_P2, entry_00_level_P1, entry_00_level_P2, entry_00_experience_P1, entry_00_experience_P2, entry_00_experience_diff],
            [entry_01_skill, entry_01_rank_P1, entry_01_rank_P2, entry_01_level_P1, entry_01_level_P2, entry_01_experience_P1, entry_01_experience_P2, entry_01_experience_diff])

#create function to compare player activites
def compareCurrentPlayerActivities(insertedPlayerNameP1, insertedPlayerNameP2):

    #retrieve data from DB
    df_retrieveActivities = pd.read_sql_table('main_runescape_achievements', engine)

    #create new dataframe for P1 > use .loc with with currentDate on datesync_date and insertedPlayerNameP1 on player_name
    df_processedActivitiesP1 = df_retrieveActivities.loc[(df_retrieveActivities['player_name'] == insertedPlayerNameP1) & (df_retrieveActivities['datesync_date'] == currentDate)]

    #create new dataframe for P2 > use .loc with with currentDate on datesync_date and insertedPlayerNameP2 on player_name
    df_processedActivitiesP2 = df_retrieveActivities.loc[(df_retrieveActivities['player_name'] == insertedPlayerNameP2) & (df_retrieveActivities['datesync_date'] == currentDate)]

    #merge tables on activity
    df_currentActivitiesMerged = pd.merge(df_processedActivitiesP1, df_processedActivitiesP2, on='activity', how='inner')

    #calculate rank_diff between players
    df_currentActivitiesMerged['rank_diff'] = df_currentActivitiesMerged['rank_x'] - df_currentActivitiesMerged['rank_y']

    #calculate score_diff between players
    df_currentActivitiesMerged['score_diff'] = df_currentActivitiesMerged['score_x'] - df_currentActivitiesMerged['score_y']

    entry_00_activity = str(df_currentActivitiesMerged.iloc[0]['activity'])
    entry_00_rank_P1 = str(df_currentActivitiesMerged.iloc[0]['rank_x'])
    entry_00_rank_P2 = str(df_currentActivitiesMerged.iloc[0]['rank_y'])
    entry_00_score_P1 = str(df_currentActivitiesMerged.iloc[0]['score_x'])
    entry_00_score_P2 = str(df_currentActivitiesMerged.iloc[0]['score_y'])
    entry_00_score_diff = str(df_currentActivitiesMerged.iloc[0]['score_diff'])

    entry_01_activity = str(df_currentActivitiesMerged.iloc[1]['activity'])
    entry_01_rank_P1 = str(df_currentActivitiesMerged.iloc[1]['rank_x'])
    entry_01_rank_P2 = str(df_currentActivitiesMerged.iloc[1]['rank_y'])
    entry_01_score_P1 = str(df_currentActivitiesMerged.iloc[1]['score_x'])
    entry_01_score_P2 = str(df_currentActivitiesMerged.iloc[1]['score_y'])
    entry_01_score_diff = str(df_currentActivitiesMerged.iloc[1]['score_diff'])

    return([entry_00_activity, entry_00_rank_P1, entry_00_rank_P2, entry_00_score_P1, entry_00_score_P2, entry_00_score_diff], 
           [entry_01_activity, entry_01_rank_P1, entry_01_rank_P2, entry_01_score_P1, entry_01_score_P2, entry_01_score_diff])

#create function to compare player achievements
def compareLast30daysPlayerAchievements(insertedPlayerNameP1, insertedPlayerNameP2):
    
    #create current date minus 30 days datestamp
    datePrior = str(currentDateNum - timedelta(days=30))

    #retrieving data from DB
    df_retrieveLastAchievements = pd.read_sql_table('main_runescape_activities_processed', engine)

    #create new dataframe for P1 > use .loc with currentDate and datePrior on event_date_numeric, and .loc with insertedPlayerNameP1 on player_name
    df_lastAchievementsProcessedP1 = df_retrieveLastAchievements.loc[(df_retrieveLastAchievements['event_date_numeric'] >= datePrior) & (df_retrieveLastAchievements['event_date_numeric'] <= currentDate) & (df_retrieveLastAchievements['player_name'] == insertedPlayerNameP1)]

    #create string value for number of achievements for P1 in last 30 days
    player1NumberOfAchievements = str(df_lastAchievementsProcessedP1['activities_unique_id'].value_counts().shape[0])

    #create new dataframe for P2 > use .loc with currentDate and datePrior on event_date_numeric, and .loc with insertedPlayerNameP1 on player_name
    df_lastAchievementsProcessedP2 = df_retrieveLastAchievements.loc[(df_retrieveLastAchievements['event_date_numeric'] >= datePrior) & (df_retrieveLastAchievements['event_date_numeric'] <= currentDate) & (df_retrieveLastAchievements['player_name'] == insertedPlayerNameP2)]

    #create string value for number of achievements for P2 in last 30 days
    player2NumberOfAchievements = str(df_lastAchievementsProcessedP2['activities_unique_id'].value_counts().shape[0])

    return (player1NumberOfAchievements, player2NumberOfAchievements)