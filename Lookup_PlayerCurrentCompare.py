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
engine = create_engine(f"{db_method_db}+{db_method_conn}://{db_user}:{db_password}@{db_hostname}:{db_port_id}/{db_database}")
    
#create function to compare player combat stats and quest progression
def compareCurrentPlayerStatus(insertedPlayerNameP1, insertedPlayerNameP2):

    #p1 sql query
    sql_compareCurrentPlayerStatus_p1 = str(f"SELECT combat_level, quests_completed, quests_started, quests_not_started FROM main_runescape_status WHERE player_name = '{insertedPlayerNameP1}' AND datesync_date = '{currentDate}'")

    #create DataFrame P1
    df_compareCurrentStatus_p1 = pd.read_sql(sql=sql_compareCurrentPlayerStatus_p1, con=engine)
    
    #p2 sql query
    sql_compareCurrentPlayerStatus_p2 = str(f"SELECT combat_level, quests_completed, quests_started, quests_not_started FROM main_runescape_status WHERE player_name = '{insertedPlayerNameP2}' AND datesync_date = '{currentDate}'")

    #create DataFrame P2
    df_compareCurrentStatus_p2 = pd.read_sql(sql=sql_compareCurrentPlayerStatus_p2, con=engine)

    #if either DataFrame is empty, return 0
    if df_compareCurrentStatus_p1.empty or df_compareCurrentStatus_p2.empty:

        return([0])
    
    #if both DataFrames not empty, return 1 and final DataFrame
    elif not df_compareCurrentStatus_p1.empty and not df_compareCurrentStatus_p2.empty:

        #p1 objects:
        combat_level_p1 = df_compareCurrentStatus_p1.iloc[0]['combat_level']
        quests_completed_p1 = df_compareCurrentStatus_p1.iloc[0]['quests_completed']
        quests_started_p1 = df_compareCurrentStatus_p1.iloc[0]['quests_started']
        quests_not_started_p1 = df_compareCurrentStatus_p1.iloc[0]['quests_not_started']

        #p2 objects:
        combat_level_p2 = df_compareCurrentStatus_p2.iloc[0]['combat_level']
        quests_completed_p2 = df_compareCurrentStatus_p2.iloc[0]['quests_completed']
        quests_started_p2 = df_compareCurrentStatus_p2.iloc[0]['quests_started']
        quests_not_started_p2 = df_compareCurrentStatus_p2.iloc[0]['quests_not_started']

        
        #create data for interim DataFrame
        df_data = [['Combat/level', combat_level_p1, combat_level_p2],
                   ['Quests completed', quests_completed_p1, quests_completed_p2],
                   ['Quests started', quests_started_p1, quests_started_p2],
                   ['Quests not started', quests_not_started_p1, quests_not_started_p2]]
        
        #create interim DataFrame
        df_compareCurrentStatus_interim = pd.DataFrame(df_data, columns=['Combat/Quests', insertedPlayerNameP1, insertedPlayerNameP2])

        #determine which player has higher, equal or lower level/score
        df_compareCurrentStatus_interim.loc[df_compareCurrentStatus_interim[insertedPlayerNameP1] < df_compareCurrentStatus_interim[insertedPlayerNameP2], 'Q'] = '<'
        df_compareCurrentStatus_interim.loc[df_compareCurrentStatus_interim[insertedPlayerNameP1] > df_compareCurrentStatus_interim[insertedPlayerNameP2], 'Q'] = '>'
        df_compareCurrentStatus_interim.loc[df_compareCurrentStatus_interim[insertedPlayerNameP1] == df_compareCurrentStatus_interim[insertedPlayerNameP2], 'Q'] = '='

        #create final dataframe
        df_compareCurrentStatus_Final = df_compareCurrentStatus_interim[['Combat/Quests', insertedPlayerNameP1, 'Q', insertedPlayerNameP2]]

        return([1], df_compareCurrentStatus_Final)
    
    #if unexpected error, return 2
    else:

        return([2])

#create function to compare player levels
def compareCurrentPlayerSkills(insertedPlayerNameP1, insertedPlayerNameP2):

    #p1 sql query
    sql_compareCurrentPlayerSkills_p1 = str(f"""SELECT skill AS "Skill", level, experience FROM main_runescape_hiscores WHERE player_name = '{insertedPlayerNameP1}' AND datesync_date = '{currentDate}'""")

    #p1 create DataFrame
    df_CompareCurrentPlayerSkills_p1 = pd.read_sql(sql=sql_compareCurrentPlayerSkills_p1, con=engine)

    #p2 sql query
    sql_compareCurrentPlayerSkills_p2 = str(f"""SELECT skill AS "Skill", level, experience FROM main_runescape_hiscores WHERE player_name = '{insertedPlayerNameP2}' AND datesync_date = '{currentDate}'""")

    #p2 create DataFrame
    df_CompareCurrentPlayerSkills_p2 = pd.read_sql(sql=sql_compareCurrentPlayerSkills_p2, con=engine)

    #if either DataFrame is empty, return 0
    if df_CompareCurrentPlayerSkills_p1.empty or df_CompareCurrentPlayerSkills_p2.empty:

        return([0])

    elif not df_CompareCurrentPlayerSkills_p1.empty and not df_CompareCurrentPlayerSkills_p2.empty:

        #merge dataframes
        df_CompareCurrentPlayerSkills_Merged = pd.merge(df_CompareCurrentPlayerSkills_p1, df_CompareCurrentPlayerSkills_p2, on='Skill', how='inner')

        #determine which player has higher, equal or lower level/score
        df_CompareCurrentPlayerSkills_Merged.loc[df_CompareCurrentPlayerSkills_Merged['experience_x'] < df_CompareCurrentPlayerSkills_Merged['experience_y'], 'Q'] = '<'
        df_CompareCurrentPlayerSkills_Merged.loc[df_CompareCurrentPlayerSkills_Merged['experience_x'] > df_CompareCurrentPlayerSkills_Merged['experience_y'], 'Q'] = '>'
        df_CompareCurrentPlayerSkills_Merged.loc[df_CompareCurrentPlayerSkills_Merged['experience_x'] == df_CompareCurrentPlayerSkills_Merged['experience_y'], 'Q'] = '='

        #create combined values for skill + experience for p1
        df_CompareCurrentPlayerSkills_Merged[insertedPlayerNameP1] = df_CompareCurrentPlayerSkills_Merged['level_x'].astype(str) + " (" + df_CompareCurrentPlayerSkills_Merged['experience_x'].astype(str) + ")"

        #create combined values for skill + experience for p2
        df_CompareCurrentPlayerSkills_Merged[insertedPlayerNameP2] = df_CompareCurrentPlayerSkills_Merged['level_y'].astype(str) + " (" + df_CompareCurrentPlayerSkills_Merged['experience_y'].astype(str) + ")"

        #create final DataFrame
        df_CompareCurrentPlayerSkills_Final = df_CompareCurrentPlayerSkills_Merged[['Skill', insertedPlayerNameP1, 'Q', insertedPlayerNameP2]]

        return(1, df_CompareCurrentPlayerSkills_Final)

    #if unexpected error occured, return 2
    else:

        return([2])

#create function to compare player activites
def compareCurrentPlayerActivities(insertedPlayerNameP1, insertedPlayerNameP2):

    #p1 sql query
    sql_compareCurrentPlayerActivities_p1 = str(f"""SELECT activity AS "Activity", score FROM main_runescape_achievements WHERE player_name = '{insertedPlayerNameP1}' AND datesync_date = '{currentDate}'""")

    #p1 DataFrame
    df_compareCurrentPlayerActivities_p1 = pd.read_sql(sql=sql_compareCurrentPlayerActivities_p1, con=engine)

    #p2 sql query
    sql_compareCurrentPlayerActivities_p2 = str(f"""SELECT activity AS "Activity", score FROM main_runescape_achievements WHERE player_name = '{insertedPlayerNameP2}' AND datesync_date = '{currentDate}'""")

    #p2 dDataFrame
    df_compareCurrentPlayerActivities_p2 = pd.read_sql(sql=sql_compareCurrentPlayerActivities_p2, con=engine)

    #if either DataFrame empty, return 0
    if df_compareCurrentPlayerActivities_p1.empty or df_compareCurrentPlayerActivities_p2.empty:
        
        return([0])

    #if both DataFrames not empty, return 1 and DataFrame
    elif not df_compareCurrentPlayerActivities_p1.empty and not df_compareCurrentPlayerActivities_p2.empty:

        #merge DataFrames
        df_compareCurrentPlayerActivities_merged = pd.merge(df_compareCurrentPlayerActivities_p1, df_compareCurrentPlayerActivities_p2, on='Activity', how='inner')

        #determine which player has higher, equal or lower level/score
        df_compareCurrentPlayerActivities_merged.loc[df_compareCurrentPlayerActivities_merged['score_x'] < df_compareCurrentPlayerActivities_merged['score_y'], 'Q'] = '<'
        df_compareCurrentPlayerActivities_merged.loc[df_compareCurrentPlayerActivities_merged['score_x'] > df_compareCurrentPlayerActivities_merged['score_y'], 'Q'] = '>'
        df_compareCurrentPlayerActivities_merged.loc[df_compareCurrentPlayerActivities_merged['score_x'] == df_compareCurrentPlayerActivities_merged['score_y'], 'Q'] = '='

        df_compareCurrentPlayerActivities_Final = df_compareCurrentPlayerActivities_merged[['Activity', 'score_x', 'Q', 'score_y']]

        return(1, df_compareCurrentPlayerActivities_Final)

    #if unexpected error, return 2
    else:

        return([2])

#create function to compare player achievements
def compareLast30daysPlayerAchievements(insertedPlayerNameP1, insertedPlayerNameP2):
    
    #create current date minus 30 days datestamp
    datePrior = str(currentDateNum - timedelta(days=30))

    #p1 sql query
    sql_compareLast30daysPlayerAchievements_p1 = str(f"SELECT * FROM main_runescape_activities_processed WHERE player_name = '{insertedPlayerNameP1}' AND event_date_numeric >= '{datePrior}' AND event_date_numeric <= '{currentDate}'")

    #p1 dataframe
    df_compareLast30daysPlayerAchievements_p1 = pd.read_sql(sql=sql_compareLast30daysPlayerAchievements_p1, con=engine)

    #p2 sql query
    sql_compareLast30daysPlayerAchievements_p2 = str(f"SELECT * FROM main_runescape_activities_processed WHERE player_name = '{insertedPlayerNameP2}' AND event_date_numeric >= '{datePrior}' AND event_date_numeric <= '{currentDate}'")

    #p2 dataframe
    df_compareLast30daysPlayerAchievements_p2 = pd.read_sql(sql=sql_compareLast30daysPlayerAchievements_p2, con=engine)

    #if either DataFrame empty, return 0
    if df_compareLast30daysPlayerAchievements_p1.empty or df_compareLast30daysPlayerAchievements_p2.empty:

        return([0])
    
    #if both DataFrames have content, return 1 and final DataFrame
    elif not df_compareLast30daysPlayerAchievements_p1.empty and not df_compareLast30daysPlayerAchievements_p2.empty:

        #p1 count achievements
        achievements_p1 = str(len(df_compareLast30daysPlayerAchievements_p1))

        #p2 count achievements
        achievements_p2 = str(len(df_compareLast30daysPlayerAchievements_p2))

        #creating data for final DataFrame
        df_data = [[insertedPlayerNameP1, achievements_p1],
                   [insertedPlayerNameP2, achievements_p2]]
        
        #final DataFrame
        df_compareAchievements_Final = pd.DataFrame(df_data, columns=['Player Name', 'Number of Achievements in last 30 days'])

        return(1, df_compareAchievements_Final)

    #if unexpected error, return 2
    else:

        return([2])
