from twitchio.ext import commands, routines
from config import *
from dbdFunctions import *
from zeakFunctions import *


class Bot(commands.Bot):

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(token=TWITCH_BOT_TOKEN, prefix='!', initial_channels=TWITCH_CHANNELS,
                         case_insensitive=True)

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

        await bot.wait_for_ready()
        # channel = bot.get_channel('kaikendoh')
        channel = bot.get_channel('zeakthehusky', 'kaikendoh')
        await channel.send('zeakthHype Beep Boop zeakthHype')

        # self.sending.start()

    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        if message.echo:
            return
        
        elif message.content[0] == '!':
            print(str(message.timestamp)[:19] + ' |*| ' + message.author.name + ': ' + message.content)
        
        else:
            # Print the contents of our message to console...
            print(str(message.timestamp)[:19] + ' | ' + message.author.name + ': ' + message.content)

        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        await self.handle_commands(message)

    # hello command
    @commands.cooldown(1, 10, commands.Bucket.channel)
    @commands.command()
    async def hello(self, ctx: commands.Context):
        await ctx.send(f'Hello @{ctx.author.name}!')
    
    # @commands.command()
    # async def test(self, ctx: commands.Context):
    #     toggle = next(cycle(["1","2"]))
    #     await ctx.send(toggle)

    # raid command
    @commands.command()
    async def raid(self, ctx:commands.Context, *, cmd):
        if ctx.author.is_broadcaster or ctx.author.name == 'kaikendoh':
            subMsg, freeMsg = raid_scrape(cmd)
            await ctx.send(subMsg)
            await ctx.send(freeMsg)

    # spam command
    @commands.command()
    async def spam(self, ctx:commands.Context, *, cmd):
        if ctx.author.is_broadcaster or ctx.author.name == 'kaikendoh':
            subMsg, freeMsg = raid_scrape(cmd)
            await ctx.send(4 * (subMsg + ' '))
            await ctx.send(4 * (freeMsg + ' '))

    # lurk command
    @commands.command()
    async def lurk(self, ctx: commands.Context):
        emote = heartRand()
        await ctx.send(f'@{ctx.author.name} {lurkMsg} {emote}')
    
    # discord command
    @commands.command()
    async def discord(self, ctx: commands.Context):
        mybot = self.create_user(int(ctx.author.id), ctx.author.name)
        print(ctx.author.id)
        print(ctx.author.name)
        await mybot.chat_announcement(token=TWITCH_BCSTR_TOKEN, moderator_id=self.user_id, message="testing", color="green")
    
    # commandslist command
    @commands.command()
    async def commandlist(self, ctx: commands.Context):
        await ctx.send(zeakBotMsg)

    # commandslist command
    @commands.command()
    async def zeakbot(self, ctx: commands.Context):
        await ctx.send(zeakBotMsg)

    # shrine command
    @commands.command()
    async def shrine(self, ctx: commands.Context):
        sos_list, remaining = shrine_scrape()
        await ctx.send(f"The current perks in the Shrine of Secrets are: {sos_list}. The Shrine will refresh in {remaining}.")

    # killers command
    @commands.command()
    async def killers(self, ctx: commands.Context):
        killer = killer_scrape()
        print(len(killer))
        if len(killer) < 500:
            await ctx.send(f'The current killers are: {killer}.')

        # If greater than twitch's char limit (500), split it up
        else:
            # Check how many messages will need to be sent
            sets = round(len(killer)/500 + 0.5)

            # Split up the description by the last space in each 500 characters
            for i in range(sets):
                if i == 0:
                    s_index = killer[:460].rfind(' ')
                    await ctx.send(f'The current killers are: {killer[:s_index]}.')
                    i += 1
                    killer = killer[s_index + 1:]
                elif i == sets - 1:
                    await ctx.send(killer)
                else:
                    s_index = killer[:494].rfind(' ')
                    await ctx.send(killer[:s_index])
                    i += 1
                    killer = killer[s_index + 1:]

    # survivors command
    @commands.command()
    async def survivors(self, ctx: commands.Context):
        survivor = survivor_scrape()
        print(len(survivor))
        if len(survivor) < 500:
            await ctx.send(f'The current survivors are: {survivor}.')

        # If greater than twitch's char limit (500), split it up
        else:
            # Check how many messages will need to be sent
            sets = round(len(survivor)/500 + 0.5)

            # Split up the description by the last space in each 500 characters
            for i in range(sets):
                if i == 0:
                    s_index = survivor[:460].rfind(' ')
                    await ctx.send(f'The current survivors are: {survivor[:s_index]}.')
                    i += 1
                    survivor = survivor[s_index + 1:]
                elif i == sets - 1:
                    await ctx.send(survivor)
                else:
                    s_index = survivor[:494].rfind(' ')
                    await ctx.send(survivor[:s_index])
                    i += 1
                    survivor = survivor[s_index + 1:]
    
    # perkhelp command
    @commands.command()
    async def perkhelp(self, ctx: commands.Context):
        await ctx.send(perkhelp)

    # statushelp
    @commands.command()
    async def statushelp(self, ctx: commands.Context):
        await ctx.send(statushelp)

    # statshelp command
    @commands.command()
    async def statshelp(self, ctx: commands.Context):
        await ctx.send(namehelp)

    # uniquehelp command
    @commands.command()
    async def uniquehelp(self, ctx: commands.Context):
        await ctx.send(uniquehelp)

    # perk command
    # @commands.cooldown(1, 10, commands.Bucket.channel)
    @commands.command()
    async def perk(self, ctx:commands.Context, *, perk):
        if perk.lower() == 'help':
            await ctx.send(perkhelp)
        else:
            # take perk from chat message and run through perk_scrape function
            try:
                perk_name, perk_desc = perk_scrape(perk.lower())
                perk_full = perk_name + ' - ' + perk_desc

                # if description is below twitch's character limit (500), send it to twitch chat
                if len(perk_full) <= 500:
                    await ctx.send(perk_full)

                # If greater than twitch's char limit (500), split it up
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


    # status command
    # @commands.cooldown(1, 10, commands.Bucket.channel)
    @commands.command()
    async def status(self, ctx:commands.Context, *, status):
        if status.lower() == 'help':
            await ctx.send(statushelp)
        else:
            try:
                status_name, status_desc = status_scrape(status.lower())
                status_full = status_name + ' - ' + status_desc

                # if description is below twitch's character limit (500), send it to twitch chat
                if len(status_full) <= 500:
                    await ctx.send(status_full)

                # If greater than twitch's char limit (500), split it up
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

    @commands.command()
    async def stats(self, ctx:commands.Context, *, name):
        if name.lower() == 'help':
            await ctx.send(namehelp)
        else:
            try:
                summary = stats_scrape(name.lower())
                await ctx.send(summary)

            except AttributeError:
                await ctx.send('No killer found!')

            except IndexError:
                await ctx.send('No killer found!')

            except ValueError:
                await ctx.send('No stat info on survivors!')

    @commands.command()
    async def unique(self, ctx:commands.Context, *, name):
        if name.lower() == 'help':
            await ctx.send(uniquehelp)
        else:
            try:
                perks = u_perks(name.lower())
                await ctx.send(perks)

            except AttributeError:
                await ctx.send('No survivor/killer found!')

            except IndexError:
                await ctx.send('No survivor/killer found!')

    # @routines.routine(seconds=5.0, iterations=5)
    # async def sending(self):
    #     await self.wait_for_ready() 
    #     channel = self.get_channel('kaikendoh')
    #     await channel.send('routine test')

bot = Bot()
bot.run()
# bot.run() is blocking and will stop execution of any below code here until stopped or closed.