import gspread
import pandas as pd
from config import *
import random

# Import perks google sheets as dataframe
sa = gspread.service_account(filename='service_account.json')
sh = sa.open(GOOGLE_SHEET)

lurkMsg = 'lurks away to be comfy in their blanket zeakthComfy Thanks for the support'
zeakBotMsg = "Here are the commands that you can ask me, try typing help after the command to get more details! !perk, !status, !shrine, !survivors, !killers, !stats, !unique"

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