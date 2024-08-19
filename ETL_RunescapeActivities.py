#!/usr/bin/python3

#import pandas to create dataframe
import pandas as pd

#importing sqlalchemy create_engine package to create engine and retrieve data from DB, as well as save dataframe to DB
from sqlalchemy import create_engine

#import datetime to print timestamp
import datetime

#import os to us dotenv
import os

#import dotenv to load db credentials
from dotenv import load_dotenv, dotenv_values

#creating datestamp to use for syncing only latest batch, and convert datestamp to string
currentDate = str(datetime.date.today())

#set credentials to be used in sqlalchemy engine
load_dotenv()
db_database = os.getenv("db_database")
db_password = os.getenv("db_password")
db_user = os.getenv("db_user")
db_hostname = os.getenv("db_hostname")
db_port_id = os.getenv("db_port_id")
db_method_db = os.getenv("db_method_db")
db_method_conn = os.getenv("db_method_conn")

#create engine to connect to db
engine = create_engine(db_method_db + "+" + db_method_conn + "://" + db_user + ":" + db_password + "@" + db_hostname + ":" + db_port_id + "/" + db_database)

#creating function to allow to be imported into other python programs
def runescape_activities_etl():

    #creating raw dataframe, retrieving data from DB using sqlalchemy engine
    df_raw = pd.read_sql_table('main_runescape_activities_imp', engine)

    #creating new columns 'day', 'month', 'year' and 'time' based on 'event_date'
    df_raw['event_date_time'] = df_raw['event_date'].str[12:17]
    df_raw['event_date_day'] = df_raw['event_date'].str[:2]
    df_raw['event_date_year'] = df_raw['event_date'].str[7:11]
    df_raw['event_date_month_text'] = df_raw['event_date'].str[3:6]

    #creating numeric value for event_date_month_text and insert into new column 'event_date_month_numeric'
    df_raw.loc[df_raw['event_date_month_text'].str.contains("Jan"), 'event_date_month_numeric'] = "01"
    df_raw.loc[df_raw['event_date_month_text'].str.contains("Feb"), 'event_date_month_numeric'] = "02"
    df_raw.loc[df_raw['event_date_month_text'].str.contains("Mar"), 'event_date_month_numeric'] = "03"
    df_raw.loc[df_raw['event_date_month_text'].str.contains("Apr"), 'event_date_month_numeric'] = "04"
    df_raw.loc[df_raw['event_date_month_text'].str.contains("May"), 'event_date_month_numeric'] = "05"
    df_raw.loc[df_raw['event_date_month_text'].str.contains("Jun"), 'event_date_month_numeric'] = "06"
    df_raw.loc[df_raw['event_date_month_text'].str.contains("Jul"), 'event_date_month_numeric'] = "07"
    df_raw.loc[df_raw['event_date_month_text'].str.contains("Aug"), 'event_date_month_numeric'] = "08"
    df_raw.loc[df_raw['event_date_month_text'].str.contains("Sep"), 'event_date_month_numeric'] = "09"
    df_raw.loc[df_raw['event_date_month_text'].str.contains("Oct"), 'event_date_month_numeric'] = "10"
    df_raw.loc[df_raw['event_date_month_text'].str.contains("Nov"), 'event_date_month_numeric'] = "11"
    df_raw.loc[df_raw['event_date_month_text'].str.contains("Dec"), 'event_date_month_numeric'] = "12"

    #creating new event_date_numeric column
    df_raw['event_date_numeric'] = df_raw.apply(lambda x: '%s-%s-%s' % (x['event_date_year'], x['event_date_month_numeric'], x['event_date_day']), axis=1)

    #creating new event_datetime_numeric column
    df_raw['event_datetime_numeric'] = df_raw.apply(lambda x: '%s-%s' % (x['event_date_numeric'], x['event_date_time']), axis=1)

    #creating new activities_unique_id column
    df_raw['activities_unique_id'] = df_raw.apply(lambda x: '%s-%s-%s' % (x['event_datetime_numeric'], x['event_text'], x['player_name']), axis=1)

    #retrieving only data from dataframe of which datsync date = currentDate. Dataframe will return as empty if no data was found for currentDate
    df_processed = df_raw.loc[(df_raw['datesync_date'] == currentDate)]

    #copy dataframe into main_runescape_activities, append rows if table already exists
    df_processed.to_sql('main_runescape_activities_processed', engine, if_exists='append')

    print(df_processed)

#run runescape_activities_etl
runescape_activities_etl()