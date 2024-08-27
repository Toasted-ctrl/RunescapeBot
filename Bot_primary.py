import discord
import Lookup_PlayerCurrentStatus
import Lookup_PlayerCurrentCompare
import Lookup_PlayerDxpChallenges
import admin
import datetime
import os
import commandInputChecker
from dotenv import load_dotenv, dotenv_values
from discord.ext import commands
from table2ascii import table2ascii as t2a, PresetStyle

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
        if message.content == "Test input 1":
            await message.channel.send("Test response 1")
        if message.content == "Test input 2":
            await message.channel.send("Test response 2")

    #addTrackingFor command, using discord username and playerName as arguments
    @bot.command()
    async def addTracking(ctx, playerName):

        #!help information message
        """Adds player to historical tracking. Will store daily hiscore/logs in database. Can only be used by Admins, Global Admins and Super Admins."""

        #create objects for usage in terminal event logger, as well as commandAuthor for retrieving adminrights for discord user
        addTrackingFor_timestamp = datetime.datetime.now()
        commandAuthor = ctx.message.author

        #print log of interaction in terminal
        print(f"[{addTrackingFor_timestamp}] {commandAuthor} used 'addTracking' with player name '{playerName}'.")

        #input validation to check if any characters in input are forbidden
        userCheckInputString = commandInputChecker.checkInputString(playerName)

        if userCheckInputString == 1:

            #requesting admin rights for command author
            adminRights = admin.retrieveAdminRights(str(commandAuthor))

            #if user does not have admin rights, return:
            if adminRights[0] == 0:
                await ctx.send(f"{commandAuthor} does not have permission to add tracking for '{playerName}'.")
            
            elif adminRights[0] == 1 and adminRights[2] == 1:
                #check if player exists in tracked list prior to adding
                playerExistsInTracking_prior = admin.checkPlayerExistsInTrackedList(playerName)

                #if player exists in tracking, return that player is already being tracked
                if playerExistsInTracking_prior == 1:
                    await ctx.send(f"Statistics for '{playerName}' are already tracked.")

                #if player does not exist in tracking, do following:
                else:
                    #add player to tracked list
                    admin.addPlayerToTrackedList(playerName)
                    
                    #check again if player was added to tracked list
                    playerExistsInTracking_after = admin.checkPlayerExistsInTrackedList(playerName)

                    if playerExistsInTracking_after == 1:
                        await ctx.send(f"Tracking was enabled for '{playerName}'.")
                    else:
                        await ctx.send(f"Tracking could not be enabled for '{playerName}'.")

            else:
                await ctx.send("Error: An unexpected error occured.")

        else:
            await ctx.send("Error: Violation of input criteria. Only characters A-Z, a-z, and 0-9 are allowed.")

    #removeTracking command, using discord username and playerName as arguments
    @bot.command()
    async def removeTracking(ctx, playerName):

        #!help information message
        """Removes player from historical tracking. Can only be used by Admins, Global Admin and Super Admins."""

        #create objects for usage in terminal event logger, as well as commandAuthor for retrieving adminrights for discord user
        removeTrackingfor_timestamp = datetime.datetime.now()
        commandAuthor = ctx.message.author

        #print log of interaction in terminal
        print(f"[{removeTrackingfor_timestamp}] {commandAuthor} used 'removeTracking' with player name '{playerName}'.")

        #requesting admin rights for command author
        adminRights = admin.retrieveAdminRights(str(commandAuthor))

        #input validation to check if any characters in input are forbidden
        userCheckInputString = commandInputChecker.checkInputString(playerName)

        if userCheckInputString == 1:

            #if user does not have admin rights, return:
            if adminRights[0] == 0:
                await ctx.send(f"{commandAuthor} does not have permission to remove tracking for '{playerName}'.")
            
            elif adminRights[0] == 1 and adminRights[2] == 1:
                #check if player exists in tracking before remove function
                playerExistsInTracking_prior = admin.checkPlayerExistsInTrackedList(playerName)

                #if player does not exist in tracked list, return:
                if playerExistsInTracking_prior == 0:
                    await ctx.send(f"'{playerName}' was already untracked.")

                else:
                    #remove player from tracking list
                    admin.removePlayerFromTrackedList(playerName)
                    
                    #check if player exists in tracked list after remove function
                    playerExistsInTracking_after = admin.checkPlayerExistsInTrackedList(playerName)

                    #if player was removed successfully, return:
                    if playerExistsInTracking_after == 0:
                        await ctx.send(f"Tracking was disabled for '{playerName}'.")
                    
                    #if player was not successfully removed, return:
                    else:
                        await ctx.send(f"Tracking could not be disabled for '{playerName}'.")

            else:
                await ctx.send("Error: An unexpected error occured.")

        else:
            await ctx.send("Error: Violation of input criteria. Only characters A-Z, a-z, and 0-9 are allowed.")

    #command for superadmin to add new admins
    @bot.command()
    async def addAdmin(ctx, discord_username):

        #!help text
        """Adds Admin rights for specific user. Can only be used by Global Admins and Super Admins."""

        #create objects for usage in terminal event logger, as well as commandAuthor for retrieving adminrights for discord user
        addAdmin_timestamp = datetime.datetime.now()
        commandAuthor = ctx.message.author

        print(f"[{addAdmin_timestamp}] {commandAuthor} used 'addAdmin' with discord username '{discord_username}'.")

        #retrieve admin rights for user
        adminRights = admin.retrieveAdminRights(str(commandAuthor))

        #input validation to check if any characters in input are forbidden
        userCheckInputString = commandInputChecker.checkInputString(discord_username)

        if userCheckInputString == 1:

            #check if potential new exists as admin
            checkIfUserIsAdmin_before = admin.retrieveAdminRights(discord_username)

            #if user exists as admin already, return:
            if checkIfUserIsAdmin_before[0] == 1:
                await ctx.send(f"'{discord_username}' is already an Admin.")

            else:
                #if user does not have permission to add new admins, return:
                if adminRights[3] == 0:
                    await ctx.send(f"{commandAuthor} does not have permission to add new Admins.")
                
                #if user does have permission to add new admins, do:
                if adminRights[0] == 1 and adminRights[3] == 1:

                    #add new admin
                    admin.addAdminToAdminList(discord_username)
                    checkIfUserIsAdmin_after = admin.retrieveAdminRights(discord_username)

                    #if user was added as admin, return:
                    if checkIfUserIsAdmin_after[0] == 1:
                        await ctx.send(f"'{discord_username}' is now an Admin.")

                    #if user was not added as admin, return:
                    else:
                        await ctx.send(f"'{discord_username}' could not be added as Admin.")

        else:
            await ctx.send("Error: Violation of input criteria. Only characters A-Z, a-z, and 0-9 are allowed.")

    #command to remove admin
    @bot.command()
    async def removeAdmin(ctx, discord_username):

        #!help text
        """Removes Admin rights for user. Can only be used by Global Admins and Super Admins"""

        #create objects for usage in terminal event logger, as well as commandAuthor for retrieving adminrights for discord user
        removeAdmin_timestamp = datetime.datetime.now()
        commandAuthor = ctx.message.author

        print(f"[{removeAdmin_timestamp}] {commandAuthor} used 'removeAdmin' with discord username '{discord_username}'.")

        #check if user has admin rights
        adminRights = admin.retrieveAdminRights(str(commandAuthor))

        #input validation to check if any characters in input are forbidden
        userCheckInputString = commandInputChecker.checkInputString(discord_username)

        if userCheckInputString == 1:

            #check if user exists as admin
            checkIfUserIsAdmin_before = admin.retrieveAdminRights(discord_username)

            #if user is already non-existent as admin, return:
            if checkIfUserIsAdmin_before[0] == 0:
                await ctx.send(f"'{discord_username}' is not an Admin.")

            else:
                #if user does not have admin permissions, return:
                if adminRights[3] == 0:
                    await ctx.send(f"{commandAuthor} does not have permission to remove Admins.")

                #if user does have admin persmission, do:
                if adminRights[0] == 1 and adminRights[3] == 1:
                    admin.removeAdminFromAdminList(discord_username)

                    #check if user was removed as admin
                    checkIfUserIsAdmin_after = admin.retrieveAdminRights(discord_username)

                    #if admin rights were revoked, return:
                    if checkIfUserIsAdmin_after[0] == 0:
                        await ctx.send(f"'{discord_username}'s' Admin rights were revoked.")

                    #if admin rights were not revoked, return:
                    else:
                        await ctx.send(f"'{discord_username}'s' Admin rights could not be revoked.")

        else:
            await ctx.send("Error: Violation of input criteria. Only characters A-Z, a-z, and 0-9 are allowed.")

    #command to add Global Admins
    @bot.command()
    async def addGlobalAdmin(ctx, discord_username):

        #!help text
        """Adds Global Admin permission for user. Can only be used by Super Admins."""

        addGlobalAdmin_timestamp = datetime.datetime.now()
        commandAuthor = ctx.message.author

        print(f"[{addGlobalAdmin_timestamp}] {commandAuthor} used 'addGlobalAdmin' with discord username '{discord_username}'.")

        #check if user is already Global Admin
        checkIfUserIsGlobalAdmin_before = admin.retrieveAdminRights(discord_username)

        #input validation to check if any characters in input are forbidden
        userCheckInputString = commandInputChecker.checkInputString(discord_username)

        if userCheckInputString == 1:

            #retrieve admin rights for command author
            adminRights = admin.retrieveAdminRights(str(commandAuthor))

            #if user is already global admin, return:
            if checkIfUserIsGlobalAdmin_before [3] == 1:
                await ctx.send(f"'{discord_username}' is already a Global Admin.")

            #if user is not global admin yet, do:
            else:

                #if user does not have permission to add global admins, return:
                if adminRights[4] == 0:
                    await ctx.send(f"{commandAuthor} does not have permission to add Global Admins.")

                #if user has permission to add global admins, do:
                if adminRights[4] == 1:
                    admin.addGlobalAdminToAdminList(discord_username)
                    checkIfUserIsGlobalAdmin_after = admin.retrieveAdminRights(discord_username)

                    if checkIfUserIsGlobalAdmin_after[3] == 1:
                        await ctx.send(f"'{discord_username}' is now a Global Admin.")

                    else:
                        await ctx.send(f"'{discord_username}' could not be added as Global Admin.")

        else:
            await ctx.send("Error: Violation of input criteria. Only characters A-Z, a-z, and 0-9 are allowed.")

    #command to add Global Admins
    @bot.command()
    async def removeGlobalAdmin(ctx, discord_username):

        #!help text
        """Removes Global Admin permission for user. Can only be used by Super Admins."""

        removeGlobalAdmin_timestamp = datetime.datetime.now()
        commandAuthor = ctx.message.author

        print(f"[{removeGlobalAdmin_timestamp}] {commandAuthor} used 'removeGlobalAdmin' with discord username '{discord_username}'.")

        #check if user is already Global Admin
        checkIfUserIsGlobalAdmin_before = admin.retrieveAdminRights(discord_username)

        #input validation to check if any characters in input are forbidden
        userCheckInputString = commandInputChecker.checkInputString(discord_username)

        if userCheckInputString == 1:

            #retrieve admin rights for command author
            adminRights = admin.retrieveAdminRights(str(commandAuthor))

            #if user is not a global admin:
            if checkIfUserIsGlobalAdmin_before [3] == 0:
                await ctx.send(f"'{discord_username}' is not a Global Admin.")

            #if user is a global admin:
            else:

                #if user does not have permission to add global admins, return:
                if adminRights[4] == 0:
                    await ctx.send(f"{commandAuthor} does not have permission to remove Global Admins.")

                #if user has permission to add global admins, do:
                if adminRights[4] == 1:
                    admin.removeGlobalAdminFromAdminList(discord_username)
                    checkIfUserIsGlobalAdmin_after = admin.retrieveAdminRights(discord_username)

                    if checkIfUserIsGlobalAdmin_after[3] == 0:
                        await ctx.send(f"'{discord_username}'s' Global Admin permissions were revoked.")

                    else:
                        await ctx.send(f"'{discord_username}'s' Global Admin permissions could not be revoked.")

        else:
            await ctx.send("Error: Violation of input criteria. Only characters A-Z, a-z, and 0-9 are allowed.")

    #check content of main_runescape_flagged_usernames
    @bot.command()
    async def checkFlagged(ctx):

        #!help information message
        """Adds player to historical tracking. Will store daily hiscore/logs in database. Can only be used by Admins, Global Admins and Super Admins."""

        #create objects for usage in terminal event logger, as well as commandAuthor for retrieving adminrights for discord user
        addCheckFlagged_timestamp = datetime.datetime.now()
        commandAuthor = ctx.message.author

        #print log of interaction in terminal
        print(f"[{addCheckFlagged_timestamp}] {commandAuthor} used 'checkFlagged'.")

        #requesting admin rights for command author
        adminRights = admin.retrieveAdminRights(str(commandAuthor))

        #if user does not have admin rights, return:
        if adminRights[0] == 0:
            await ctx.send(f"Error: Access violation. {commandAuthor} does not have permission to add retrieve flagged_usernames'.")
            
        elif adminRights[0] == 1 and adminRights[2] == 1:
            #check if player exists in tracked list prior to adding
            checkedFlaggedList = admin.checkFlagged()

            #if no players exist in flagged list, return below
            if checkedFlaggedList[0][0] == 0:
                await ctx.send("There are currently no players in flagged_usernames.")

            #if players exist in flagged list, return below:
            else:
                numberOfUsersInFlaggedList = checkedFlaggedList[0][0]
                usersInFlaggedList = checkedFlaggedList[1][:numberOfUsersInFlaggedList]
                await ctx.send(f"There are currently {numberOfUsersInFlaggedList} names in flagged_usernames. Their usernames are: {usersInFlaggedList}.")

        else:
            await ctx.send("Error: An unexpected error occured.")

    #check content of main_runescape_flagged_usernames
    @bot.command()
    async def updateTracking(ctx, playerName1, playerName2):

        #!help information message
        """Updates tracking, historical records, and removes old name from flagged_usernames if present. Requires old and new username."""

        #create objects for usage in terminal event logger, as well as commandAuthor for retrieving adminrights for discord user
        addCheckFlagged_timestamp = datetime.datetime.now()
        commandAuthor = ctx.message.author

        #print log of interaction in terminal
        print(f"[{addCheckFlagged_timestamp}] {commandAuthor} used 'updateTracking' with '{playerName1}' and '{playerName2}'.")

        #requesting admin rights for command author
        adminRights = admin.retrieveAdminRights(str(commandAuthor))

        #check if user input is valid
        checkInputString_p1 = commandInputChecker.checkInputString(playerName1)
        checkInputString_p2 = commandInputChecker.checkInputString(playerName2)

        if checkInputString_p1 == 1 and checkInputString_p2 == 1:

            #if user does not have admin rights, return:
            if adminRights[0] == 0:
                await ctx.send(f"Error: Access violation. {commandAuthor} does not have permission to add update records.")
                
            elif adminRights[0] == 1:
                checkTrackedList_p1 = admin.checkPlayerExistsInTrackedList(playerName1)
                checkTrackedList_p2 = admin.checkPlayerExistsInTrackedList(playerName2)

                if checkTrackedList_p2 == 1:

                    await ctx.send(f"Error: Duplication Violation. '{playerName2}' already exists in tracking. It is not allowed to update record if the new name already exists in main_runescape_tracked_usernames.")

                elif checkTrackedList_p1 == 0:

                    await ctx.send(f"Error: Missing data. '{playerName1}' does not exist tracking.")

                elif checkTrackedList_p1 == 1 and checkTrackedList_p2 == 0:

                    checkHiscores_p1 = admin.checkPlayerExistInHiScores(playerName1)
                    checkHiscores_p2 = admin.checkPlayerExistInHiScores(playerName2)

                    if checkHiscores_p2 == 1:

                        await ctx.send(f"Error: Duplication Violation. '{playerName2}' already exists in hiscores. It is not allowed to update record if the second name already exists in main_runescape_hiscores.")

                    elif checkHiscores_p1 == 0:

                        await ctx.send(f"Error: Missing data. '{playerName1}' does not exist in hiscores.")

                    elif checkHiscores_p1 == 1 and checkHiscores_p2 == 0:

                        admin.updateTrackedUser(playerName1, playerName2)
                        admin.updateHistoricalUserData(playerName1, playerName2)
                        admin.removePlayerFromFlaggedList(playerName1)

                        await ctx.send("Attempting to update records.")

                        checkUpdateTrackingCompleted_p1 = admin.checkPlayerExistsInTrackedList(playerName2)

                        checkUpdateHiscoresCompleted_p1 = admin.checkPlayerExistInHiScores(playerName2)

                        checkUpdateFlagged = admin.checkPlayerExistInFlaggedList(playerName2)

                        if checkUpdateTrackingCompleted_p1 == 1 and checkUpdateHiscoresCompleted_p1 == 1 and checkUpdateFlagged == 0:

                            await ctx.send("Update completed.")

                        elif checkUpdateTrackingCompleted_p1 == 0 or checkUpdateHiscoresCompleted_p1 == 0 or checkUpdateFlagged == 1:

                            await ctx.send(f"Error: Incomplete update. Status {checkUpdateTrackingCompleted_p1}-{checkUpdateHiscoresCompleted_p1}-{checkUpdateFlagged}.")

                        else:
                            await ctx.send("Error: Possible incomplete update. Please contact Super Admin.")

                    else:
                        await ctx.send("Error: An unexpected error occured.")

                else:
                    await ctx.send("Error: An unexpected error occured.")
                
            else:
                await ctx.send("Error: An unexpected error occured.")

        elif checkInputString_p1 == 0 or checkInputString_p2 == 0:
            await ctx.send(f"Error: Violation of input criteria. Only characters A-Z, a-z, and 0-9 are allowed.")

        else:
            await ctx.send(f"Error: An unexpected error occured.")
                
    #currentHiscore command using playerName as arguments
    @bot.command()
    async def currentHiscore(ctx, playerName):

        #!help information message
        """Answers with current status/hiscore of indicated player"""

        #create objects for usage in terminal event logger
        currentHiscore_timestamp = datetime.datetime.now()
        commandAuthor = ctx.message.author

        #print log of interaction in terminal
        print(f"[{currentHiscore_timestamp}] {commandAuthor} used 'currentHiscore' with player name '{playerName}'.")

        #input validation to check if any characters in input are forbidden
        userCheckInputString = commandInputChecker.checkInputString(playerName)

        if userCheckInputString == 1:
        
            #checking if player exists in all required databases
            databaseCheck = commandInputChecker.checkDatabasePresence(playerName)

            #check if returnStatus[0][0] returns 1. If so, then return currentHiscore
            if databaseCheck[0] == 1 and databaseCheck[1] == 1 and databaseCheck[2] == 1 and databaseCheck[3] == 1:
                
                returnStatus = Lookup_PlayerCurrentStatus.playerCurrentStatus(playerName)
                returnHiscores = Lookup_PlayerCurrentStatus.playerCurrentHiscores(playerName)
                returnActivities = Lookup_PlayerCurrentStatus.playerCurrentActivities(playerName)
                returnAchievements = Lookup_PlayerCurrentStatus.playerLastAchievements(playerName)

                #creating table with current combat and quest stats using returnStatus
                statusTable = t2a(
                    header=["Combat level/Quest progression", "Score"],
                    body=[['Combat level', returnStatus[1]], 
                        ['Quests completed', returnStatus[2]], 
                        ['Quests started', returnStatus[3]], 
                        ['Quests not started', returnStatus[4]]],
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

                await ctx.send(f"Data for {playerName} is missing from database. Return Status: {databaseCheck}.")

        else:
            await ctx.send("Error: Violation of input criteria. Only characters A-Z, a-z, and 0-9 are allowed.")

    @bot.command()
    async def pCurrentCompare(ctx, playerName1, playerName2):

        #!help information message
        """Answers with a current status/hiscores comparison of two indicated players."""

        #create objects for usage in terminal event logger
        pCurrentCompare_timestamp = datetime.datetime.now()
        commandAuthor = ctx.message.author

        #print log of interaction in terminal
        print(f"[{pCurrentCompare_timestamp}] {commandAuthor} used 'pCurrentCompare' command with player names '{playerName1}' and '{playerName2}'")

        #input validation to check if any characters in input are forbidden
        userCheckInputString_p1 = commandInputChecker.checkInputString(playerName1)
        userCheckInputString_p2 = commandInputChecker.checkInputString(playerName2)

        if userCheckInputString_p1 == 1 and userCheckInputString_p2 == 1:

            #requesting data from DONE_Lookup_PlayerCurrentCompare.compareCurrentPlayerStatus
            databaseCheck_p1 = commandInputChecker.checkDatabasePresence(playerName1)
            databaseCheck_p2 = commandInputChecker.checkDatabasePresence(playerName2)

            databaseCheckCount_p1 = databaseCheck_p1[0] + databaseCheck_p1[1] + databaseCheck_p1[2] + databaseCheck_p1[3]
            databaseCheckCount_p2 = databaseCheck_p2[0] + databaseCheck_p2[1] + databaseCheck_p2[2] + databaseCheck_p2[3]
            
            #checks if Status dataframe contains data. If it does contain data, return pCurrentCompare
            if databaseCheckCount_p1 == 4 and databaseCheckCount_p2 == 4:

                #requesting other tables from DONE_Lookup_PlayerCurrentCompare
                returnStatus = Lookup_PlayerCurrentCompare.compareCurrentPlayerStatus(playerName1, playerName2)
                returnHiscores = Lookup_PlayerCurrentCompare.compareCurrentPlayerSkills(playerName1, playerName2)
                returnActivities = Lookup_PlayerCurrentCompare.compareCurrentPlayerActivities(playerName1, playerName2)
                returnAchievements = Lookup_PlayerCurrentCompare.compareLast30daysPlayerAchievements(playerName1, playerName2)

                #creating table to compare both player's combat level and quest progression using returnStatus
                statusTable = t2a(
                    header=["Combat level/quest progression", playerName1 + "'s score", playerName2 + "'s score"],
                    body=[['Combat level', returnStatus[0][1], returnStatus[1][1]],
                        ['Quests completed', returnStatus[0][2], returnStatus[1][2]],
                        ['Quests started', returnStatus[0][3], returnStatus[1][3]],
                        ['Quests not started', returnStatus[0][4], returnStatus[1][4]]],
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
            elif databaseCheckCount_p1 < 4 and databaseCheckCount_p2 == 4:
                await ctx.send(f"Error: Data for {playerName1} is missing from database. Return Status for {playerName1}: {databaseCheck_p1}.")

            #if data missing for P2, return below
            elif databaseCheckCount_p1 == 4 and databaseCheckCount_p2 < 4:
                await ctx.send(f"Error: Data for {playerName2} is missing from database. Return Status for {playerName2}: {databaseCheck_p2}.")

            #return below if data is missing for both P1 and P2
            else:
                await ctx.send(f"Error: Data for both players ('{playerName1}' and '{playerName2}') is missing from database. Return Status for {playerName1}: {databaseCheck_p1}. Return Status for {playerName2}: {databaseCheck_p2}.")

        else:
            await ctx.send("Error: Violation of input criteria. Only characters A-Z, a-z, and 0-9 are allowed.")

    @bot.command()
    async def dxpChallenge (ctx, firstInsertedDate, secondInsertedDate):

        #!help information message
        """Returns graph of all tracked players and experience gained between two dates."""

        #create objects for usage in terminal event logger
        pCurrentCompare_timestamp = datetime.datetime.now()
        commandAuthor = ctx.message.author

        #print log of interaction in terminal
        print(f"[{pCurrentCompare_timestamp}] {commandAuthor} used 'dxpChallenge' command with firstInsertedDate '{firstInsertedDate}' and secondInsertedDate '{secondInsertedDate}'.")

        #check if input data meets criteria
        if commandInputChecker.checkInputDate(firstInsertedDate) == 1 and commandInputChecker.checkInputDate(secondInsertedDate) == 1:
            dateOrderCheck = commandInputChecker.checkDateOrder(firstInsertedDate, secondInsertedDate)
            if dateOrderCheck[0] == 1:
                inputMeetsCriteria = 1
            elif dateOrderCheck[0] == 2:
                inputMeetsCriteria = 1
            elif dateOrderCheck[0] == 0:
                inputMeetsCriteria = 0
        else:
            inputMeetsCriteria = 0

        #if return status == 1, dxpBetweenTwoDates created a graph and the DataFrame is not empty.
        if inputMeetsCriteria == 1:

            #creating returnstatus to determine whether graph can be sent to discord
            returnStatus = Lookup_PlayerDxpChallenges.dxpBetweenTwoDates(dateOrderCheck[1], dateOrderCheck[2])

            #create file to send in response
            file = discord.File("ExperienceGainedBetweenTwoDates.png", filename=(f"DXP_Experience Gained between {dateOrderCheck[1]} and {dateOrderCheck[2]}.png"))

            if returnStatus[0] == 1:
                await ctx.send(f"Players gained the following experience between '{dateOrderCheck[1]}' and '{dateOrderCheck[2]}':", file=file)
            elif returnStatus[0] == 0: #0 is returned if graph was generated but dataframe is empty.
                await ctx.send(f"Error: returnStatus = '{returnStatus[0]}', DataFrame is empty with given parameters. Please try again with different dates.")
            else:
                await ctx.send(f"Error: An unexpected error occured while creating graph.")
        else:
            await ctx.send(f"Error: Violation of input criteria. Two differing dates must be provided, and they must be in YYYY-MM-DD format. The dates must be separated by a space.")

    bot.run(TOKEN)