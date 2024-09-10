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


    @bot.command()
    async def checkTracked(ctx):

        #!help information message
        """Retrieves list of all RuneScape player names that are currently being tracked."""

        #create objects for usage in terminal event logger, as well as commandAuthor for retrieving adminrights for discord user
        addCheckTracked_timestamp = datetime.datetime.now()
        commandAuthor = ctx.message.author

        #print log of interaction in terminal
        print(f"[{addCheckTracked_timestamp}] {commandAuthor} used 'checkTracked'.")

        #retrieve admin rights for discord user
        adminRights = admin.retrieveAdminRights(str(commandAuthor))

        #only allowed to invoke command if user has general admin rights
        if adminRights[0] == 1 and adminRights[2] == 1:

            #obtain tracked users
            trackedUsersResponse = admin.retrieveTrackedUsers()

            #if trackedUsersResponse[0] == 1, return list of tracked users
            if trackedUsersResponse[0] == 1:

                table_string = trackedUsersResponse[1].to_string()
                formatted_table = (f"```\n{table_string}\n```")

                await ctx.send(f"Players that are currently being tracked:\n\n{formatted_table}")

            #if trackedUsersResponse[0] == 0, return that no users are currently being tracked
            elif trackedUsersResponse[0] == 0:

                await ctx.send(f"No players are currently being tracked.")

            #if trackedUsersResponse[0] == 2, return that unexpected error occured when on creating DataFrame
            elif trackedUsersResponse[0] == 2:

                await ctx.send(f"Error: An unexpected error occured while trying to retrieve DataFrame.")

            #else, return unexpected error.
            else:

                await ctx.send(f"Error: An unexpected error occured.")

        #deny command if user does not meet admin rights requirements
        else:

            await ctx.send(f"Error: You do not have the right permission to use the checkTracked command.")

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

        #if userCheckInputString returns 1, follow below
        if userCheckInputString[0] == 1:

            #retrieving corrected playerName 
            checkedPlayerName = userCheckInputString[1]

            #requesting admin rights for command author
            adminRights = admin.retrieveAdminRights(str(commandAuthor))

            #if user does not have admin rights, return:
            if adminRights[0] == 0:
                await ctx.send(f"{commandAuthor} does not have permission to add tracking for '{checkedPlayerName}'.")
            
            elif adminRights[0] == 1 and adminRights[2] == 1:
                #check if player exists in tracked list prior to adding
                playerExistsInTracking_prior = admin.checkPlayerExistsInTrackedList(checkedPlayerName)

                #if player exists in tracking, return that player is already being tracked
                if playerExistsInTracking_prior == 1:
                    await ctx.send(f"Statistics for '{checkedPlayerName}' are already tracked.")

                #if player does not exist in tracking, do following:
                else:
                    #add player to tracked list
                    admin.addPlayerToTrackedList(checkedPlayerName)
                    
                    #check again if player was added to tracked list
                    playerExistsInTracking_after = admin.checkPlayerExistsInTrackedList(checkedPlayerName)

                    if playerExistsInTracking_after == 1:
                        await ctx.send(f"Tracking was enabled for '{checkedPlayerName}'.")
                    else:
                        await ctx.send(f"Tracking could not be enabled for '{checkedPlayerName}'.")

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

        if userCheckInputString[0] == 1:

            #retrieving corrected playerName 
            checkedPlayerName = userCheckInputString[1]

            #if user does not have admin rights, return:
            if adminRights[0] == 0:
                await ctx.send(f"{commandAuthor} does not have permission to remove tracking for '{checkedPlayerName}'.")
            
            elif adminRights[0] == 1 and adminRights[2] == 1:
                #check if player exists in tracking before remove function
                playerExistsInTracking_prior = admin.checkPlayerExistsInTrackedList(checkedPlayerName)

                #if player does not exist in tracked list, return:
                if playerExistsInTracking_prior == 0:
                    await ctx.send(f"'{checkedPlayerName}' was already untracked.")

                else:
                    #remove player from tracking list
                    admin.removePlayerFromTrackedList(checkedPlayerName)
                    
                    #check if player exists in tracked list after remove function
                    playerExistsInTracking_after = admin.checkPlayerExistsInTrackedList(checkedPlayerName)

                    #if player was removed successfully, return:
                    if playerExistsInTracking_after == 0:
                        await ctx.send(f"Tracking was disabled for '{checkedPlayerName}'.")
                    
                    #if player was not successfully removed, return:
                    else:
                        await ctx.send(f"Tracking could not be disabled for '{checkedPlayerName}'.")

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
            if checkedFlaggedList[0] == 0:
                await ctx.send("There are currently no flagged RuneScape player names.")

            elif checkedFlaggedList[0] == 1:

                checkedFlagTableToString = checkedFlaggedList[1].to_string()
                checkedFlagFormattedTable = (f"```\n{checkedFlagTableToString}\n```")

                await ctx.send(f"The following RuneScape users are currently flagged:\n\n{checkedFlagFormattedTable}")

            elif checkedFlaggedList[0] == 2:

                await ctx.send(f"Error: An unexpected error occured while attempting to create DataFrame.")

            else:

                await ctx.send(f"Error: An unexpected error occured (1).")

        else:
            await ctx.send("Error: An unexpected error occured (0).")

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

        if checkInputString_p1[0] == 1 and checkInputString_p2[0] == 1:

            #if user does not have admin rights, return:
            if adminRights[0] == 0:
                await ctx.send(f"Error: Access violation. {commandAuthor} does not have permission to add update records.")
                
            elif adminRights[0] == 1:

                checkedPlayerName_p1 = checkInputString_p1[1]
                checkedPlayerName_p2 = checkInputString_p2[1]

                checkTrackedList_p1 = admin.checkPlayerExistsInTrackedList(checkedPlayerName_p1)
                checkTrackedList_p2 = admin.checkPlayerExistsInTrackedList(checkedPlayerName_p2)

                if checkTrackedList_p2 == 1:

                    await ctx.send(f"Error: Duplication Violation. '{checkedPlayerName_p2}' already exists in tracking. It is not allowed to update record if the new name already exists in main_runescape_tracked_usernames.")

                elif checkTrackedList_p1 == 0:

                    await ctx.send(f"Error: Missing data. '{checkedPlayerName_p1}' does not exist tracking.")

                elif checkTrackedList_p1 == 1 and checkTrackedList_p2 == 0:

                    checkHiscores_p1 = admin.checkPlayerExistInHiScores(checkedPlayerName_p1)
                    checkHiscores_p2 = admin.checkPlayerExistInHiScores(checkedPlayerName_p2)

                    if checkHiscores_p2 == 1:

                        await ctx.send(f"Error: Duplication Violation. '{checkedPlayerName_p2}' already exists in hiscores. It is not allowed to update record if the second name already exists in main_runescape_hiscores.")

                    elif checkHiscores_p1 == 0:

                        await ctx.send(f"Error: Missing data. '{checkedPlayerName_p1}' does not exist in hiscores.")

                    elif checkHiscores_p1 == 1 and checkHiscores_p2 == 0:

                        admin.updateTrackedUser(checkedPlayerName_p1, checkedPlayerName_p2)
                        admin.updateHistoricalUserData(checkedPlayerName_p1, checkedPlayerName_p2)
                        admin.removePlayerFromFlaggedList(checkedPlayerName_p1)

                        await ctx.send("Attempting to update records.")

                        checkUpdateTrackingCompleted_p1 = admin.checkPlayerExistsInTrackedList(checkedPlayerName_p2)

                        checkUpdateHiscoresCompleted_p1 = admin.checkPlayerExistInHiScores(checkedPlayerName_p2)

                        checkUpdateFlagged = admin.checkPlayerExistInFlaggedList(checkedPlayerName_p2)

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

        elif checkInputString_p1[0] == 0 or checkInputString_p2[0] == 0:
            await ctx.send(f"Error: Violation of input criteria. Only characters A-Z, a-z, and 0-9 are allowed.")

        else:
            await ctx.send(f"Error: An unexpected error occured.")
                
    #currentHiscore command using playerName as arguments
    @bot.command()
    async def currentHiscore(ctx, playerName):

        #!help information message
        """Answers with latest status/hiscore of indicated player"""

        #create objects for usage in terminal event logger
        currentHiscore_timestamp = datetime.datetime.now()
        commandAuthor = ctx.message.author

        #print log of interaction in terminal
        print(f"[{currentHiscore_timestamp}] {commandAuthor} used 'currentHiscore' with player name '{playerName}'.")

        #input validation to check if any characters in input are forbidden
        userCheckInputString = commandInputChecker.checkInputString(playerName)

        #datestamp for invoking Lookup_PlayerCurrentStatus
        lookupInvokeDate = datetime.date.today()

        if userCheckInputString[0] == 1:

            checkPlayerName = userCheckInputString[1]
        
            #checking if player exists in all required databases
            databaseCheck = commandInputChecker.checkDatabasePresence(checkPlayerName)

            #check if returnStatus[0][0] returns 1. If so, then return currentHiscore
            if databaseCheck[0] == 1 and databaseCheck[1] == 1 and databaseCheck[2] == 1 and databaseCheck[3] == 1:
                
                #creating table with current combat and quest stats using returnStatus
                returnStatus = Lookup_PlayerCurrentStatus.playerCurrentStatus(checkPlayerName, lookupInvokeDate)
                status_string = returnStatus[1].to_string()
                status_final_table = (f"```\n{status_string}\n```")

                #creating table with current hiscores using returnHiscores
                returnHiscores = Lookup_PlayerCurrentStatus.playerCurrentHiscores(checkPlayerName, lookupInvokeDate)
                hiscore_string = returnHiscores[1].to_string()
                hiscore_final_table = (f"```\n{hiscore_string}\n```")

                #creating table with current activities using returnActivities
                returnActivities = Lookup_PlayerCurrentStatus.playerCurrentActivities(checkPlayerName, lookupInvokeDate)
                activites_string = returnActivities[1].to_string()
                activities_final_table = (f"```\n{activites_string}\n```")

                #creating table with last achievements/event logs using returnAchievements
                returnAchievements = Lookup_PlayerCurrentStatus.playerLastAchievements(checkPlayerName, lookupInvokeDate)
                achievements_string = returnAchievements[1].to_string()
                achievements_final_table = (f"```\n{achievements_string}\n```")

                #return tables to discord channel
                await ctx.send(f"Overview for '{checkPlayerName}'.")
                await ctx.send(f"Last Status reading:\n{status_final_table}")
                await ctx.send(f"Last Hiscore readings:\n{hiscore_final_table}")
                await ctx.send(f"Last Activity readings:\n{activities_final_table}")
                await ctx.send(f"Last five Achievement readings:\n{achievements_final_table}")

            #if returnStatus[0][0] does not return one, return below
            else:

                await ctx.send(f"Data for {checkPlayerName} is missing from database. Return Status: {databaseCheck}.")

        else:
            await ctx.send("Error: Violation of input criteria. Only characters Aa-Zz, 0-9, and symbols '-, _, +' are allowed.")

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

        if userCheckInputString_p1[0] == 1 and userCheckInputString_p2[0] == 1:

            checkPlayerName_p1 = userCheckInputString_p1[1]
            checkPlayerName_p2 = userCheckInputString_p2[1]

            #requesting data from DONE_Lookup_PlayerCurrentCompare.compareCurrentPlayerStatus
            databaseCheck_p1 = commandInputChecker.checkDatabasePresence(checkPlayerName_p1)
            databaseCheck_p2 = commandInputChecker.checkDatabasePresence(checkPlayerName_p2)

            databaseCheckCount_p1 = databaseCheck_p1[0] + databaseCheck_p1[1] + databaseCheck_p1[2] + databaseCheck_p1[3]
            databaseCheckCount_p2 = databaseCheck_p2[0] + databaseCheck_p2[1] + databaseCheck_p2[2] + databaseCheck_p2[3]
            
            #checks if Status dataframe contains data. If it does contain data, return pCurrentCompare
            if databaseCheckCount_p1 == 4 and databaseCheckCount_p2 == 4:

                #date for invoking Lookup_PlayerCurrentCompare
                lookupInvokeDate = datetime.date.today()

                #creating table to compare both player's combat level and quest progression using returnStatus
                returnStatus = Lookup_PlayerCurrentCompare.compareCurrentPlayerStatus(checkPlayerName_p1, checkPlayerName_p2, lookupInvokeDate)
                status_string = returnStatus[1].to_string()
                status_final_table = (f"```\n{status_string}\n```")

                #creating table to compare both player's skills using returnHiscores
                returnHiscores = Lookup_PlayerCurrentCompare.compareCurrentPlayerSkills(checkPlayerName_p1, checkPlayerName_p2, lookupInvokeDate)
                hiscores_string = returnHiscores[1].to_string()
                hiscores_final_table = (f"```\n{hiscores_string}\n```")

                #creating table to compare both player's activities using returnActivities
                returnActivities = Lookup_PlayerCurrentCompare.compareCurrentPlayerActivities(checkPlayerName_p1, checkPlayerName_p2, lookupInvokeDate)
                activities_string = returnActivities[1].to_string()
                activities_final_table = (f"```\n{activities_string}\n```")
                
                #creating table to compare number of achievements/event logs recorded in last 30 days using returnAchievements
                returnAchievements = Lookup_PlayerCurrentCompare.compareLast30daysPlayerAchievements(checkPlayerName_p1, checkPlayerName_p2, lookupInvokeDate)
                achievements_string = returnAchievements[1].to_string()
                achievements_final_table = (f"```\n{achievements_string}\n```")

                await ctx.send(f"Overview for '{checkPlayerName_p1}' and '{checkPlayerName_p2}'.")
                await ctx.send(f"Latest Status readings:\n{status_final_table}")
                await ctx.send(f"Latest Hiscore readings:\n{hiscores_final_table}")
                await ctx.send(f"Latest Activity readings:\n{activities_final_table}")
                await ctx.send(f"Latest Achievement readings:\n{achievements_final_table}")
            
            #if data missing for P1, return below
            elif databaseCheckCount_p1 < 4 and databaseCheckCount_p2 == 4:
                await ctx.send(f"Error: Data for {checkPlayerName_p1} is missing from database. Return Status for {checkPlayerName_p1}: {databaseCheck_p1}.")

            #if data missing for P2, return below
            elif databaseCheckCount_p1 == 4 and databaseCheckCount_p2 < 4:
                await ctx.send(f"Error: Data for {checkPlayerName_p2} is missing from database. Return Status for {checkPlayerName_p2}: {databaseCheck_p2}.")

            #return below if data is missing for both P1 and P2
            else:
                await ctx.send(f"Error: Data for both players ('{checkPlayerName_p1}' and '{checkPlayerName_p2}') is missing from database. Return Status for {checkPlayerName_p1}: {databaseCheck_p1}. Return Status for {checkPlayerName_p2}: {databaseCheck_p2}.")

        else:
            await ctx.send("Error: Violation of input criteria. Only characters Aa-Zz and 0-9 are allowed.")

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