import winterfacev5cl
import requests
import discord
from discord.ext import commands
import gspread
from oauth2client.service_account import ServiceAccountCredentials


scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('FLOORS.json', scope)
client_ = gspread.authorize(creds)

image_url = None


def get_pic(image_url):
    img_data = requests.get(image_url).content
    with open('test.png', 'wb') as handler:
        handler.write(img_data)



client = commands.Bot(command_prefix = '^')





@client.event
async def on_ready():
    print("bot is ready")

@client.event
async def on_message(message):        #default reaction to a msg
    txt = message.content.strip().upper()        #returns the string
    channel = message.channel               #gets current channel
    if 'DG HUB' in txt:
        await channel.send('never heard of it...')
    await client.process_commands(message)



@client.command()
async def ping(ctx):
    await ctx.send('PONG')

@client.command()
async def inv(ctx):
    """Create instant invite"""
    link = await ctx.channel.create_invite(max_age = 300)
    print(link)
    msg = "Here is an invite link to our server!: " + str(link)
    await ctx.send(msg)

@client.command()
async def calc(ctx):
    link = 'https://dg-service.info/calc.html'
    await ctx.send(link)

@client.command()
async def whine(ctx):
    pass

@client.command()
async def dxp(ctx):
    msg = get_relative_time(dxp_day)
    await ctx.send(msg)

@client.command()
async def website(ctx):
    await ctx.send('https://dg-service.info/')

@client.command()
async def barrikade(ctx):
    await ctx.send('barrikade sucks and whine is the superior human being')

@client.command()
async def satvik(ctx):
    await ctx.send('did nothing wrong...as far as i can tell.')

@client.command()
async def log(ctx,arg1,arg2):
    get_pic(arg1)
    result = arg2 + " " + winterfacev5cl.retrieve('test.png')
    row = result.split()
    sheet = client_.open('FLOORS').sheet1
    print('adding row to sheet')
    sheet.append_row(row)
    print('after adding row...')
    
    await ctx.send(result)







client.run('NzA1MDQxMTAzNTQzNDY4MDcz.Xql-4g.q4BPu5WrLsWZzWlX8pTSbbI8f98')