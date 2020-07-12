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


categories = ['1s','2s','3s','4s','5s']


@client.event
async def on_ready():
    print("bot is ready")

@client.event
async def on_message(message):        #default reaction to a msg
    txt = message.content.strip().upper() 
    link = message.content.strip()       #returns the string
    channel = message.channel               #gets current channel
 
    if '.png' in link or 'imgur' in link:
        data = link.split(' ')
        get_pic(data[0])
        result = None

        print(winterfacev5cl.retrieve('test.png'))
        if winterfacev5cl.retrieve('test.png') is None:
            await channel.send("``` BAD image!, must be original sized screenshot!```")
            
        try:
            result = data[1].lower() + " " + winterfacev5cl.retrieve('test.png') + ' ' + data[2]
            print(result)
        except IndexError:
            await channel.send("``` BAD SYNTAX!, E.G : [LINK] [RSN] [CATEGORY] [1:1 (optional)]```")
        

        if data[2] in categories:
            if '1:1' in data:
                row = result.split()
                row.append('1:1')
                sheet = client_.open('FLOORS').sheet1
                print('adding row to sheet')
                sheet.append_row(row,value_input_option='USER_ENTERED')
                print('after adding row...')
                result += ' 1:1'
            else:
                row = result.split()
                row.append('5:5')
                sheet = client_.open('FLOORS').sheet1
                print('adding row to sheet')
                sheet.append_row(row,value_input_option='USER_ENTERED')
                print('after adding row...')

            
            await channel.send("``` " +result+"```")
        else :
            await channel.send('invalid input, correct format is ```[LINK] [RSN] [1S/2S/3S...]```')

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
async def link(ctx):
    """Create instant link to sheet"""
    link = 'https://docs.google.com/spreadsheets/d/1hoHTXpwujNqJskp-72_oqkQyRFkuMvOGlfqMd5VxbPo/edit#gid=367218127'
    print(link)
    msg = "Here is a link the floors sheet!: " + str(link)
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