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
-  Allows admins to manage the bot through the Discord chat (add/remove tracking for players, add/remove new admins).

REQUIREMENTS
-  This bot requires a database to be set up locally, and several tables within said database. Table requirements will be added at a later stage.

RECENTLY ADDED

[2024-08-10] Added user input validation check on all commands in Bot_primary that require Discord usernames or RuneScape usernames as manual input.

[2024-08-10] Overall exp tracking over X time for all player for DXP events. Returns graph when invoked.

[2024-08-10] Added commandInputChecker to verify user input when invoking command. Currently supports checking the date format, and order of dates if two dates need to be provided.

[2024-08-09] Capture usernames that have no profile when requesting date from public APIs. These usernames are stored in main_runescape_flagged_usernames.

FUTURE IMPLEMENTATIONS
1, Super Admin functions:
-  Modify Global Admin settings (discord_username).

2, Super Admin and Global Admin functions:
-  Modify Admin settings (discord_username).

3, Admin funcions (add/remove/modify players to tracked lists);
-  Modify tracked username in main_runescape_tracked_usernames.
-  Modify historical records tracked, based on main_tracked_usernames.

4, Add function for admins to retrieve list of main_runescape_flagged_usernames.