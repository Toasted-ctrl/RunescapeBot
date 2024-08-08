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
def compareCurrentPlayerStatus_test(insertedPlayerNameP1, insertedPlayerNameP2):
    
    #retrieve data from DB
    df_retrieveCurrentStatus = pd.read_sql_table('main_runescape_status', engine)


    #p1 sql query
    sql_compareCurrentPlayerStatus_p1 = str("SELECT * FROM main_runescape_status WHERE player_name = '" + insertedPlayerNameP1 + "' AND datesync_date = '" + currentDate + "'")

    #p1 create dataframe
    df_CompareCurrentStatus_p1 = pd.read_sql(sql=sql_compareCurrentPlayerStatus_p1, con=engine)

    #p1 check if dataframe contains data
    if df_CompareCurrentStatus_p1.empty:
        df_CompareCurrentStatus_p1_checkContent = 0
    else:
        df_CompareCurrentStatus_p1_checkContent = 1
    
    #p2 sql query
    sql_compareCurrentPlayerStatus_p2 = str("SELECT * FROM main_runescape_status WHERE player_name = '" + insertedPlayerNameP2 + "' AND datesync_date = '" + currentDate + "'")

    #p2 create dataframe
    df_CompareCurrentStatus_p2 = pd.read_sql(sql=sql_compareCurrentPlayerStatus_p2, con=engine)

    #p2 check if dataframe contains data
    if df_CompareCurrentStatus_p2.empty:
        df_CompareCurrentStatus_p2_checkContent = 0
    else:
        df_CompareCurrentStatus_p2_checkContent = 1

    #return following if both dataframes (p1 and p2) contain data
    if df_CompareCurrentStatus_p1_checkContent == 1 and df_CompareCurrentStatus_p2_checkContent == 1:

        #creating objects for p1 and p2 data to include in return
        combatLevel_p1 = str(df_CompareCurrentStatus_p1.iloc[0]['combat_level'])
        combatLevel_p2 = str(df_CompareCurrentStatus_p2.iloc[0]['combat_level'])

        questsCompleted_p1 = str(df_CompareCurrentStatus_p1.iloc[0]['quests_completed'])
        questsCompleted_p2 = str(df_CompareCurrentStatus_p2.iloc[0]['quests_completed'])

        questsStarted_p1 = str(df_CompareCurrentStatus_p1.iloc[0]['quests_started'])
        questsStarted_p2 = str(df_CompareCurrentStatus_p2.iloc[0]['quests_started'])

        questsNotStarted_p1 = str(df_CompareCurrentStatus_p1.iloc[0]['quests_not_started'])
        questsNotStarted_p2 = str(df_CompareCurrentStatus_p2.iloc[0]['quests_not_started'])

        return ([df_CompareCurrentStatus_p1_checkContent, combatLevel_p1, questsCompleted_p1, questsStarted_p1, questsNotStarted_p1], 
                [df_CompareCurrentStatus_p2_checkContent, combatLevel_p2, questsCompleted_p2, questsStarted_p2, questsNotStarted_p2])

    else:
        return ([df_CompareCurrentStatus_p1_checkContent], 
                [df_CompareCurrentStatus_p2_checkContent])

result = compareCurrentPlayerStatus_test('Jake', 'CocoaToast')
print(format(result[0][0]))
print(format(result[1][0]))