import winterfacev5cl
import requests
import discord
from discord.ext import commands
import gspread
from datetime import date
import time
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
    channel = message.channel 
    attach = None
    
    try:   
        attach = message.attachments[0].url
    except:
        print('no attatchment')           #gets current channel
 
    if '.png' in link or '.jpg' in link or attach:
        
        data = [link]
        
        if attach:
            print(attach,'this was found in attachments')
            data = [attach]

        for dat in data:
            try:
                get_pic(dat)
                
            except Exception as e:
                pass

            result = None

            try:
                result =  winterfacev5cl.get_data(25,200,'test.png') + ' '
                print(result)

            except :
                continue
                
            
            row = result.split(',')
            print(row,'this is row print')
            row.append(date.today().strftime('%d-%m-%Y-'))
            row.append(str(dat))
            sheet = client_.open('FLOORS').sheet1
            print('adding row to sheet')
            sheet.append_row(row,value_input_option='USER_ENTERED')
             

            await channel.send(f'```{result}```')
            continue

        

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
async def past_20(ctx,arg):
    messages = await ctx.channel.history(limit=int(arg)).flatten()

    for link in messages:
        print(link.content)

        attach = None

        try:
            attach = link.attachments[0].url
        except:
            print('no attachment, trying links')

        if '.png' in link.content or '.jpg' in link.content or attach:
            
            data = [link.content]

            if attach:
                data = [attach]
                    
            print('this is data[]: ',data)
            for dat in data:
                    
                get_pic(dat)
                result = None

                try:
                    result =  winterfacev5cl.get_data(25,200,'test.png').strip()
                    print(result)

                except :
                    print('winterfacecl failed to get any data from link')
                    pass
                        
                if result:    
                    row = result.split(',')
                    print(row,'this is row print')
                    row.append(date.today().strftime('%d-%m-%Y-'))
                    row.append(str(dat))
                    sheet = client_.open('FLOORS').sheet1
                    print('adding row to sheet')
                    sheet.append_row(row,value_input_option='USER_ENTERED')

                    await ctx.channel.send(f'```{result}```')
                
        


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
async def log(ctx,**kwargs):
    get_pic(kwargs[0])
    result =  winterfacev5cl.retrieve('test.png')
    row = result.split(',')
    sheet = client_.open('FLOORS').sheet1
    print('adding row to sheet')
    sheet.append_row(row)
    print('after adding row...')
    for ply in kwargs[1:]:
        row[0] = str(ply)
        sheet.append_row(row)
        print('added',ply)

    
    await ctx.send(result)







client.run('NzA1MDQxMTAzNTQzNDY4MDcz.Xql-4g.q4BPu5WrLsWZzWlX8pTSbbI8f98')
