from sqlalchemy import create_engine
from datetime import timedelta
from dotenv import load_dotenv, dotenv_values
import datetime
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#load credentials for usage in engine
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

def dxpBetweenTwoDates(firstInsertedDate, SecondInsertedDate):
    
    #sql inserted date 1
    sql_dxpBetweenTwoDates_firstInsertedDate = str(f"SELECT player_name, experience FROM main_runescape_hiscores WHERE datesync_date = '{firstInsertedDate}' AND skill = 'Overall'")

    #sql inserted date 2
    sql_dxpBetweenTwoDates_secondInsertedDate = str(f"SELECT player_name, experience FROM main_runescape_hiscores WHERE datesync_date = '{SecondInsertedDate}' AND skill = 'Overall'")

    #df inserted date 1
    df_dxpBetweenTwoDates_firstInsertedDate = pd.read_sql(sql=sql_dxpBetweenTwoDates_firstInsertedDate, con=engine)

    #df inserted date 2
    df_dxpBetweenTwoDates_secondInsertedDate = pd.read_sql(sql=sql_dxpBetweenTwoDates_secondInsertedDate, con=engine)

    #merge both dataframes
    df_dxpBetweenTwoDates_merged = pd.merge(df_dxpBetweenTwoDates_firstInsertedDate, df_dxpBetweenTwoDates_secondInsertedDate, on='player_name', how='inner')

    #create new experience_gained column
    df_dxpBetweenTwoDates_merged['experience_gained'] = df_dxpBetweenTwoDates_merged['experience_y'] - df_dxpBetweenTwoDates_merged['experience_x']

    #create new dataframe, sorted by experience_gained, descending
    df_dxpBetweenTwoDates_sorted = df_dxpBetweenTwoDates_merged.sort_values(by='experience_gained', ascending=False)

    #create x and y value lists based on sorted dataframe
    x = df_dxpBetweenTwoDates_sorted['player_name'].head(10).tolist()
    y = df_dxpBetweenTwoDates_sorted['experience_gained'].head(10).tolist()

    #draw plot for experience gained
    fig, ax = plt.subplots(figsize=(12,6))

    #create axes to plot
    ax = plt.bar(x, y)

    #set x and y labels on plot
    plt.xlabel('Player Name')
    plt.ylabel('Experience Gained')

    #set title on plot
    plt.title(f"Experience gained between {firstInsertedDate} and {SecondInsertedDate}")

    #save plot as 'ExperienceGainedBetweenTwoDates
    fig.savefig('ExperienceGainedBetweenTwoDates.png')

    #check if dataframe contains data:
    if df_dxpBetweenTwoDates_sorted.empty:
        df_dxpBetweenTwoDates_sorted_checkContent = 0
    else:
        df_dxpBetweenTwoDates_sorted_checkContent = 1

    #return 1 after completeion to signal to Bot_primary that the image can be submitted to discord
    if df_dxpBetweenTwoDates_sorted_checkContent == 1:
        return ([1])
    elif df_dxpBetweenTwoDates_sorted_checkContent == 0:
        return ([0])