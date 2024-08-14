from sqlalchemy import create_engine, inspect
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

table_presence_main_runescape_tracked_usernames = inspection.has_table("main_runescape_tracked_usernames")
table_presence_main_runescape_hiscores = inspection.has_table("main_runescape_hiscores")
table_presence_main_runescape_achievements = inspection.has_table("main_runesape_achievements")
table_presence_main_runescape_activities_imp = inspection.has_table("main_runescape_activities_imp")
table_presence_main_runescape_activities_processed = inspection.has_table("main_runescape_activities_processed")
table_presence_main_runescape_status = inspection.has_table("main_runescape_status")
table_presence_main_runescape_flagged_usernames = inspection.has_table("main_runescape_flagged_usernames")