from bs4 import BeautifulSoup
import requests
import re

from twitchio.ext import commands
from config import TWITCH_OAUTH_TOKEN

twitch_channels = ['kaikendoh', 'bongokaibot']
articles = ['a', 'an', 'of', 'the', 'is']

def title_except(s, exceptions):
    word_list = re.split(' ', s)
    final = [word_list[0].capitalize()]
    for word in word_list[1:]:
        final.append(word if word in exceptions else word.capitalize())
    return " ".join(final)

def dbd_perk(perk):
    perkurl = title_except(perk, articles).replace(" ", "_")
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
        # Here we have a command hello, we can invoke our command with our prefix and command name
        # e.g ?hello
        # We can also give our commands aliases (different names) to invoke with.

        # Send a hello back!
        # Sending a reply back to the channel is easy... Below is an example.
        await ctx.send(f'Hello yeah {ctx.author.name} and {other}!')
    
    @commands.command()
    async def test(self, ctx: commands.Context, *, message):
        await ctx.send(f'Echoing {message}')

    @commands.command()
    async def dbdperk(self, ctx:commands.Context, *, perk):
        perk_desc = dbd_perk(perk)
        await ctx.send(perk_desc)

bot = Bot()
bot.run()
# bot.run() is blocking and will stop execution of any below code here until stopped or closed.