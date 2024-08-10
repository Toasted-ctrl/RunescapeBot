# RunescapeBot
Runescape bot that fetches and stores public API data, and makes it readable through a discord bot.

I've only just started to learn python, this is my first project!

I chose this as I am a somewhat active player myself, and primarily so I could learn:
-  Fetching data from APIs;
-  Setting up a database including tables;
-  Storing fetched API data into tables;
-  Where necessary, retrieve data from table, transform, and insert back into another table;
-  Pandas to create and manupulate dataframes;
-  Setting up admin profiles and functions for specific users to make use of;
-  Discord.py.

REQUIREMENTS

-  This bot requires a database to be set up locally, and several tables within said database. Table requirements will be added at a later stage.

FUTURE IMPLEMENTATIONS

1, Super Admin functions:
-  Modify Global Admin settings (discord_username).

2, Super Admin and Global Admin functions:
-  Modify Admin settings (discord_username).

3, Admin funcions (add/remove/modify players to tracked lists);
-  Modify tracked username in main_runescape_tracked_usernames.
-  Modify historical records tracked, based on main_tracked_usernames.

4, Retrieve user's admin status.

5, For security reasons, Add user input checks when invoking commands that require usernames, to only allow input that do not have characters in them such as '%!()[]{},' etc.

6, Add function for admins to retrieve list of main_runescape_flagged_usernames.

RECENTLY ADDED

[2024-08-10] Overall exp tracking over X time for all player for DXP events. Returns graph when invoked.

[2024-08-10] Added commandInputChecker to verify user input when invoking command. Currently supports checking the date format, and order of dates if two dates need to be provided.

[2024-08-09] Capture usernames that have no profile when requesting date from public APIs. These usernames are stored in main_runescape_flagged_usernames.