

### REQUIRES MORE DEVELOPMENT, DO NOT USE ###


from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
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

db_database_test = os.getenv("db_database_test")

engine = create_engine(f"{db_method_db}+{db_method_conn}://{db_user}:{db_password}@{db_hostname}:{db_port_id}/{db_database_test}")

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

table_presence_main_runescape_hiscores = inspection.has_table("main_runescape_hiscores")

if table_presence_main_runescape_hiscores == False:
    print("hiscores = missing")

elif table_presence_main_runescape_hiscores == True:
    print("hiscores = present")

table_presence_main_runescape_achievements = inspection.has_table("main_runescape_achievements")

if table_presence_main_runescape_achievements == False:
    print("achievements = missing")

elif table_presence_main_runescape_achievements == True:
    print("achievements = present")

table_presence_main_runescape_activities_imp = inspection.has_table("main_runescape_activities_imp")

if table_presence_main_runescape_activities_imp == False:
    print("activities_imp = missing")

elif table_presence_main_runescape_activities_imp == True:
    print("activities_imp = present")

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