from bs4 import BeautifulSoup
import requests
import re
import gspread
import pandas as pd
import random
from config import *

# Import perks google sheets as dataframe
sa = gspread.service_account(filename='service_account.json')
sh = sa.open(GOOGLE_SHEET)

perkhelp = 'Try typing !perk <perk name> to get a description of the perk. ie "!perk spine chill"'
statushelp = 'Try typing !status <status name> to get a description of the status. ie "!status exhausted"'
namehelp = 'Try typing !stats <killer name> to get a summary of that particular killer. ie "!stats trapper"'
uniquehelp = 'Try typing !unique <killer/survivor name> to get the unique perks of that particular killer or survivor. ie "!unique artist"'

# Function to change the case of perk to capitalize the first letter
# except for certain words
def case_except(s):
    exceptions = ['a', 'an', 'of', 'the', 'is', 'for', 'de', 'from', 'with']
    word_list = re.split(' ', s)
    final = [word_list[0].capitalize()]
    for word in word_list[1:]:
        final.append(word if word in exceptions else word.capitalize())
    return " ".join(final)

# Function to grab the current perks in the Shrine of Secrets and when it will refresh
def shrine_scrape():

    url = "https://deadbydaylight.fandom.com/wiki/Dead_by_Daylight_Wiki"

    response = requests.get(url)
    webpage = response.content

    soup = BeautifulSoup(webpage, 'html.parser')

    sos = soup.find_all('div', class_='sosPerkDescName')
    sos_list = []

    for i in range(len(sos)):
        sos_list.append(sos[i].get_text(separator=' ', strip=True))

    sos_s = ', '.join(sos_list)
    sos_time = soup.find('span', class_='luaClr clr clr4').get_text()
    
    return sos_s, sos_time

# Function to grab all the current killers from dbd fandom wiki
def killer_scrape():

    url = "https://deadbydaylight.fandom.com/wiki/Dead_by_Daylight_Wiki"

    response = requests.get(url)
    webpage = response.content

    soup = BeautifulSoup(webpage, 'html.parser')

    killers = soup.find_all('div', id='fpkiller')[0].get_text(', ', strip=True)[14:]
    
    return killers

# Function to grab all the current survivor names from dbd fandom wiki
def survivor_scrape():

    url = "https://deadbydaylight.fandom.com/wiki/Dead_by_Daylight_Wiki"

    response = requests.get(url)
    webpage = response.content

    soup = BeautifulSoup(webpage, 'html.parser')

    survivors = soup.find_all('div', id='fpsurvivors')[0].get_text(', ', strip=True)[16:]
    
    return survivors

# Function to scrape the perk from the dbd fandom wiki
def perk_scrape(perk):
    wks = sh.worksheet('Names')
    perks_df = pd.DataFrame(wks.get_all_records())

    memewks = sh.worksheet('Memes')
    meme_df = pd.DataFrame(memewks.get_all_records())

    if perks_df['name'].eq(perk).any():
        perkurl = perks_df.loc[perks_df['name'] == perk, 'url'].values[0]
    
    elif meme_df['Lookup'].eq(perk).any():
        memeRow = memewks.find(perk).row
        perk_name = memewks.cell(memeRow,2).value
        perk_desc = memewks.cell(memeRow,3).value
        
        return perk_name, perk_desc
    else:
        perkurl = case_except(perk).strip().replace(" ", "_")

    url = "https://deadbydaylight.fandom.com/wiki/{a}".format(a=perkurl)

    response = requests.get(url)
    webpage = response.content

    soup = BeautifulSoup(webpage, 'html.parser')

    perk_name = soup.find('h1').get_text(strip=True)
    perk_desc = soup.find('div', class_='formattedPerkDesc').get_text(separator=' ', strip=True).replace('\n', '')

    return perk_name, perk_desc

# Function to scrape the status from the dbd fandom wiki
def status_scrape(status):
    status = status.capitalize()

    url = "https://deadbydaylight.fandom.com/wiki/Status_HUD"
    response = requests.get(url)
    webpage = response.content

    soup = BeautifulSoup(webpage, "html.parser")

    status_all = soup.find_all('td')

    status_list = []
    status_name = []

    for i in range(len(status_all)):
        status_list.append(status_all[i].get_text(separator=' ', strip=True))
        try:
            status_name.append(re.search('The (.*?) Status', status_list[i]).group(1))
        except:
            status_name.append(status_list[i])

    status_df = pd.DataFrame({'status_name': status_name, 'status_desc': status_list})
    
    status_desc = status_df.loc[status_df['status_name'] == status, 'status_desc'].values[0]

    return status, status_desc

# Function to scrape the status from the dbd fandom wiki
def stats_scrape(name):
    wks = sh.worksheet('Names')
    names_df = pd.DataFrame(wks.get_all_records())

    if names_df['name'].eq(name).any():
        nameurl = names_df.loc[names_df['name'] == name.lower(), 'url'].values[0]
    else:
        nameurl = case_except(name).strip().replace(" ", "_")

    url = "https://deadbydaylight.fandom.com/wiki/{a}".format(a=nameurl)

    response = requests.get(url)
    webpage = response.content

    soup = BeautifulSoup(webpage, 'html.parser')

    title = soup.find_all('table', class_='infoboxtable')[0].find_all('th', class_='center bold')[0].get_text(separator=' ', strip=True)
    title = re.sub(' +', ' ', title)
    
    try:
        name_index = td_scrape(soup, 'Name')
        name = soup.find_all('td', class_='valueColumn')[name_index].get_text(separator=' ', strip=True).replace('\n', '')
    except:
        name = "None"

    radius_index = td_scrape(soup, 'Terror Radius')
    radius = soup.find_all('td', class_='valueColumn')[radius_index].get_text(separator=' ', strip=True).replace('\n', '')

    mv_index = td_scrape(soup, 'Movement Speed')
    mv = soup.find_all('td', class_='valueColumn')[mv_index].get_text(separator=' ', strip=True).replace('\xa0', '').replace(' | ','-')

    try:
        amv_index = td_scrape(soup, 'Alternate Movement speed')
        amv = soup.find_all('td', class_='valueColumn')[amv_index].get_text(separator=' ', strip=True).replace('\xa0', '').replace(' | ','-')

    except:
        summary = f"Title: {title} || Name: {name} || Terror Radius: {radius} || Movement Speed: {mv}"
        return summary

    summary = f"Title: {title} || Name: {name} || Terror Radius: {radius} || Movement Speed: {mv}, {amv}"

    return summary

def td_scrape(soup, title):
    titles = soup.find_all('td', class_='titleColumn')
    titles_strip = [x.get_text(separator=' ', strip=True).replace('\n', '') for x in titles]

    col_index = titles_strip.index(title)

    return col_index

def u_perks(name):
    wks = sh.worksheet('Names')
    names_df = pd.DataFrame(wks.get_all_records())

    if names_df['name'].eq(name).any():
        nameurl = names_df.loc[names_df['name'] == name.lower(), 'url'].values[0]
    else:
        nameurl = case_except(name).strip().replace(" ", "_")

    url = "https://deadbydaylight.fandom.com/wiki/{a}".format(a=nameurl)

    response = requests.get(url)
    webpage = response.content

    soup = BeautifulSoup(webpage, 'html.parser')

    name = soup.find_all('table', class_='infoboxtable')[0].find_all('th', class_='center bold')[0].get_text(separator=' ', strip=True)

    perk1 = soup.find_all('table', class_='wikitable')[0].find_all('th')[1].get_text(strip=True)
    perk2 = soup.find_all('table', class_='wikitable')[0].find_all('th')[3].get_text(strip=True)
    perk3 = soup.find_all('table', class_='wikitable')[0].find_all('th')[5].get_text(strip=True)

    perks = f"{name}'s unique perks are: {perk1}, {perk2}, and {perk3}."

    return perks

def randTrivia():
    k_url = "https://deadbydaylight.fandom.com/wiki/Category:Killers"
    s_url = "https://deadbydaylight.fandom.com/wiki/Category:Survivors"

    k_webpage = requests.get(k_url).content
    k_soup = BeautifulSoup(k_webpage, "html.parser")

    s_webpage = requests.get(s_url).content
    s_soup = BeautifulSoup(s_webpage, "html.parser")

    k_fullFind = k_soup.find_all('a', href=re.compile('^/wiki/'))
    s_fullFind = s_soup.find_all('a', href=re.compile('^/wiki/'))

    k_eleList = []

    for element in k_fullFind:
        k_eleList.append(element['href'])

    s_eleList = []

    for element in s_fullFind:
        s_eleList.append(element['href'])

    k_eleList = k_eleList[22:-3]
    s_eleList = s_eleList[22:-3]

    eleList = k_eleList + s_eleList

    randEle = random.choice(eleList)
    randurl = 'https://deadbydaylight.fandom.com{a}'.format(a=randEle)
    webpage2 = requests.get(randurl).content
    soup2 = BeautifulSoup(webpage2, "html.parser")

    title = soup2.find('th', class_='center bold').get_text(strip=True)
    print(title)
    try:
        trivia = random.choice(soup2.find('span', id='Trivia').findNext('ul').find_all('li', recursive=False)).get_text(separator=' ', strip=True)

    except:
        trivia = "Something wrong happened, try the command again!"

    return title, trivia