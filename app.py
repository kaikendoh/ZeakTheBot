from twitchio.ext import commands, routines
import twitchio
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
        
        himboSet(0)
        # Starting routines that have been created
        # self.sending.start()
        self.socials.start()

        await bot.wait_for_ready()
        # channel = bot.get_channel('kaikendoh')
        channel = bot.get_channel('zeakthehusky')
        await channel.send('zeakthHype Beep Boop zeakthHype')


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

    # test command
    @commands.command()
    async def test(self, ctx: commands.Context, user: twitchio.User):
        if ctx.author.name == 'kaikendoh':
            chanInfo = await self.fetch_channel(user.name)
            authInfo = ctx.get_user(ctx.author.name)
            await ctx.send(f'Hello @{ctx.author.name}! You mentioned {user.display_name}, last seen playing {chanInfo.game_name}')
            await ctx.send(f'Sent by {authInfo}')

    # hello command
    @commands.cooldown(1, 10, commands.Bucket.channel)
    @commands.command()
    async def hello(self, ctx: commands.Context):
        await ctx.send(f'Hello @{ctx.author.name}!')
        

    # raid command
    @commands.command()
    async def raid(self, ctx:commands.Context, *, cmd):
        if ctx.author.is_broadcaster or ctx.author.name == 'kaikendoh':
            subMsg, freeMsg = raid_scrape(cmd)
            await ctx.send(subMsg)
            await ctx.send(freeMsg)

    # raid command
    @commands.command()
    async def clip(self, ctx:commands.Context, *, cmd):
        clipLink = clip_scrape(cmd)
        await ctx.send(clipLink)

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
        await ctx.send(f'@{ctx.author.display_name} {lurkMsg} {emote}')

    # shoutout command
    @commands.command()
    async def so(self, ctx: commands.Context, user: twitchio.User):
        if ctx.author.is_mod:
            chanInfo = await self.fetch_channel(user.name)
            authInfo = ctx.get_user(ctx.author.name)
            await ctx.send(f'{user.display_name} is an awesome streamer! They were last seen playing {chanInfo.game_name}. Check them out at http://twitch.tv/{user.channel.name} zeakthDance')

    # voice chat command
    @commands.command()
    async def vc(self, ctx: commands.Context):
        mybot = self.create_user(BROADCASTER_ID, BROADCASTER_NICK)
        await ctx.send(vcMsg)
        # await mybot.chat_announcement(token=TWITCH_BOT_TOKEN, moderator_id=self.user_id, message=discordMsg, color="green")

    # friend code command
    @commands.command()
    async def fc(self, ctx: commands.Context):
        await ctx.send(fcMsg1)

    # shoutout command
    @commands.command()
    async def biobreak(self, ctx: commands.Context):
        if ctx.author.is_mod:
            await ctx.send(f'Quote 31: I HAVE TO PEE')

    # ban command
    @commands.command()
    @commands.cooldown(1, 5, commands.Bucket.channel)
    async def ban(self, ctx: commands.Context, user: twitchio.User=None):
        if user == None or user.name == ctx.author.name:
            await ctx.send(f"You can't ban yourself!")
        else:
            name = user.display_name
            banCnt = usrInc(name, 'ban')
            await ctx.send(f"No! Bad {name}! You get bonked! zeakthBonk You've been banned {banCnt} times!")

    # bancount command
    @commands.command()
    async def bancount(self, ctx: commands.Context, user: twitchio.User=None):
        if user == None or user.name == ctx.author.name:
            name = ctx.author.display_name
            banCnt = usrCnt(name, 'ban')
            if banCnt == 0:
                await ctx.send(f"Such a good boy! You haven't been banned yet!")
            else:
                await ctx.send(f"You've been banned {banCnt} times!")
        else:
            name = user.display_name
            banCnt = usrCnt(name, 'ban')
            await ctx.send(f"{user.display_name} has been banned {banCnt} times!")

    # boop command
    @commands.command()
    @commands.cooldown(1, 3, commands.Bucket.channel)
    async def boop(self, ctx: commands.Context, user: twitchio.User=None):
        if user == None:    
            name = 'ZeakTheHusky'
            boopCnt = usrInc(name, 'boop')
            await ctx.send(f"{ctx.author.display_name} booped {name}'s snoot! zeakthBoop They've been booped {boopCnt} times!")

        elif user.name == ctx.author.name:
            await ctx.send(f"You can't boop yourself!")

        else:    
            name = user.display_name
            boopCnt = usrInc(name, 'boop')
            await ctx.send(f"{ctx.author.display_name} booped {name}! zeakthBoop They've been booped {boopCnt} times!")

    # boopcount command
    @commands.command()
    async def boopcount(self, ctx: commands.Context, user: twitchio.User=None):
        if user == None or user.name == ctx.author.name:
            name = ctx.author.display_name
            boopCnt = usrCnt(name, 'boop')
            if boopCnt == 0:
                await ctx.send(f"No boops yet!")
            else:
                await ctx.send(f"You've been booped {boopCnt} times!")
        else:
            name = user.display_name
            boopCnt = usrCnt(name, 'boop')
            await ctx.send(f"{user.display_name} has been booped {boopCnt} times!")

    # himbo command
    @commands.command()
    async def himbo(self, ctx: commands.Context):
        name = 'ZeakTheHusky'
        himboCnt = usrInc(name, 'himbo')
        await ctx.send(f"Zeak has had {himboCnt} himbo moment(s) this stream zeakthHuh")

    # himbo command
    @commands.command()
    async def himboset(self, ctx: commands.Context, *, cmd):
        # himboCnt = usrInc(name, 'himbo')
        setCount = int(cmd)
        himboSet(setCount)
        await ctx.send(f"Zeak has had {setCount} himbo moment(s) this stream zeakthHuh")

    # discord command
    @commands.command()
    async def discord(self, ctx: commands.Context):
        mybot = self.create_user(BROADCASTER_ID, BROADCASTER_NICK)
        await mybot.chat_announcement(token=TWITCH_BOT_TOKEN, moderator_id=self.user_id, message=discordMsg, color="primary")

    # twitter command
    @commands.command()
    async def twitter(self, ctx: commands.Context):
        mybot = self.create_user(BROADCASTER_ID, BROADCASTER_NICK)
        await mybot.chat_announcement(token=TWITCH_BOT_TOKEN, moderator_id=self.user_id, message=twitterMsg, color="primary")

    # tiktok command
    @commands.command()
    async def tiktok(self, ctx: commands.Context):
        mybot = self.create_user(BROADCASTER_ID, BROADCASTER_NICK)
        await mybot.chat_announcement(token=TWITCH_BOT_TOKEN, moderator_id=self.user_id, message=tiktokMsg, color="primary")
    
    # socials command
    @commands.command()
    async def socials(self, ctx: commands.Context):
        mybot = self.create_user(BROADCASTER_ID, BROADCASTER_NICK)
        await mybot.chat_announcement(token=TWITCH_BOT_TOKEN, moderator_id=self.user_id, message=discordMsg, color="purple")
        await mybot.chat_announcement(token=TWITCH_BOT_TOKEN, moderator_id=self.user_id, message=twitterMsg, color="blue")
        await mybot.chat_announcement(token=TWITCH_BOT_TOKEN, moderator_id=self.user_id, message=tiktokMsg, color="green")

    # misspelled socials command
    @commands.command()
    async def disocrd(self, ctx: commands.Context):
        if ctx.author.is_broadcaster or ctx.author.name == 'kaikendoh':
            name = 'ZeakTheHusky'
            himboCnt = usrInc(name, 'himbo')
            await ctx.send(f"zeakthLUL Zeak misspelled the command. Now it's {himboCnt} himbo moment(s) this stream zeakthHuh")

    # misspelled socials command
    @commands.command()
    async def tiwtter(self, ctx: commands.Context):
        if ctx.author.is_broadcaster or ctx.author.name == 'kaikendoh':
            name = 'ZeakTheHusky'
            himboCnt = usrInc(name, 'himbo')
            await ctx.send(f"zeakthLUL Zeak misspelled the command. Now it's {himboCnt} himbo moment(s) this stream zeakthHuh")

    # misspelled socials command
    @commands.command()
    async def twiter(self, ctx: commands.Context):
        if ctx.author.is_broadcaster or ctx.author.name == 'kaikendoh':
            name = 'ZeakTheHusky'
            himboCnt = usrInc(name, 'himbo')
            await ctx.send(f"zeakthLUL Zeak misspelled the command. Now it's {himboCnt} himbo moment(s) this stream zeakthHuh")

    # aster command
    @commands.command()
    async def aster(self, ctx: commands.Context):
        if ctx.author.name == 'asterthebull':
            await ctx.send("That's you!")
        else:
            msg = 'AsterBongo'
            await ctx.send(f"{msg} {msg} {msg} {msg} {msg} {msg} {msg} {msg} {msg} {msg} {msg} {msg} {msg}")

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

    # sehelp
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
                await ctx.send('No status effect found!')

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

    # @routines.routine(seconds=2.0, iterations=0)
    # async def sending(self):
    #     await self.wait_for_ready() 
    #     channel = self.get_channel('zeakthehusky')
    #     await channel.send(discordMsg)

    @routines.routine(minutes=20.0, iterations=0)
    async def socials(self):
        await self.wait_for_ready() 
        channel = self.get_channel('zeakthehusky')
        await channel.send(socialsMsg)


bot = Bot()
bot.run()
# bot.run() is blocking and will stop execution of any below code here until stopped or closed.