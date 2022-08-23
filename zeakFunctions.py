import gspread
import pandas as pd
from config import *

# Import perks google sheets as dataframe
sa = gspread.service_account(filename='service_account.json')
sh = sa.open(GOOGLE_SHEET)

def raid_scrape(msg):
    wks = sh.worksheet('Raid Msg')
    zeak_df = pd.DataFrame(wks.get_all_records())
    
    msg = msg.lower()
    subMsg = zeak_df.loc[zeak_df['Command'] == msg, 'Subs'].values[0]
    freeMsg = zeak_df.loc[zeak_df['Command'] == msg, 'Free'].values[0]

    return subMsg, freeMsg