# Runescape Discord Bot
Discord bot that fetches and stores data from some of RuneScape's public APIs, and allows Discord users to interact with said data through through commands.

I've only just started to learn python, this is my very first project! It started with just requesting data from APIs, but gradually grew into something bigger.

I chose this as I am a somewhat active player myself, and primarily so I could learn:
-  Fetching data from APIs.
-  Setting up a database including tables.
-  Storing fetched API data into tables.
-  Use SQL to retrieve filtered data from database.
-  Where necessary, retrieve data from table, transform, and insert back into another table.
-  Pandas to create and manupulate dataframes.
-  Add restrictions to validate user input.
-  Setting up admin profiles and functions for specific users to make use of.
-  Discord.py.

FUNCTIONS
-  Allows users to lookup individual RuneScape player's stats (hiscores, recent achievements, activities, etc) if tracked.
-  Allows users to compare two individual RuneScape player's stats (hiscores, recent achievements, activities, etc) if tracked.
-  Allows users to request DXP challenge graphs, which outputs a graphs to Discord that compares all tracked players, based on two iput dates.
-  Allows admins to manage the bot through the Discord chat (add/remove/update tracking for players, add/remove new admins).

REQUIREMENTS
This bot requires PostgreSQL to be set up on the host machine. Run createDatabases.py once database is set up. Please also make sure to create a .env file that includes the following objects:
-  BOT_TOKEN --> include Discord bot token.
-  db_database --> include database name.
-  db_password --> include database password.
-  db_port_id --> include database port. Default port is "5432".
-  db_hostname --> include database hostname. Should by default be "localhost" if running locally.
-  db_user --> include database user.
-  db_method_db --> should be set to "postgresql".
-  db_method_conn --> should be set to "psycopg2".\
PLEASE ALSO MAKE SURE, IF ATTEMPTING TO RUN FROM A LINUX MACHINE, TO USE DOS2UNIX. FILE WILL OTHERWISE NOT EXECUTE AFTER USING CHMOD.

RECENTLY ADDED
[2024-08-28] Bugfix (KI001). Fixed issue where RuneScape usernames with spaces could not be accepted. Now if a name needs to be added/removed/searched for you can substitute a space with a '+'. The '+' is removed on the backend. This will ensure that two names can still be provided when two names are required for a command.

[2024-08-27] Bugfix (KI002). Fixed an issue where main.py would throw an error if user data was not present in at least one of the required tables for currentHiscore and pCurrentCompare, but would be present in returnStatus. Bot will now also reply in the Discord chat correctly, with missing data indication.

[2024-08-17] Added features to createDatabases.py. Running this scipt at the host machine will create all tables necessary. User must have set up PostgreSQL prior, see 'REQUIREMENTS' for more info.

[2024-08-13] Implemented updateTracking to allow admin to update records in case a user changed RuneScape usernames.

[2024-08-11] Allow admins to retrieve list of flagged_usernames.

[2024-08-10] Added user input validation check on all commands in Bot_primary that require Discord usernames or RuneScape usernames as manual input.

[2024-08-10] Overall exp tracking over X time for all player for DXP events. Returns graph when invoked.

[2024-08-10] Added commandInputChecker to verify user input when invoking command. Currently supports checking the date format, and order of dates if two dates need to be provided.

[2024-08-09] Capture usernames that have no profile when requesting date from public APIs. These usernames are stored in main_runescape_flagged_usernames.

KNOWN ISSUES

FUTURE IMPLEMENTATIONS
-  Update removeTracking to also remove username from flagged_usernames, if present.