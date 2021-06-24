from replit import db
from keep_alive import keep_alive
from discord.ext import commands
from time import sleep
import typing
import discord
import os
import time
import http1
import json
import asyncio

activity = discord.Activity(type=discord.ActivityType.listening, name="s!help")
PW = os.environ['PW']
TOKEN = os.environ['TOKEN']
client = commands.Bot(command_prefix = "s!", help_command=None, activity=activity, status=discord.Status.idle)
ublacklist = {409369294690975755}
wblacklist = {"@here", "@everyone","fuck","shit","damn"}
serverid = {852444192756334592}
cwhite = {854636337558192138, 852444361638805566, 854685298448138250}
swhite = {854636337558192138}

@client.event
async def on_ready():
  print('Logging in...')
  time.sleep(1)
  print('Log in done!')
  return

@client.event
async def on_message(message):
  if client.user.mentioned_in(message):
    await message.channel.send("My prefix is `s!`")

@client.command(name="help")
async def help(ctx, cmd=''):
  if not bool(cmd):
    f = open('helpcontent.txt', 'r')
    ff = f.read()
    helpE = discord.Embed(title="Commands List", description=ff)
    f.close()
    helpE.set_footer(text="Remember to add the prefix before the command!")
    helpE.set_author(name="Prefix: s!")
    await ctx.send(embed=helpE)
  else:
    cmdhelp = open('cmd.json', 'r')
    cmdhelpc = json.load(cmdhelp)
    hpEm = discord.Embed(title=cmd, description=str(cmdhelpc[cmd]))
    hpEm.set_footer(text="Tip: Type s!help to see all commands of this bot!")
    await ctx.send(embed=hpEm)
    cmdhelp.close()

@client.command()
async def invite(ctx):
  await ctx.send(embed=discord.Embed(title="Invite The Bot", description="Press [here](https://discord.com/api/oauth2/authorize?client_id=852422040878186556&permissions=2251808321&scope=bot) to invite the bot! You can also go to https://spammer.chesterwov.repl.co/invite.html to invite the bot."))

@client.command(name="ping", help="--Sends you a message. This is to make sure the bot works.")
async def ping(ctx):
    before = time.monotonic()
    message = await ctx.send("Pong!")
    ping = (time.monotonic() - before) * 1000
    await message.edit(content=f"Pong!  {int(ping)}ms!")
    print(f'Ping {int(ping)}ms')
  
@client.command(name="spam", help="--Spams the text you added after the command", category="Main Function")
async def spam(ctx, Times: typing.Optional[int]=15, *Text): 
  if ctx.author.id in ublacklist:
        await ctx.message.delete()
        await ctx.send(str(ctx.author.mention)+', you were blacklisted from this bot! DM ChesterWOV#2768 to do the ban appeal.')
        return

  for word in Text:
     if word in wblacklist:
       c = ctx.message
       await c.add_reaction('<:error:853056082066669609>')
       await ctx.send(ctx.author.mention+", "+word+' is blacklisted.')
       
       return
     
     if "@" in word:
       await ctx.message.delete()
       await ctx.send(ctx.author.mention+', `@` is blacklisted from this bot.')
       return
     
  if not ctx.channel.id == 854636337558192138:
    if ctx.guild.id == serverid:
      await ctx.message.delete()
      await ctx.send(ctx.author.mention+', `spam` is disabled in this channel.')
      return
       
  if int(Times) > 30:
    await ctx.send('Too many times! It can only be repeated under or 30 times!')
    return

  output = ''
  
  for word in Text:
    output += word
    output += ' '
  for i in range(int(Times)):
    await ctx.send(output)
    await asyncio.sleep(.7)

@client.command(name="server")
async def server(ctx):
  await ctx.send('Want to join the support server? Invite link is here: https://discord.gg/WJqJyRDntD')

@client.command(aliases=["information"])
async def info(ctx):
  await ctx.send(embed=discord.Embed(title="Information", description="Welcome to spammer! This bot is made for people to spam something :/\n\nInformation\n• Name: Spammer [s!]#6830\n• Prefix: s!\n• Developer: ChesterWOV#4052\n• Develop platforms: ⎋repl.it and ⎋uptimerobot.com\n• Code language: Python\n• Python packages used: discord.py; discord.ext commands; keep_alive.py; os; time"))
  
@client.command()
async def remember(ctx, *thing):
  thingy = ''
  for word in thing:
    thingy += word
    thingy += ' '
  db[ctx.author.id] = thingy
  msg = ''
  msg += 'I remembered \"'
  msg += thingy
  msg += '\" now! You can type `s!wihr` anytime to let me say what are the word(s) you stored in my brain.'
  await ctx.send(msg)

@client.command()
async def wihr(ctx):
  await ctx.send('<a:loading_circle:855420234098016256> Fetching data <a:loading_circle:855420234098016256>')
  dbvalue = db[ctx.author.id]
  if bool(str(dbvalue)):
    await asyncio.sleep(1)
    await ctx.send('<:check:835080284491874314> Data fetched successfully. <:check:835080284491874314>')
    await ctx.send('Your message is:')
    asyncio.sleep(.5)
    await ctx.send(str(dbvalue))
  else:
    await ctx.send('Hey '+ctx.author.mention+', seems like you still don\'t have any things stored in my brain!')
  
@client.command(name="announce", help="--This is an bot developer-only command.", category="Developer Only")
async def announce(ctx, *Announcement: str):
  if ctx.message.author.id == 788274635871092777:
    annouce = ''
    for word in Announcement:
     annouce += word
     annouce += ' '
     
    await ctx.message.delete()
    await ctx.send(annouce)
    
  else:
     await ctx.author.send("Hey, you are not the owner of this bot! Do not try to use this command! \n \nTip: Type `s!help [command]` to know more about that command.")

@client.command()
async def restart(ctx):
  if ctx.message.author.id == int(788274635871092777):
    await ctx.message.delete()
    await ctx.send('Type your password in the code to continue.')
    upw = str(input('\nType your password to continue.\n'))
    if upw == PW:
      await client.close()
      time.sleep(5)
      await login(TOKEN, bot=True)
    else:
      await ctx.send('Restart cancelled.')
      print('\nRestart cancelled.')

@client.command()
async def off(ctx):
  if ctx.message.author.id == 788274635871092777:
    await ctx.message.delete()
    await ctx.send('Type your password in the code to continue.')
    upw = str(input('\nType your password to continue.\n'))
    if upw == PW:
      await client.close()
      print('Logged out from discord.')
    else:
      await ctx.send('Restart cancelled.')
      print('\nRestart cancelled.')

@client.event
async def on_command_error(ctx, error):
  print(ctx.command.name + " was handled incorrectly.")
  time.sleep(.25)
  print(error)
  if 'Missing Permissions' in str(error):
    await ctx.send('Needed permissions are required in order to use this bot.')
    return
  else:
    if 'KeyError' in str(error):
      await ctx.send('Please insert a valid command name. Make sure to check if the capital letters are right.')
      return

  message = 'Umm... seems like an unknown error occured. Maybe you can join our support server? Here is the link: https://discord.gg/WJqJyRDntD'
  await ctx.send(message)

def deleteAllDB():
  keys = db.keys()
  for i in keys:
    del db[i]

@client.command() 
async def deleteData(ctx):
  if ctx.message.author.id == 788274635871092777:
    await ctx.send('Deleted things.')
    deleteAllDB()

async def serverCount():
  print('I am in ' + str(len(client.guilds)) + ' servers!')

keep_alive()
client.run(TOKEN)