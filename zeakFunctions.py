import gspread
import pandas as pd
from config import *
import random
from itertools import cycle

# Import perks google sheets as dataframe
sa = gspread.service_account(filename='service_account.json')
sh = sa.open(GOOGLE_SHEET)

lurkMsg = 'lurks away to be comfy in their blanket zeakthComfy Thanks for the support'
zeakBotMsg = "Here are the commands that you can ask me, try typing help after the command to get more details! !perk, !status, !shrine, !survivors, !killers, !stats, !unique"

discordMsg = "Come join Zeak's husky house! Get notified when I go live and vibe with cool people. 18+ only please. https://discord.gg/MM9UKbqJpV zeakthDance"
twitterMsg = "Need some funny memes or want to know when I go live? Follow me at https://twitter.com/ZeakTheHusky zeakthLove"
tiktokMsg = "Want to check out some classic moments from stream? Follow me at https://www.tiktok.com/@zeakthehusky zeakthLUL"
socialsMsg = "Want to follow Zeak in every possible way? Try !discord, !twitter, !tiktok, or check out his linktree at https://linktr.ee/ZeakTheHusky zeakthBoop"

vcMsg = "To join voice chat, Zeak would need to at least game in vc with you once off stream. Feel free to join the discord, a bunch of off stream games happen there! 18+ only please. https://discord.gg/MM9UKbqJpV zeakthDance"
fcMsg1 = "Zeak's Steam friend code is 165494960 and his DBD friend code is ZeakTheHusky.TTV#92e6"
fcMsg2 = "Zeak's DBD friend code is ZeakTheHusky.TTV#92e6"

qMsg = "Zeak will regularly ask rhetorical questions and talk to himself about the game. Please do not answer these questions unless Zeak SPECIFICALLY asks chat. You will get warned and then timed out. This rule is for PvE/Story based games"
spoilerMsg = "Please do not spoil or explain game mechanics unless explicitly asked by Zeak."
bsMsg = "Please do not backseat Zeak, let him suffer through his struggles! zeakthSad"
ttvMsg = "Looks like there's a TTV in our lobby, if they are live and you wanna see from their perspective, please be kind and respectful no matter what zeakthLove"
raidersMsg = "Welcome on in raiders! If you'd like to help out our Husky's metrics, you can come in as a viewer by hitting refresh or clicking on ZeakTheHusky profile twice to avoid the ads! zeakthLove"
ageMsg = "Hey guys, even though it's not against TOS to reveal age, please refrain from doing so here. If you reveal you are under 18, you will be immediately banned."

jamMsg = "Dance Dance AsterBongo catJAM zeakthDance zeakthDance AsterBongo dogJAM Dance Dance"

def heartRand():
    emotes = ['zeakthLove', 'zeakthPride']
    heart = random.choice(emotes)
    return(heart)

def alternate():
    while True:
        yield 0
        yield 1

def raid_scrape(msg):
    wks = sh.worksheet('Raid Msg')
    zeak_df = pd.DataFrame(wks.get_all_records())
    
    msg = msg.lower()
    subMsg = zeak_df.loc[zeak_df['Command'] == msg, 'Subs'].values[0]
    freeMsg = zeak_df.loc[zeak_df['Command'] == msg, 'Free'].values[0]

    return subMsg, freeMsg

def clip_scrape(msg):
    wks = sh.worksheet('Clips')
    
    clipRow = wks.find(msg).row
    clipLink = wks.cell(clipRow, 2).value

    return clipLink

def clip_rand():
    wks = sh.worksheet('Clips')
    
    clipCnt = len(wks.col_values(1))

    clipRow = random.randrange(2, clipCnt)
    clipLink = wks.cell(clipRow, 2).value

    return clipLink

def usrInc(user, col):
    wks = sh.worksheet('Counts')
    
    match col:
        case 'ban':
            try:
                usrRow = wks.find(user).row

                usrCnt = int(wks.cell(usrRow,2).value)
                usrCnt += 1

                wks.update_cell(usrRow, 2, usrCnt)

            except:
                lastRow = len(wks.get_all_values()) + 1
                wks.update_cell(lastRow, 1, user)
                wks.update_cell(lastRow, 2, 1)
                wks.update_cell(lastRow, 3, 0)
                wks.update_cell(lastRow, 4, 0)

                usrCnt = 1
        case 'boop':
            try:
                usrRow = wks.find(user).row

                usrCnt = int(wks.cell(usrRow,3).value)
                usrCnt += 1

                wks.update_cell(usrRow, 3, usrCnt)

            except:
                lastRow = len(wks.get_all_values()) + 1
                wks.update_cell(lastRow, 1, user)
                wks.update_cell(lastRow, 3, 1)
                wks.update_cell(lastRow, 2, 0)
                wks.update_cell(lastRow, 4, 0)

                usrCnt = 1

        case 'hug':
            try:
                usrRow = wks.find(user).row

                usrCnt = int(wks.cell(usrRow,4).value)
                usrCnt += 1

                wks.update_cell(usrRow, 4, usrCnt)

            except:
                lastRow = len(wks.get_all_values()) + 1
                wks.update_cell(lastRow, 1, user)
                wks.update_cell(lastRow, 4, 1)
                wks.update_cell(lastRow, 2, 0)
                wks.update_cell(lastRow, 3, 0)

                usrCnt = 1

        case 'himbo':
            usrRow = wks.find(user).row

            usrCnt = int(wks.cell(usrRow,5).value)
            usrCnt += 1

            wks.update_cell(usrRow, 5, usrCnt)

        case 'piss':
            usrRow = wks.find(user).row

            usrCnt = int(wks.cell(usrRow,6).value)
            usrCnt += 1

            wks.update_cell(usrRow, 6, usrCnt)

    return usrCnt

def usrCnt(user, col):
    wks = sh.worksheet('Counts')
    
    match col:
        case 'ban':
            try:
                usrRow = wks.find(user).row

                usrCnt = int(wks.cell(usrRow,2).value)

            except:
                usrCnt = 0

        case 'boop':
            try:
                usrRow = wks.find(user).row

                usrCnt = int(wks.cell(usrRow,3).value)

            except:
                usrCnt = 0
        
        case 'hug':
            try:
                usrRow = wks.find(user).row

                usrCnt = int(wks.cell(usrRow,4).value)

            except:
                usrCnt = 0

        case 'himbo':
            usrRow = wks.find(user).row

            usrCnt = int(wks.cell(usrRow,5).value)

        case 'piss':
            usrRow = wks.find(user).row

            usrCnt = int(wks.cell(usrRow,6).value)

    return usrCnt

def himboSet(himboNum):
    wks = sh.worksheet('Counts')

    user = 'ZeakTheHusky'

    usrRow = wks.find(user).row

    wks.update_cell(usrRow, 5, himboNum)