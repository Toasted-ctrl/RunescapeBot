

### REQUIRES MORE DEVELOPMENT, DO NOT USE ###


from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, BigInteger, Date
import os
from dotenv import dotenv_values, load_dotenv

load_dotenv()

db_database = os.getenv("db_database")
db_password = os.getenv("db_password")
db_port_id = os.getenv("db_port_id")
db_hostname = os.getenv("db_hostname")
db_user = os.getenv("db_user")
db_method_db = os.getenv("db_method_db")
db_method_conn = os.getenv("db_method_conn")

engine = create_engine(f"{db_method_db}+{db_method_conn}://{db_user}:{db_password}@{db_hostname}:{db_port_id}/{db_database}")

inspection = inspect(engine)

Base = declarative_base()

table_1_name = "main_runescape_tracked_usernames"
table_1_check = inspection.has_table(table_1_name)

if table_1_check == False:
    print(f"'{table_1_name}' = missing, attempting to create table.")

    class tracked_usernames(Base):
        __tablename__ = table_1_name
        player_name = Column(String(30), primary_key=True, nullable=False)
        count = Column(Integer, nullable=False)

    Base.metadata.create_all(engine)

table_2_name = "main_runescape_hiscores"
table_2_check = inspection.has_table(table_2_name)

if table_2_check == False:
    print(f"'{table_2_name}' = missing, attempting to create table.")

    class hiscores(Base):
        __tablename__ = table_2_name
        id = Column(BigInteger, primary_key=True, nullable=False)
        datesync_date = Column(Date, nullable=False)
        datesync_datetime = Column(String(30), nullable=False)
        player_name = Column(String(30), nullable=False)
        skill = Column(String(20), nullable=False)
        rank = Column(Integer)
        level = Column(Integer)
        experience = Column(BigInteger)

    Base.metadata.create_all(engine)

table_3_name = "main_runescape_achievements"
table_3_check = inspection.has_table(table_3_name)

if table_3_check == False:
    print(f"'{table_3_name}' = missing, attempting to create table.")

    class achievements(Base):
        __tablename__ = table_3_name
        id = Column(BigInteger, primary_key=True, nullable=False)
        datesync_date = Column(Date, nullable=False)
        datesync_datetime = Column(String(30), nullable=False)
        player_name = Column(String(30), nullable=False)
        activity = Column(String(40), nullable=False)
        rank = Column(Integer, nullable=False)
        score = Column(Integer, nullable=False)

    Base.metadata.create_all(engine)

table_4_name = "main_runescape_activities_imp"
table_4_check = inspection.has_table(table_4_name)

if table_4_check == False:
    print(f"'{table_4_name}' = missing, attempting to create table.")

    class activities_imp(Base):
        __tablename__ =  table_4_name
        datesync_date = Column(Date, nullable=False)
        datesync_datetime = Column(String(30), nullable=False)
        player_name = Column(String(30), primary_key=True, nullable=False)
        event_date = Column(String(30), primary_key=True, nullable=False)
        event_details = Column(String(150), nullable=False)
        event_text = Column(String(50), primary_key=True, nullable=False)

    Base.metadata.create_all(engine)

table_presence_main_runescape_activities_processed = inspection.has_table("main_runescape_activities_processed")

if table_presence_main_runescape_activities_processed == False:
    print("activities_processed = missing")

elif table_presence_main_runescape_activities_processed == True:
    print("activities_processed = present")

table_presence_main_runescape_status = inspection.has_table("main_runescape_status")

if table_presence_main_runescape_status == False:
    print("status = missing")

elif table_presence_main_runescape_status == True:
    print("status = present")

table_presence_main_runescape_flagged_usernames = inspection.has_table("main_runescape_flagged_usernames")

if table_presence_main_runescape_flagged_usernames == False:
    print("flagged_usernames = missing")

elif table_presence_main_runescape_flagged_usernames == True:
    print("flagged_usernames = present")