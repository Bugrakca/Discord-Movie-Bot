# MovieBot

# DONE 0.1- i/o ile dosyadan okunma yapılacak.
# DONE 0.2- i/odaki veriler arraye aktarılacak
# DONE 0.3- i/odaki verilerde - olanlar izlenecek arrayine +lar izlenenler arrayine aktarılacak
# DONE 0.4- !izlenecek ve !izlenen komutları çalışır olacak
# DONE    1- birisi gelecek !add moviename yazcak
# DONE 1.1- izlenecek filmler incelenecek böyle bir film var mı? --->ya da sadece bir array olur
# DONE 1.2- izlenen filmler incelenecek böyle bir film var mı?
# DONE    2- daha önce eklenmiş böyle bir film yoksa ekleyecek NOT: eklenecek filmin başında - olacak
# DONE 2.1- önce arraye eklenecek.
# DONE 2.2- sonra kod direkt movielist.txt verisini silinip arraydekileri yazacak.
# DONE   3- !bugeceninfilmi random film çekecek.
# TODO 3.1- Timer Olsun
# DONE 3.2- Cikar goster gifini ekle
# FIXME:3.3- a harfini yazinca tum a harfini iceren filmleri listeden silinmesi.

# Import OS library
import os
# Importing random library
import random
# Importing urllib.request library
import urllib.request
# Importing re library
import re
# Importing asyncio
import asyncio
# Importing
import traceback
import sys
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


# When bot connect, open movielist.txt file. Check all the lines if has '-' (dash) or not.
@bot.event
async def on_connect():
    guncelle()


def guncelle():
    input_file = "/root/Discord-Movie-Bot/src/movielist.txt"
    with open(input_file, 'r') as filepointer:  # Su an bir problem gorunmuyor
        tire = '-'
        arti = '+'
        global izlenenler
        global izlenecek
        izlenenler = []
        izlenecek = []
        lines = filepointer.readlines()
        for line in lines:
            # If one line has '-' (dash), then add that line in to the izlenecekler(want to watch) list.
            if tire in line:
                izlenecek.append(line)
            # Else add that line in to izleneneler(watched) list.
            elif arti in line:
                izlenenler.append(line)
            else:
                print('something is wrong')


@bot.event
# Get errors by using ctx and error arguments
async def on_command_error(ctx, error):
    # Using the CommandNotFound command for the errors. If there is no match command name then give error message.
    if isinstance(error, CommandNotFound):
        # Sending an error message for that channel.
        await ctx.channel.send(":angry: Senin komutun burada geçmez aslanım :angry:")
        # Sending a gif message for that channel.
        await ctx.channel.send('https://tenor.com/view/critical-role-shoo-go-away-talks-machina-gif-11759908')
    else:
            # All other Errors not returned come here. And we can just print the default TraceBack.
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

# Creating a bot command for saying hello.


@bot.command(name='hello', help='Help melp yok lan, adam olsaydın da help istemeseydin')
async def on_message(ctx):  # Called when a message is created and sent.
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


# Edit last message.
@bot.command(name='edit', help='Son yazilan mesaji duzenler.')
async def edit(ctx):
    message_id1 = message_id  # Get message id
    channel_id1 = bot.get_channel(channel_id)  # Get channel id for object
    print(channel_id1)  # Checking the channel Id is right or wrong
    # Fetch the last message
    msg = await channel_id1.fetch_message(message_id1)
    await msg.edit(content="""```diff\n+ Hello!```""")  # Editing last message


# Create an add command
@bot.command(name='ekle', help='Listeye yeni film ekler')
async def editfile(ctx, *args):  # Define an editfile method
    guncelle()
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
        await ctx.channel.send("Eklendi. Vakti gelince izleriz." + args)
        izlenecek.append("\n-" + args)
        output_file = "/root/Discord-Movie-Bot/src/movielist.txt"
        with open(output_file, 'a') as filepointer:
            filepointer.write("\n-" + args)
    elif i == -1:
        await ctx.channel.send("Elif bir işi de başar be aslanım:" + args)


@bot.command(name='kontrolet', help = 'Listede ayni isimden film var mi kontrol edecektir, varsa birini silecek.')  # Create a checkduplicate command
async def editfile(ctx):  # Define editfile method
    input_file = "/root/Discord-Movie-Bot/src/movielist.txt"  # Defining a variable to store the file path
    with open(input_file, 'r') as filepointer:  # Open the file
        # Read lines, not just the end of the word. End of the last character
        lines = filepointer.readlines()
        # Defining a variable to store the new lines in array list.
        new_lines = []
        for line in lines:  # Get the all line in the file
            line = line.strip()  # Strip whitespaces
            if line not in new_lines:  # If new_lines and line doesn't match
                new_lines.append(line.title())  # Add to the last line
            else:  # Else print line, we don't need that but I want to see which word is duplicate
                print(line.title())
    outputfile = "/root/Discord-Movie-Bot/src/movielist.txt"  # Defining a variable to store the file path
    with open(outputfile, 'w') as filepointer:  # Open the file
        # Write into the file all the array elements.
        filepointer.write('\n'.join(new_lines))


# Creating a todaysmovie command
@bot.command(name='gününfilmi', help='Bu komut rastgele bir film sececektir.')
async def gununfilmi(ctx):  # Defining todaysmovie method
    tire = '-'  # Defining a dash variable
    input_file = "/root/Discord-Movie-Bot/src/movielist.txt"  # Defining a variable to store the file path
    with open(input_file, 'r') as filepointer:  # Open the file
        # Read lines, not just the end of the word. End of the last character
        lines = filepointer.readlines()
        for line in lines:  # Get all lines elements into the line array.
            line = line.strip()  # Strip whitespaces
            # Select a random element into the array
            choice = random.choice(lines)
            search = choice # For further usage I define another variable
            search = search.replace(" ", "+") # Replacing spaces to + (plus)
            html = urllib.request.urlopen("https://www.youtube.com/results?search_query=trailer" + search) # Using the link for search
            if tire in line:  # If elements has '-' (dash) in that line
                # Choose one and send the message
                await ctx.channel.send(choice)
                video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode()) # Read the link and decode it for uniqe regex
                await ctx.channel.send("https://www.youtube.com/watch?v=" + video_ids[0]) # Embed the first element in the link
                await ctx.channel.send('https://media.giphy.com/media/8fEaweALlO9dUmYuqv/giphy.gif') # Sending some gif
                break


@bot.command(name='liste', help='Bu komut, tum listeyi ekrana yazdirir.')
async def liste(ctx):  # Defining list method
    response = """```diff\n"""  # a This is the string value that we want to print
    i = 0  # Counter
    # Taking the lines from izlenecek(wanttowatch) array
    for line in izlenecek:
        # Fills the string value with array elements
        response = response + "{listecik}".format(listecik=line)
        i += 1
        if i % 110 == 0:
            await ctx.channel.send(response + """```""")
            response = """```diff\n"""  # ilk 110u yazdırdıktan sonra döngü dönecek ama daha veri var.
    if i % 110 != 0:
        await ctx.channel.send(response + """```""")


@bot.command(name="izlenenler", help='Izlenenler listesini ekrana yazridir.')
async def izlenenler(ctx):
    guncelle()
    await ctx.channel.send('https://cdn.discordapp.com/attachments/804499069601841173/805175464955609118/tenor.gif')
    response = """```diff\n"""
    i = 0
    for line in izlenenler:
        response = response + "{listecik}".format(listecik=line)
        i += 1
        if i % 110 == 0:
            await ctx.channel.send(response + """```""")
            response = """```diff\n"""
    if i % 110 != 0:
        await ctx.channel.send(response + """```""")

@bot.command(name ='çıkargöster', help = 'Çıkar göster gifini çıkarıp gösterir')
async def cikargoster(ctx):
    await ctx.channel.send('https://cdn.discordapp.com/attachments/804499069601841173/805175464955609118/tenor.gif')


@bot.command(name='izlendi', help='Izlenen filmleri izlenenler listesine ekleyecektir.')
async def editfile(ctx, args):
    # Gets the given value start
    response = ""
    for arg in args:
        response = response + "" + arg
    args = response.title()
    print("calışıyor " + args + " \n")
    # Gets the given value end
    input_file = "/root/Discord-Movie-Bot/src/movielist.txt"
    with open(input_file, 'r') as filepointer:
        lines = filepointer.readlines()
        new_lines = []
        for line in lines:
            line = line.strip()
            if line not in new_lines:
                if args in line:
                    line = line.replace("-", "+")
                    print("calışıyor2 " + args + " eşittir " + line)
                    new_lines.append(line)
                    await ctx.channel.send(line.replace('+', '') + " İzlenenler listesine eklendi!")
                else:
                    new_lines.append(line.title())
    outputfile = "/root/Discord-Movie-Bot/src/movielist.txt"
    with open(outputfile, 'w') as filepointer:
        filepointer.write('\n'.join(new_lines))
    filepointer.close(outputfile)

@bot.command(name='izlenmedi', help='Izlenen filmleri izlenenler listesinden çıkaracaktır.')
async def editfile(ctx, args):
    # Gets the given value start
    response = ""
    for arg in args:
        response = response + "" + arg
    args = response.title()
    # Gets the given value end
    input_file = "/root/Discord-Movie-Bot/src/movielist.txt"
    with open(input_file, 'r') as filepointer:
        lines = filepointer.readlines()
        new_lines = []
        for line in lines:
            line = line.strip()
            if line not in new_lines:
                if args in line:
                    line = line.replace("+", "-")
                    new_lines.append(line)
                    await ctx.channel.send(line.replace('-', '') + " İzlenenler listesinden çıkarıldı!")
                else:
                    new_lines.append(line.title())
    outputfile = "/root/Discord-Movie-Bot/src/movielist.txt"
    with open(outputfile, 'w') as filepointer:
        filepointer.write('\n'.join(new_lines))
    filepointer.close(outputfile)

@bot.command(name='çıkar', help='Izlenen filmleri izlenenler listesinden çıkaracaktır.')
async def editfile(ctx, args):
    # Gets the given value start
    response = ""
    for arg in args:
        response = response + "" + arg
    args = response.title()
    # Gets the given value end
    input_file = "/root/Discord-Movie-Bot/src/movielist.txt"
    with open(input_file, 'r') as filepointer:
        lines = filepointer.readlines()
        new_lines = []
        for line in lines:
            line = line.strip()
            if line not in new_lines:
                if args in line:
                    await ctx.channel.send(line.replace('-', '') + " Listeden silindi!")
                else:
                    new_lines.append(line.title())
    outputfile = "/root/Discord-Movie-Bot/src/movielist.txt"
    with open(outputfile, 'w') as filepointer:
        filepointer.write('\n'.join(new_lines))
    filepointer.close(outputfile)


@bot.command(name = "clear", help = 'Verdiginiz deger kadar mesaji, bulunan kanal icin silecektir.')
async def clear(ctx, number):
    await ctx.channel.purge(limit = int(number))

@bot.command(name='yazarlar', help='Yazarları gösterir.')
async def editfile(ctx):
    await ctx.channel.send("Bu bot;\nBuğra Akca ve Elif Nur Kemiksiz\nTarafından yazılmıştır.\n(evet tarafından)")

bot.run(TOKEN)
