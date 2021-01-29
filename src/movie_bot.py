# MovieBot
# Import OS library
import os
# Importing random library
import random
# Importing discord ext commands
from discord.ext.commands.core import Command
# Importing discord error command - CommandNotFound
from discord.ext.commands.errors import CommandNotFound

# Importing dotenv library
from dotenv import load_dotenv
# Importing discord commands
from discord.ext import commands

# Load dotenv file
load_dotenv()
# Load DISCORD TOKEN from dotenv file
TOKEN = os.getenv('DISCORD_TOKEN')

# Assign a prefix for all bot commands name
bot = commands.Bot(command_prefix='!')

# Printing to console, 'Bot is connected'
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.event # When bot connect, open movielist.txt file. Check all the lines if has '-' (dash) or not.
async def on_connect():
    input_file = "src\movielist.txt"
    with open(input_file, 'r') as filepointer:  # Su an bir problem gorunmuyor
        tire = '-'
        arti = '+'
        global izlenenler
        global izlenecek
        izlenenler = []
        izlenecek = []
        lines = filepointer.readlines()
        for line in lines:
            if tire in line: # If one line has '-' (dash), then add that line in to the izlenecekler(want to watch) list.
                izlenecek.append(line)
            else: # Else add that line in to izleneneler(watched) list.
                izlenenler.append(line)


@bot.event
async def on_command_error(ctx, error):  # Get errors by using ctx and error arguments
    if isinstance(error, CommandNotFound): # Using the CommandNotFound command for the errors. If there is no match command name then give error message.
        await ctx.channel.send(":angry: Senin komutun burada geçmez aslanım :angry:") # Sending an error message for that channel.
        await ctx.channel.send('https://tenor.com/view/critical-role-shoo-go-away-talks-machina-gif-11759908') # Sending a gif message for that channel.

# Creating a bot command for saying hello.
@bot.command(name='hello', help='Help melp yok lan, adam olsaydın da help istemeseydin')
async def on_message(ctx): # Called when a message is created and sent.
    if ctx.author == bot.user:
        return
    global channel_id
    global message_id
    global hello_there

    hello_there = [
        """```diff\n- Hello!```""",
        """```diff\n- Hi!```"""
    ]
    response = random.choice(hello_there)
    msg = await ctx.channel.send(response)
    channel_id = msg.channel.id
    message_id = msg.id
    print(message_id)


@bot.command(name='edit')
async def edit(ctx):
    message_id1 = message_id
    channel_id1 = bot.get_channel(channel_id)
    print(channel_id1)
    msg = await channel_id1.fetch_message(message_id1)
    await msg.edit(content="""```diff\n+ Hello!```""")


@bot.command(name='ekle')
async def editfile(ctx, *args):
    i = -1
    response = ""
    for arg in args:
        response = response + " " + arg
    args = response.title()
    for line in izlenecek:
        if args in line:
            i = 0
            break
    if(i != 0):
        for line in izlenenler:
            if args in line:
                i = 1
                break
            else:
                i = 2
    if i == 0:
        await ctx.channel.send("Bu zaten eklenmiş aslan parçası sakin ol. Vakti gelince izlenir." + args)
    elif i == 1:
        await ctx.channel.send("E bu zaten izlenmiiiş. Sen yok muydun? :cry: " + args)
    elif i == 2:
        await ctx.channel.send("Eklendi vakti gelince izleriz." + args)
        izlenecek.append("\n-" + args)
        output_file = 'src\movielist.txt'
        with open(output_file, 'a') as filepointer:
            filepointer.write("\n-" + args)
    elif i == -1:
        await ctx.channel.send("Elif bir işi de başar be aslanım:" + args)

@bot.command(name='kontrolet')
async def editfile(ctx):
    input_file = "src\movielist.txt"
    with open(input_file, 'r') as filepointer:
        lines = filepointer.readlines()
        new_lines = []
        for line in lines:
            # Strip whitespaces
            line = line.strip()
            if line not in new_lines:
                new_lines.append(line)
            else:
                print(line)
    outputfile = "src\movielist.txt"
    with open(outputfile, 'w') as filepointer:
        filepointer.write('\n'.join(new_lines))


@bot.command(name='gününfilmi', help='Bu komut rastgele bir film sececektir.')
async def gununfilmi(ctx):
    tire = '-'
    input_file = "src\movielist.txt"
    with open(input_file, 'r') as filepointer:
        lines = filepointer.readlines()
        for line in lines:
            line = line.strip()
            choice = random.choice(lines)
            if tire in line:
                await ctx.channel.send(choice)
                await ctx.channel.send('https://media.giphy.com/media/8fEaweALlO9dUmYuqv/giphy.gif')
                break

bot.run(TOKEN)
