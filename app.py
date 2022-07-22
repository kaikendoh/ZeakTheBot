from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

from twitchio.ext import commands
from config import TWITCH_OAUTH_TOKEN

# Import perks csv as dataframe
perks_df = pd.read_csv('perks.txt')

# Twitch channels for the bot to listen to
twitch_channels = ['kaikendoh', 'bongokaibot']

# Function to change the case of perk to capitalize the first letter
# except for certain words
def case_except(s):
    exceptions = ['a', 'an', 'of', 'the', 'is', 'for', 'de', 'from', 'with']
    word_list = re.split(' ', s)
    final = [word_list[0].capitalize()]
    for word in word_list[1:]:
        final.append(word if word in exceptions else word.capitalize())
    return " ".join(final)

# Function to scrape the perk from the dbd fandom wiki
def perk_scrape(perk):
    if perks_df['perk_name'].eq(perk).any():
        perkurl = perks_df.loc[perks_df['perk_name'] == perk, 'perk_url'].values[0]
    else:
        perkurl = case_except(perk).strip().replace(" ", "_")

    url = "https://deadbydaylight.fandom.com/wiki/{a}".format(a=perkurl)

    response = requests.get(url)
    webpage = response.content

    soup = BeautifulSoup(webpage, 'html.parser')

    perk_name = soup.find('h1').get_text(strip=True)
    perk_desc = soup.find('div', class_='formattedPerkDesc').get_text(separator=' ', strip=True).replace('\n', '')

    return perk_name, perk_desc

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


class Bot(commands.Bot):

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(token=TWITCH_OAUTH_TOKEN, prefix='?', initial_channels=twitch_channels, 
                         case_insensitive=True)

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        if message.echo:
            return

        # Print the contents of our message to console...
        print(message.content)

        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        await self.handle_commands(message)

    # hello command
    @commands.cooldown(1, 10, commands.Bucket.channel)
    @commands.command()
    async def hello(self, ctx: commands.Context):
        await ctx.send(f'Hello @{ctx.author.name}!')
        await ctx.send('2nd message')
    
    # test command
    @commands.command()
    async def test(self, ctx: commands.Context, *, message):
        if message == 'test':
            await ctx.send(f"You typed {message}!")
        else:
            await ctx.send(f"You didn't type test!")

    @commands.command()
    async def perkhelp(self, ctx: commands.Context):
        await ctx.send('Try typing ?perk <perk name> to get a description of the perk. ie "?perk spine chill"')

    # perk command
    # @commands.cooldown(1, 10, commands.Bucket.channel)
    @commands.command()
    async def perk(self, ctx:commands.Context, *, perk):
        if perk.lower() == 'help':
            await ctx.send('Try typing ?perk <perk name> to get a description of the perk. ie "?perk spine chill"')
        else:
            # take perk from chat message and run through perk_scrape function
            try:
                perk_name, perk_desc = perk_scrape(perk.lower())
                perk_full = perk_name + ' - ' + perk_desc

                # if description is below twitch's character limit, send it to twitch chat
                if len(perk_full) <= 500:
                    await ctx.send(perk_full)

                # If greater than twitch's char limit, split it up
                else:
                    # Check how many messages will need to be sent
                    sets = round(len(perk_full)/500 + 0.5)

                    # Split up the description by the last space in each 500 characters
                    for i in range(sets):
                        if i == 0:
                            s_index = perk_desc[:491 - len(perk_name)].rfind(' ')
                            await ctx.send(perk_name + ' (' + str(i + 1) + '/' + str(sets) + ') - ' + perk_desc[:s_index])
                            i += 1
                            perk_desc = perk_desc[s_index + 1:]
                        elif i == sets - 1:
                            await ctx.send('(' + str(i + 1) + '/' + str(sets) + ') - ' + perk_desc)
                        else:
                            s_index = perk_desc[:494].rfind(' ')
                            await ctx.send('(' + str(i + 1) + '/' + str(sets) + ') - ' + perk_desc[:s_index])
                            i += 1
                            perk_desc = perk_desc[s_index + 1:]
            
            except AttributeError:
                await ctx.send('No perk found!')


    # perk command
    # @commands.cooldown(1, 10, commands.Bucket.channel)
    @commands.command()
    async def status(self, ctx:commands.Context, *, status):
        if status.lower() == 'help':
            await ctx.send('Try typing ?status <status name> to get a description of the status. ie "?status exhausted"')
        else:
            try:
                status_name, status_desc = status_scrape(status.lower())
                status_full = status_name + ' - ' + status_desc

                # if description is below twitch's character limit, send it to twitch chat
                if len(status_full) <= 500:
                    await ctx.send(status_full)

                # If greater than twitch's char limit, split it up
                else:
                    # Check how many messages will need to be sent
                    sets = round(len(status_full)/500 + 0.5)

                    # Split up the description by the last space in each 500 characters
                    for i in range(sets):
                        if i == 0:
                            s_index = status_desc[:491 - len(status_name)].rfind(' ')
                            await ctx.send(status_name + ' (' + str(i + 1) + '/' + str(sets) + ') - ' + status_desc[:s_index])
                            i += 1
                            status_desc = status_desc[s_index + 1:]
                        elif i == sets - 1:
                            await ctx.send('(' + str(i + 1) + '/' + str(sets) + ') - ' + status_desc)
                        else:
                            s_index = status_desc[:494].rfind(' ')
                            await ctx.send('(' + str(i + 1) + '/' + str(sets) + ') - ' + status_desc[:s_index])
                            i += 1
                            status_desc = status_desc[s_index + 1:]
            except AttributeError:
                await ctx.send('No status found!')

bot = Bot()
bot.run()
# bot.run() is blocking and will stop execution of any below code here until stopped or closed.