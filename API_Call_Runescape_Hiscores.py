#import module to create API calls
import requests

#blabla

#import module to create db connection to postgres, and insert records
import psycopg2

#import module to create datetime timestamp
import datetime

#import os to use dotenv
import os

#import dotenv modules to import db credentials
from dotenv import load_dotenv, dotenv_values

#load dotenv file with db credentials
load_dotenv()

#list db credentials
db_database = os.getenv("db_database")
db_user = os.getenv("db_user")
db_password = os.getenv("db_password")
db_hostname = os.getenv("db_hostname")
db_port_id = os.getenv("db_port_id")

conn = None
cur = None

try:
    #connect to db
    conn = psycopg2.connect(
        database = db_database,
        user = db_user,
        password = db_password,
        host = db_hostname,
        port = db_port_id
    )

    #create cursor
    cursor = conn.cursor()

    #retrieve list of usernames that need to be looked up from db
    fetch_playerNames_query = "SELECT player_name FROM main_runescape_tracked_usernames"

    #execute query
    cursor.execute(fetch_playerNames_query)

    #list fetched playernames
    fetchedPlayerNames = cursor.fetchall()

    #close cursor and connection
    cursor.close()
    conn.close()

    #for loop for every fetchedPlayerName in list
    for fetchedPlayerName in fetchedPlayerNames:
        username = fetchedPlayerName[0]
        
        print('-------------New record extracted-------------')
        print('\n')
        print("Records retrieved for: " + username)

        #creating datetime timestamp
        current_date_timestamp = datetime.datetime.now()

        #creatine datestamp
        current_date = datetime.date.today()

        #setting parameters for API link (player name)
        playerName = username
        paramPlayerName = {
            "player": {playerName}
        }
        
        #creating API request
        response = requests.get('https://secure.runescape.com/m=hiscore/index_lite.ws?', params=paramPlayerName)
        print(response.status_code)

        #print url used for API request, based on link + parameters
        print("URL used for API call: " + response.url)
        print('\n')

        #replaceing linebreak of unicode excerpts with commas
        lbremoved = response.text.replace('\n', ",")

        #splitting unicode into list by using comma in text string as split location
        splitResponse = lbremoved.split(',')

        #skills - defining python objects by indicating location in list, followed by printing object to check if defined properly
        overallRank = splitResponse[0]
        overallLevel = splitResponse[1]
        overallExp = splitResponse[2]
        attackRank = splitResponse[3]
        attackLevel = splitResponse[4]
        attackExp = splitResponse[5]
        defenceRank = splitResponse[6]
        defenceLevel = splitResponse[7]
        defenceExp = splitResponse[8]
        strengthRank = splitResponse[9]
        strengthLevel = splitResponse[10]
        strengthExp = splitResponse[11]
        constitutionRank = splitResponse[12]
        constitutionLevel = splitResponse[13]
        constitutionExp = splitResponse[14]
        rangedRank = splitResponse[15]
        rangedLevel = splitResponse[16]
        rangedExp = splitResponse[17]
        prayerRank = splitResponse[18]
        prayerLevel = splitResponse[19]
        prayerExp = splitResponse[20]
        magicRank = splitResponse[21]
        magicLevel = splitResponse[22]
        magicExp = splitResponse[23]
        cookingRank = splitResponse[24]
        cookingLevel = splitResponse[25]
        cookingExp = splitResponse[26]
        woodcuttingRank = splitResponse[27]
        woodcuttingLevel = splitResponse[28]
        woodcuttingExp = splitResponse[29]
        fletchingRank = splitResponse[30]
        fletchingLevel = splitResponse[31]
        fletchingExp = splitResponse[32]
        fishingRank = splitResponse[33]
        fishingLevel = splitResponse[34]
        fishingExp = splitResponse[35]
        firemakingRank = splitResponse[36]
        firemakingLevel = splitResponse[37]
        firemakingExp = splitResponse[38]
        craftingRank = splitResponse[39]
        craftingLevel = splitResponse[40]
        craftingExp = splitResponse[41]
        smithingRank = splitResponse[42]
        smithingLevel = splitResponse[43]
        smithingExp = splitResponse[44]
        miningRank = splitResponse[45]
        miningLevel = splitResponse[46]
        miningExp = splitResponse[47]
        herbloreRank = splitResponse[48]
        herbloreLevel = splitResponse[49]
        herbloreExp = splitResponse[50]
        agilityRank = splitResponse[51]
        agilityLevel = splitResponse[52]
        agilityExp = splitResponse[53]
        thievingRank = splitResponse[54]
        thievingLevel = splitResponse[55]
        thievingExp = splitResponse[56]
        slayerRank = splitResponse[57]
        slayerLevel = splitResponse[58]
        slayerExp = splitResponse[59]
        farmingRank = splitResponse[60]
        farmingLevel = splitResponse[61]
        farmingExp = splitResponse[62]
        runecraftingRank = splitResponse[63]
        runecraftingLevel = splitResponse[64]
        runecraftingExp = splitResponse[65]
        hunterRank = splitResponse[66]
        hunterLevel = splitResponse[67]
        hunterExp = splitResponse[68]
        constructionRank = splitResponse[69]
        constructionLevel = splitResponse[70]
        constructionExp = splitResponse[71]
        summoningRank = splitResponse[72]
        summoningLevel = splitResponse[73]
        summoningExp = splitResponse[74]
        dungeoneeringRank = splitResponse[75]
        dungeoneeringLevel = splitResponse[76]
        dungeoneeringExp = splitResponse[77]
        divinationRank = splitResponse[78]
        divinationLevel = splitResponse[79]
        divinationExp = splitResponse[80]
        inventionRank = splitResponse[81]
        inventionLevel = splitResponse[82]
        inventionExp = splitResponse[83]
        archaeologyRank = splitResponse[84]
        archaeologyLevel = splitResponse[85]
        archaeologyExp = splitResponse[86]
        necromancyRank = splitResponse[87]
        necromancyLevel = splitResponse[88]
        necromancyExp = splitResponse[89]

        #achievements - defining python objects by indicating location in list, followed by printing object to check if defined properly
        bountyHunterRank = splitResponse[90]
        bountyHunterTotal = splitResponse[91]
        bountyHunterRoguesRank = splitResponse[92]
        bountyHunterRoguesTotal = splitResponse[93]
        dominionTowerRank = splitResponse[94]
        dominionTowerTotal = splitResponse[95]
        theCrucibleRank = splitResponse[96]
        theCrucibleTotal = splitResponse[97]
        castleWarsRank = splitResponse[98]
        castleWarsTotal = splitResponse[99]
        barbarianAssaultAttackersRank = splitResponse[100]
        barbarianAssaultAttackersTotal = splitResponse[101]
        barbarianAssaultDefendersRank = splitResponse[102]
        barbarianAssaultDefendersTotal = splitResponse[103]
        barbarianAssaultCollectorsRank = splitResponse[104]
        barbarianAssaultCollectorsTotal = splitResponse[105]
        barbarianAssaultHealersRank = splitResponse[106]
        barbarianAssaultHealersTotal = splitResponse[107]
        duelTournamentRank = splitResponse[108]
        duelTournamentTotal = splitResponse[109]
        mobilisingArmiesRank = splitResponse[110]
        mobilisingArmiesTotal = splitResponse[111]
        conquestRank = splitResponse[112]
        conquestTotal = splitResponse[113]
        fistOfGuthixRank = splitResponse[114]
        fistOfGuthixTotal = splitResponse[115]
        ggAthleticsRank = splitResponse[116]
        ggAthleticsTotal = splitResponse[117]
        ggResourceRaceRank = splitResponse[118]
        ggResourceRaceTotal = splitResponse[119]
        we2ArmadylLifetimeContributionRank = splitResponse[120]
        we2ArmadylLifetimeContributionTotal = splitResponse[121]
        we2BandosLifetimeContributionRank = splitResponse[122]
        we2BandoslLifetimeContributionTotal = splitResponse[123]
        we2ArmadylPVPkillsRank = splitResponse[124]
        we2ArmadylPVPkillsTotal = splitResponse[125]
        we2BandosPVPkillsRank = splitResponse[126]
        we2BandosPVPkillsTotal = splitResponse[127]
        heistGuardLevelRank = splitResponse[128]
        heistGuardLevelTotal = splitResponse[129]
        heistRobberLevelRank = splitResponse[130]
        heistRobberLevelTotal = splitResponse[131]
        cfp5gameAverageRank = splitResponse[132]
        cfp5gameAverageTotal = splitResponse[133]
        af15cowTippingRank = splitResponse[134]
        af15cowTippingTotal = splitResponse[135]
        af15ratsKilledRank = splitResponse[136]
        af15ratsKilledTotal = splitResponse[137]
        runescoreRank = splitResponse[138]
        runescoreTotal = splitResponse[139]
        clueScrollsEasyRank = splitResponse[140]
        clueScrollsEasyTotal = splitResponse[141]
        clueScrollsMediumRank = splitResponse[142]
        clueScrollsMediumTotal = splitResponse[143]
        clueScrollsHardRank = splitResponse[144]
        clueScrollsHardTotal = splitResponse[145]
        clueScrollsEliteRank = splitResponse[146]
        clueScrollsEliteTotal = splitResponse[147]
        clueScrollsMasterRank = splitResponse[148]
        clueScrollsMasterTotal = splitResponse[149]

        #connect to DB
        try:
            conn = psycopg2.connect(
                host = db_hostname,
                dbname = db_database,
                user = db_user,
                password = db_password,
                port = db_port_id
            )

            #cursor needs to be created in order to navigate and interact with DB
            cur = conn.cursor()

            #inserting values into hiscores table
            insert_script_hiscores = 'INSERT INTO main_runescape_hiscores (datesync_date, datesync_datetime, player_name, skill, rank, level, experience) VALUES (%s, %s, %s, %s, %s, %s, %s)'
            insert_values_hiscores = [(current_date, current_date_timestamp, playerName, 'Overall', overallRank, overallLevel, overallExp),
                                    (current_date, current_date_timestamp, playerName, 'Attack', attackRank, attackLevel, attackExp),
                                    (current_date, current_date_timestamp, playerName, 'Defence', defenceRank, defenceLevel, defenceExp),
                                    (current_date, current_date_timestamp, playerName, 'Strength', strengthRank, strengthLevel, strengthExp),
                                    (current_date, current_date_timestamp, playerName, 'Constitution', constitutionRank, constitutionLevel, constitutionExp),
                                    (current_date, current_date_timestamp, playerName, 'Ranged', rangedRank, rangedLevel, rangedExp),
                                    (current_date, current_date_timestamp, playerName, 'Prayer', prayerRank, prayerLevel, prayerExp),
                                    (current_date, current_date_timestamp, playerName, 'Magic', magicRank, magicLevel, magicExp),
                                    (current_date, current_date_timestamp, playerName, 'Cooking', cookingRank, cookingLevel, cookingExp),
                                    (current_date, current_date_timestamp, playerName, 'Woodcutting', woodcuttingRank, woodcuttingLevel, woodcuttingExp),
                                    (current_date, current_date_timestamp, playerName, 'Fletching', fletchingRank, fletchingLevel, fletchingExp),
                                    (current_date, current_date_timestamp, playerName, 'Fishing', fishingRank, fishingLevel, fishingExp),
                                    (current_date, current_date_timestamp, playerName, 'Firemaking', firemakingRank, firemakingLevel, firemakingExp),
                                    (current_date, current_date_timestamp, playerName, 'Crafting', craftingRank, craftingLevel, craftingExp),
                                    (current_date, current_date_timestamp, playerName, 'Smithing', smithingRank, smithingLevel, smithingExp),
                                    (current_date, current_date_timestamp, playerName, 'Mining', miningRank, miningLevel, miningExp),
                                    (current_date, current_date_timestamp, playerName, 'Herblore', herbloreRank, herbloreLevel, herbloreExp),
                                    (current_date, current_date_timestamp, playerName, 'Agility', agilityRank, agilityLevel, agilityExp),
                                    (current_date, current_date_timestamp, playerName, 'Thieving', thievingRank, thievingLevel, thievingExp),
                                    (current_date, current_date_timestamp, playerName, 'Slayer', slayerRank, slayerLevel, slayerExp),
                                    (current_date, current_date_timestamp, playerName, 'Farming', farmingRank, farmingLevel, farmingExp),
                                    (current_date, current_date_timestamp, playerName, 'Runecrafting', runecraftingRank, runecraftingLevel, runecraftingExp),
                                    (current_date, current_date_timestamp, playerName, 'Hunter', hunterRank, hunterLevel, hunterExp),
                                    (current_date, current_date_timestamp, playerName, 'Construction', constructionRank, constructionLevel, constructionExp),
                                    (current_date, current_date_timestamp, playerName, 'Summoning', summoningRank, summoningLevel, summoningExp),
                                    (current_date, current_date_timestamp, playerName, 'Dungeoneering', dungeoneeringRank, dungeoneeringLevel, dungeoneeringExp),
                                    (current_date, current_date_timestamp, playerName, 'Divination', divinationRank, divinationLevel, divinationExp),
                                    (current_date, current_date_timestamp, playerName, 'Invention', inventionRank, inventionLevel, inventionExp),
                                    (current_date, current_date_timestamp, playerName, 'Archaeology', archaeologyRank, archaeologyLevel, archaeologyExp),
                                    (current_date, current_date_timestamp, playerName, 'Necromancy', necromancyRank, necromancyLevel, necromancyExp)]
            for record in insert_values_hiscores:
                cur.execute(insert_script_hiscores, record)

            #inserting values into achievements table
            insert_script_achievements = 'INSERT INTO main_runescape_achievements (datesync_date, datesync_datetime, player_name, activity, rank, score) VALUES (%s, %s, %s, %s, %s, %s)'
            insert_values_achievements = [(current_date, current_date_timestamp, playerName, 'Bounty Hunters', bountyHunterRank, bountyHunterTotal),
                                        (current_date, current_date_timestamp, playerName, 'B.H. Rogues', bountyHunterRoguesRank, bountyHunterRoguesTotal),
                                        (current_date, current_date_timestamp, playerName, 'Dominion tower', dominionTowerRank, dominionTowerTotal),
                                        (current_date, current_date_timestamp, playerName, 'The Crucible', theCrucibleRank, theCrucibleTotal),
                                        (current_date, current_date_timestamp, playerName, 'Castle Wars Games', castleWarsRank, castleWarsTotal),
                                        (current_date, current_date_timestamp, playerName, 'B.A. Attackers', barbarianAssaultAttackersRank, barbarianAssaultAttackersTotal),
                                        (current_date, current_date_timestamp, playerName, 'B.A. Defenders', barbarianAssaultDefendersRank, barbarianAssaultDefendersTotal),
                                        (current_date, current_date_timestamp, playerName, 'B.A. Collectors', barbarianAssaultCollectorsRank, barbarianAssaultCollectorsTotal),
                                        (current_date, current_date_timestamp, playerName, 'B.A. Healers', barbarianAssaultHealersRank, barbarianAssaultHealersTotal),
                                        (current_date, current_date_timestamp, playerName, 'Duel Tournament', duelTournamentRank, duelTournamentTotal),
                                        (current_date, current_date_timestamp, playerName, 'Mobilising Armies', mobilisingArmiesRank, mobilisingArmiesTotal),
                                        (current_date, current_date_timestamp, playerName, 'Conquest', conquestRank, conquestRank),
                                        (current_date, current_date_timestamp, playerName, 'Fist of Guthix', fistOfGuthixRank, fistOfGuthixTotal),
                                        (current_date, current_date_timestamp, playerName, 'GG: Resource Race', ggResourceRaceRank, ggResourceRaceTotal),
                                        (current_date, current_date_timestamp, playerName, 'GG: Athletics', ggAthleticsRank, ggAthleticsTotal),
                                        (current_date, current_date_timestamp, playerName, 'WE2: Armadyl Lifetime Contribution', we2ArmadylLifetimeContributionRank, we2ArmadylLifetimeContributionTotal),
                                        (current_date, current_date_timestamp, playerName, 'WE2: Bandos Lifetime Contribution', we2BandosLifetimeContributionRank, we2BandoslLifetimeContributionTotal),
                                        (current_date, current_date_timestamp, playerName, 'WE2: Armadyl PvP Kills', we2ArmadylPVPkillsRank, we2ArmadylPVPkillsTotal),
                                        (current_date, current_date_timestamp, playerName, 'WE2: Bandos PvP Kills', we2BandosPVPkillsRank, we2BandosPVPkillsTotal),
                                        (current_date, current_date_timestamp, playerName, 'Heist Guard Level', heistGuardLevelRank, heistGuardLevelTotal),
                                        (current_date, current_date_timestamp, playerName, 'Heist Robber Level', heistRobberLevelRank, heistRobberLevelTotal),
                                        (current_date, current_date_timestamp, playerName, 'CFP: 5 Game Average', cfp5gameAverageRank, cfp5gameAverageTotal),
                                        (current_date, current_date_timestamp, playerName, 'RuneScore', runescoreRank, runescoreTotal),
                                        (current_date, current_date_timestamp, playerName, 'Clue Scrolls (easy)', clueScrollsEasyRank, clueScrollsEasyTotal),
                                        (current_date, current_date_timestamp, playerName, 'Clue Scrolls (medium)', clueScrollsMediumRank, clueScrollsMediumTotal),
                                        (current_date, current_date_timestamp, playerName, 'Clue Scrolls (hard)', clueScrollsHardRank, clueScrollsHardTotal),
                                        (current_date, current_date_timestamp, playerName, 'Clue Scrolls (elite)', clueScrollsEliteRank, clueScrollsEliteTotal),
                                        (current_date, current_date_timestamp, playerName, 'Clue Scrolls (master)', clueScrollsMasterRank, clueScrollsMasterTotal)]
            for record in insert_values_achievements:
                cur.execute(insert_script_achievements, record)

            #committing updates to tables
            conn.commit()

        except Exception as error_1:
            print(error_1)

        #creating lines to at all times close DB cursor and connection
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()

except Exception as error_2:
    print(error_2)

#creating lines to at all times close DB cursor and connection
finally:
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()