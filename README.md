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

1, Super Admin and Global Admin functions:
-  Modify Admin setting (discord_username).

2, Admin funcions (add/remove/modify players to tracked lists);
-  Modify tracked username in main_runescape_tracked_usernames.
-  Modify historical records tracked, based on main_tracked_usernames.

3, Overall exp tracking over X time for all player for DXP events.

4, Retrieve user's admin status.

RECENTLY ADDED

1, Super Admin functions:
-  Add user as Global Admin to main_runescape_admin.
-  Remove user as Global Admin from main_runescape_admin.

2, Global Admin functions:
-  Add user as Admin to main_runescape_admin.
-  Remove user from main_runescape_admin.

3, Admin functions:
-  Add user to main_runescape_tracked_usernames (enables historical hiscore/stat/log tracking).
-  Remove user from main_runescape_tracked_usernames.