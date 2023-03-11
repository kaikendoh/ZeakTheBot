import gspread
import pandas as pd
from config import *
import random

# Import perks google sheets as dataframe
sa = gspread.service_account(filename='service_account.json')
sh = sa.open(GOOGLE_SHEET)

lurkMsg = 'lurks away to be comfy in their blanket zeakthComfy Thanks for the support'
zeakBotMsg = "Here are the commands that you can ask me, try typing help after the command to get more details! !perk, !status, !shrine, !survivors, !killers, !stats, !unique"

discordMsg = "Come join Zeak's husky house! Get notified when I go live and vibe with cool people. 18+ only please. https://discord.gg/MM9UKbqJpV zeakthDance"
twitterMsg = "Need some funny memes or want to know when I go live? Follow me at https://twitter.com/ZeakTheHusky zeakthLove"
tiktokMsg = "Want to check out some classic moments from stream? Follow me at https://www.tiktok.com/@zeakthehusky zeakthLUL"

vcMsg = "To join voice chat, Zeak would need to at least game in vc with you once off stream. Feel free to join the discord, a bunch of off stream games happen there! 18+ only please. https://discord.gg/MM9UKbqJpV zeakthDance"
fcMsg1 = "Zeak's Steam friend code is 165494960 and his DBD friend code is ZeakTheHusky.TTV#92e6"
fcMsg2 = "Zeak's DBD friend code is ZeakTheHusky.TTV#92e6"

def heartRand():
    emotes = ['zeakthLove', 'zeakthPride']
    heart = random.choice(emotes)
    return(heart)

def raid_scrape(msg):
    wks = sh.worksheet('Raid Msg')
    zeak_df = pd.DataFrame(wks.get_all_records())
    
    msg = msg.lower()
    subMsg = zeak_df.loc[zeak_df['Command'] == msg, 'Subs'].values[0]
    freeMsg = zeak_df.loc[zeak_df['Command'] == msg, 'Free'].values[0]

    return subMsg, freeMsg

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

                usrCnt = 1

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

    return usrCnt