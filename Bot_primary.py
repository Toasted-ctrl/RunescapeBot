import discord
import Lookup_PlayerCurrentStatus
import Lookup_PlayerCurrentCompare
import datetime
import os
from dotenv import load_dotenv, dotenv_values
from discord.ext import commands
from table2ascii import table2ascii as t2a, PresetStyle

###############################################################################################################
########## NEXT THING(S) TO BUILD: ############################################################################
########## 1 ADMIN FUNCTIONS FOR MANAGEMENT THROUGH DISCORD CHANNEL ###########################################
########## 2 FUNCTION TO RETRIEVE ALL TRACKED PLAYER CHANGES THROUGH X PERIOD, i.e., FOR DXP WEEKEND ##########
###############################################################################################################

###############################################################################################################
########## 1 ADMIN FUNCTION FOR MANAGEMENT THROUGH DISCORD CHANNEL ############################################
########## > SET UP NEW TABLE IN DB, ADD SUPERADMIN AND REGULAR ADMIN PERMISSION ##############################
########## >> SUPERADMIN TO BE ALLOWED TO ADD/REMOVE ADMINS, ADD/REMOVE TRACKED USERNAMES #####################
########## > ADMIN TO BE ALLOWED TO ADD/REMOVE TRACKED USERNAMES ##############################################
########## > CREATE NEW .PY FOR ALL ADMIN FUNCTIONS ###########################################################
########## >> INCLUDE CHECKS FOR PERMISSION LEVEL DEPENDING ON FUNCTION CALLED ################################
########## > ADD NEW COMMANDS TO BOT_PRIMARY TO CALL FUNCTION THROUGH DISCORD INTERACTION #####################
###############################################################################################################

#allow all intents for discord bot
intents = discord.Intents.all()
intents.message_content = True

#create timestamp for on_ready event
timestamp = datetime.datetime.now()

def run_discord_bot():
    #load dotend credentials
    load_dotenv()

    #fetch token from dotenv file
    TOKEN = os.getenv("BOT_TOKEN")
    bot = commands.Bot(command_prefix="!", intents=intents)

    #print that bot is ready in terminal
    @bot.event
    async def on_ready():
        print(f'[{timestamp}] {bot.user} is now running!')

    @bot.event
    async def on_message(message):

        await bot.process_commands(message)

        on_message_timestamp = datetime.datetime.now()
        user_message = message.content
        message_author = message.author
        message_channel = message.channel

        print(f"[{on_message_timestamp}] {message_author} said '{user_message}' (in channel: {message_channel})")
        if message.content == "Hello there":
            await message.channel.send("General Kenobi")
        if message.content == "Shut up!":
            await message.channel.send("No you shut up!")

    #currentHiscore command using playerName as variable
    @bot.command()
    async def currentHiscore(ctx, playerName):

        #!help information message
        """Answers with current status/hiscore of indicated player"""

        #create objects for usage in terminal event logger
        currentHiscore_timestamp = datetime.datetime.now()
        commandAuthor = ctx.message.author

        #print log of interaction in terminal
        print(f"[{currentHiscore_timestamp}] {commandAuthor} used 'currentHiscore' with player name '{playerName}'.")
        
        #requesting data from DONE_Lookup_PlayerCurrentStatus by using playerName as argument
        returnStatus = Lookup_PlayerCurrentStatus.playerCurrentStatus(playerName)
        
        #check if returnStatus[0][0] returns 1. If so, then return currentHiscore
        if returnStatus[0][0] == 1:
        
            returnHiscores = Lookup_PlayerCurrentStatus.playerCurrentHiscores(playerName)
            returnActivities = Lookup_PlayerCurrentStatus.playerCurrentActivities(playerName)
            returnAchievements = Lookup_PlayerCurrentStatus.playerLastAchievements(playerName)

            #creating table with current combat and quest stats using returnStatus
            statusTable = t2a(
                header=["Combat level/Quest progression", "Score"],
                body=[['Combat level', returnStatus[1][0]], 
                    ['Quests completed', returnStatus[1][1]], 
                    ['Quests started', returnStatus[1][2]], 
                    ['Quests not started', returnStatus[1][3]]],
                style=PresetStyle.thin_compact
            )

            #creating table with current hiscores using returnHiscores
            hiscoreTable = t2a(
                header=["Skill", "Rank", "Level", "Experience"],
                body=[[returnHiscores[0], returnHiscores[1], returnHiscores[2], returnHiscores[3]], 
                    [returnHiscores[4], returnHiscores[5], returnHiscores[6], returnHiscores[7]]],
                style=PresetStyle.thin_compact
            )

            #creating table with current activities using returnActivities
            activitiesTable = t2a(
                header=["Activity", "Rank", "Score"],
                body=[[returnActivities[0], returnActivities[1], returnActivities[2]],
                    [returnActivities[3], returnActivities[4], returnActivities[5]], 
                    [returnActivities[6], returnActivities[7], returnActivities[8]]],
                style=PresetStyle.thin_compact
            )

            #creating table with last achievements/event logs using returnAchievements
            lastAchievementsTable = t2a(
                header=["Event date", "Event"],
                body=[[returnAchievements[0], returnAchievements[1]], 
                    [returnAchievements[2], returnAchievements[3]], 
                    [returnAchievements[4], returnAchievements[5]], 
                    [returnAchievements[6], returnAchievements[7]], 
                    [returnAchievements[8], returnAchievements[9]]],
                style=PresetStyle.thin_compact
            )

            #return tables to discord channel
            await ctx.send(f'Overview for {playerName}.')
            await ctx.send(f"```\n{statusTable}\n```")
            await ctx.send('Last Hiscore readings.')
            await ctx.send(f"```\n{hiscoreTable}\n```")
            await ctx.send('Last activity readings.')
            await ctx.send(f"```\n{activitiesTable}\n```")
            await ctx.send('Recent event logs/achievements.')
            await ctx.send(f"```\n{lastAchievementsTable}\n```")

        #if returnStatus[0][0] does not return one, return below
        else:
            await ctx.send(f"Data for {playerName} is missing from database.")

    @bot.command()
    async def pCurrentCompare(ctx, playerName1, playerName2):

        #!help information message
        """Answers with a current status/hiscores comparison of two indicated players"""

        #create objects for usage in terminal event logger
        pCurrentCompare_timestamp = datetime.datetime.now()
        commandAuthor = ctx.message.author

        #print log of interaction in terminal
        print(f"[{pCurrentCompare_timestamp}] {commandAuthor} used 'pCurrentCompare' command with player names '{playerName1}' and '{playerName2}'")

        #requesting data from DONE_Lookup_PlayerCurrentCompare.compareCurrentPlayerStatus
        returnStatus = Lookup_PlayerCurrentCompare.compareCurrentPlayerStatus(playerName1, playerName2)
        
        #checks if Status dataframe contains data. If it does contain data, return pCurrentCompare
        if returnStatus[0][0] == 1 and returnStatus[0][1] == 1:

            #requesting other tables from DONE_Lookup_PlayerCurrentCompare
            returnHiscores = Lookup_PlayerCurrentCompare.compareCurrentPlayerSkills(playerName1, playerName2)
            returnActivities = Lookup_PlayerCurrentCompare.compareCurrentPlayerActivities(playerName1, playerName2)
            returnAchievements = Lookup_PlayerCurrentCompare.compareLast30daysPlayerAchievements(playerName1, playerName2)

            #creating table to compare both player's combat level and quest progression using returnStatus
            statusTable = t2a(
                header=["Combat level/quest progression", playerName1 + "'s score", playerName2 + "'s score"],
                body=[['Combat level', returnStatus[1][0], returnStatus[2][0]],
                    ['Quests completed', returnStatus[1][1], returnStatus[2][1]],
                    ['Quests started', returnStatus[1][2], returnStatus[2][2]],
                    ['Quests not started', returnStatus[1][3], returnStatus[2][3]]],
                style=PresetStyle.thin_compact
            )

            #creating table to compare both player's skills using returnHiscores
            hiscoreTable = t2a(
                header=["skill", playerName1 + "'s rank", playerName2 + "'s rank", playerName1 + "'s level", playerName2 + "'s level", playerName1 + "'s experience", playerName2 + "'s experience", "Experience difference"],
                body=[[returnHiscores[0][0], returnHiscores[0][1], returnHiscores[0][2], returnHiscores[0][3], returnHiscores[0][4], returnHiscores[0][5], returnHiscores[0][6], returnHiscores[0][7]],
                    [returnHiscores[1][0], returnHiscores[1][1], returnHiscores[1][2], returnHiscores[1][3], returnHiscores[1][4], returnHiscores[1][5], returnHiscores[1][6], returnHiscores[1][7]]],
                style=PresetStyle.thin_compact
            )

            #creating table to compare both player's activities using returnActivities
            activitiesTable = t2a(
                header=["Activity", playerName1 + "'s rank", playerName2 + "'s rank", playerName1 + "'s score", playerName2 + "'s score", "Score difference"],
                body=[[returnActivities[0][0], returnActivities[0][1], returnActivities[0][2], returnActivities[0][3], returnActivities[0][4], returnActivities[0][5]],
                    [returnActivities[1][0], returnActivities[1][1], returnActivities[1][2], returnActivities[1][3], returnActivities[1][4], returnActivities[1][5]]],
                style=PresetStyle.thin_compact
            )

            #creating table to compare number of achievements/event logs recorded in last 30 days using returnAchievements
            achievementsTable = t2a(
                header=["Player name", "Number of achievements in last 30 days"],
                body=[[playerName1, returnAchievements[0]],
                    [playerName2, returnAchievements[1]]],
                style=PresetStyle.thin_compact
            )

            await ctx.send(f"Overview for {playerName1} and {playerName2}.")
            await ctx.send(f"```\n{statusTable}\n```")
            await ctx.send(f"Hiscore overview for {playerName1} and {playerName2}.")
            await ctx.send(f"```\n{hiscoreTable}\n```")
            await ctx.send(f"Activities ranking for {playerName1} and {playerName2}.")
            await ctx.send(f"```\n{activitiesTable}\n```")
            await ctx.send(f"Number of achievements/events logged for {playerName1} and {playerName2}.")
            await ctx.send(f"```\n{achievementsTable}\n```")
        
        #if data missing for P1, return below
        elif returnStatus[0][0] == 0 and returnStatus[0][1] == 1:
            await ctx.send(f"Data for {playerName1} is missing from database.")

        #if data missing for P2, return below
        elif returnStatus[0][0] == 1 and returnStatus[0][1] == 0:
            await ctx.send(f"Data for {playerName2} is missing from database.")

        #return below if data is missing for both P1 and P2
        else:
            await ctx.send(f"Data for {playerName1} and {playerName2}is missing from database.")
    
    bot.run(TOKEN)