from bs4 import BeautifulSoup
import requests
import re

from twitchio.ext import commands
from config import TWITCH_OAUTH_TOKEN

# Twitch channels for the bot to listen to
twitch_channels = ['kaikendoh', 'bongokaibot']

# Function to change the case of perk to capitalize the first letter
# except for certain words
def case_except(s):
    exceptions = ['a', 'an', 'of', 'the', 'is', 'for', 'de', 'from']
    word_list = re.split(' ', s)
    final = [word_list[0].capitalize()]
    for word in word_list[1:]:
        final.append(word if word in exceptions else word.capitalize())
    return " ".join(final)

def perk_scrape(perk):
    perkurl = case_except(perk).replace(" ", "_")
    url = "https://deadbydaylight.fandom.com/wiki/{a}".format(a=perkurl)

    response = requests.get(url)
    webpage = response.content

    soup = BeautifulSoup(webpage, 'html.parser')

    fullperk = soup.find('div', class_='formattedPerkDesc').get_text(separator=' ', strip=True).replace('\n', '')

    return fullperk


class Bot(commands.Bot):

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(token=TWITCH_OAUTH_TOKEN, prefix='?', initial_channels=twitch_channels)

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

    @commands.command()
    async def hello(self, ctx: commands.Context):
        await ctx.send(f'Hello {ctx.author.name}!')
        await ctx.send('2nd message')
    
    @commands.command()
    async def test(self, ctx: commands.Context, *, message):
        if message == 'test':
            await ctx.send(f'Nice! You typed test!')
        else:
            await ctx.send(f"You didn't type test! You typed {message}")

    @commands.command()
    async def perk(self, ctx:commands.Context, *, perk):
        perk_desc = perk_scrape(perk)
        if len(perk_desc) <= 500:
            await ctx.send(perk_desc)
        else:
            sets = round(len(perk_desc)/500 + 0.5)

            for i in range(sets):
                if i == 0:
                    s_index = perk_desc[:494].rfind(' ')
                    await ctx.send('(' + str(i + 1) + '/' + str(sets) + ') ' + perk_desc[:s_index])
                    i += 1
                    perk_desc = perk_desc[s_index + 1:]
                elif i == sets - 1:
                    await ctx.send('(' + str(i + 1) + '/' + str(sets) + ') ' + perk_desc)
                else:
                    s_index = perk_desc[:494].rfind(' ')
                    await ctx.send('(' + str(i + 1) + '/' + str(sets) + ') ' + perk_desc[:s_index])
                    i += 1
                    perk_desc = perk_desc[s_index + 1:]

bot = Bot()
bot.run()
# bot.run() is blocking and will stop execution of any below code here until stopped or closed.