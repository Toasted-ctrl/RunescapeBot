# RunescapeBot
Runescape bot that fetches and stores public API data, and makes it readable through a discord bot.

I've only just started to learn python, this is my first project!

I chose this as I am a somewhat active player myself, and primarily so I could learn:
-  Fetching data from APIs;
-  Setting up a database including tables;
-  Storing fetched API data into tables;
-  Where necessary, retrieve data from table, transform, and insert back into another table;
-  UPandas to create and manupulate dataframes;
-  Discord.py

FUTURE IMPLEMENTATIONS
-  Superadmin functions (add/remove/modify administrators);
  -  Add user to admin list is now added to admin.py. Command still needs to be added to Bot_primary to enable Discord;
  -  Remove user from admin list is now added to admin.py. Command still needs to be added to Bot_primary to enable Discord;
  -  Modify user not added yet

-  Admin funcions (add/remove/modify players to tracked lists);
  -  Add player to tracked list is now added to admin.py. Command still needs to be added to Bot_primary to enable Discord;
  -  Remove player from tracked list is now added to admin.py. Command still needs to be added to Bot_primary to enable Discord;
  -  Modify player not added yet;

-  Overall exp tracking over X time for all player for DXP events.

REQUIREMENTS
-  This bot requires a database to be set up locally, and several tables within said database. Table requirements will be added at a later stage.