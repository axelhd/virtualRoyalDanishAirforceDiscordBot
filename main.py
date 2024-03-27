import os
import configparser
import sys
import discord
from discord.ext import commands
import wakeonlan
import requests
import socket

config = configparser.ConfigParser()

intents = discord.Intents.default()
intents.reactions = True  # Enable reaction events
intents.message_content = True
intents.members = True

# Create a bot instance
bot = commands.Bot(command_prefix="$", intents=intents)

config.read('config.ini')

if config.sections() == "[]":
    print(config.sections())
    print("Config file empty, quitting")
    sys.exit()

for key in config['DEFAULT']:
    print(f"{key}: {config['DEFAULT'][key]}")

ip = config['DEFAULT']['ip']
TOKEN = config['DEFAULT']['token']
message_id1 = config['DEFAULT']['message_id1']
message_id2 = config['DEFAULT']['message_id2']
authorization = config['DEFAULT']['authorization']
authorization_mode = config['DEFAULT']['authorization_mode']
authorization_mode = int(authorization_mode)


def update_config(updated_config):
    with open('config.ini', 'w') as configfile:
        updated_config.write(configfile)
        config.read('config.ini')


def authorize(user):
    if authorization_mode == 0:
        if str(user) != authorization:
            return True
    if authorization_mode == 1:
        if str(user) == authorization:
            return True

    return False


def reaction_message(message):
    config.read('config.ini')
    message_id1 = config['DEFAULT']['message_id1']
    message_id2 = config['DEFAULT']['message_id2']
    print(message)
    message = str(message)
    if message == message_id1 or message == message_id2:
        return True
    return False


# Emoji Variables

a = "🇦"
b = "🇦"
c = "🇨"
d = "🇩"
e = "🇪"
f = "🇫"
g = "🇬"
h = "🇭"
i = "🇮"
j = "🇯"
k = "🇰"
l = "🇱"
m = "🇲"
n = "🇳"
o = "🇴"
p = "🇵"
q = "🇶"
r = "🇷"
s = "🇸"
t = "🇹"
u = "🇺"
v = "🇻"
w = "🇼"
x = "🇽"
y = "🇾"
z = "🇿"

emoji_to_letter = {
    "🇦": "A",
    "🇧": "B",
    "🇨": "C",
    "🇩": "D",
    "🇪": "E",
    "🇫": "F",
    "🇬": "G",
    "🇭": "H",
    "🇮": "I",
    "🇯": "J",
    "🇰": "K",
    "🇱": "L",
    "🇲": "M",
    "🇳": "N",
    "🇴": "O",
    "🇵": "P",
    "🇶": "Q",
    "🇷": "R",
    "🇸": "S",
    "🇹": "T",
    "🇺": "U",
    "🇻": "V",
    "🇼": "W",
    "🇽": "X",
    "🇾": "Y",
    "🇿": "Z"
}

alphabet_emoji = [
    "🇦", "🇧", "🇨", "🇩", "🇪", "🇫", "🇬", "🇭", "🇮", "🇯", "🇰", "🇱", "🇲",
    "🇳", "🇴", "🇵", "🇶", "🇷", "🇸", "🇹", "🇺", "🇻", "🇼", "🇽", "🇾", "🇿"
]

RolesV2 = [
    "A-10A Warthog",
    "A-10C Tank Killer",
    "AH-64D Apache",
    "AV-8B Harrier",
    'Bf 109 K-4',
    "C-101 Aviojet",
    "CVN-72 Aircraft Carrier",
    "F-14D Tomcat",
    "F-15C Eagle",
    "F-15E Eagle",
    "F-16C Viper",
    "F-5 Tiger II",
    "F-86 Sabre",
    "FA-18C Hornet",
    "Fw 190 D-9",
    "SA342 Gazelle",
    "I-16",
    "JF-17 Thunder",
    "Ka-50 Black Shark 3",
    "L-39 Albatros",
    "Combined Arms",
    "MB-339 Macchi",
    "Mi-8P Hip",
    "MiG-15 Fagot",
    "MiG-19 Farmer",
    "MiG-21 Fishbed",
    "MiG-29 Fulcrum",
    "Mi-24P Hind",
    "Mirage 2000C",
    "Mirage F1",
    "Mosquito FB VI",
    "P-47 Thunderbolt",
    "P-51D Mustang",
    "Spitfire LF Mk. IX",
    "Su-25 Frogfoot",
    "Su-27 Flanker",
    "Su-33 Flanker-D",
    "UH-1 Huey",
    "AJS-37 Viggen",
    "Yak-52"
]

custom_emoji = [":A10v2:",
                ":A10:",
                ":AH64D:",
                ":AV8B:",
                ":BF109:",
                ":C101:",
                ":CVN72:",
                ":F14D:",
                ":F15C:",
                ":F15E:",
                ":F16:",
                ":F5:",
                ":F86:",
                ":FA18C:",
                ":Fw_190:",
                ":Gazelle:",
                ":I16:",
                ":JF17:",
                ":Ka50:",
                ":L39ZA:",
                ":Leopard_2_A7:",
                ":MB339:",
                ":Mi8P:",
                ":MiG15:",
                ":MiG19:",
                ":MiG21:",
                ":MiG29:",
                ":Mi24P:",
                ":Mirage_2000C:",
                ":Mirage_F1:",
                ":Mosquito:",
                ":P47:",
                ":P51D:",
                ":Spitfire:",
                ":Su25:",
                ":Su27:",
                ":Su33:",
                ":UH1:",
                ":Viggen:",
                ":Yak52:"
                ]

custom_emoji_id = [
    "<:A10:1168464122531295242>",
    "<:A10v2:1168464272909676647>",
    "<:AH64D:1168464275036184676>",
    "<:AV8B:1168464278039314472>",
    "<:BF109:1168464221340696606>",
    "<:C101:1168464287140937808>",
    "<:CVN72:1168464290580287568>",
    "<:F14D:1168464300428497016>",
    "<:F15C:1168464186028863488>",
    "<:F15E:1168464189216534578>",
    "<:F16:1168464191447891979>",
    "<:F5:1168464295890268260>",
    "<:F86:1168464194648162364>",
    "<:FA18C:1168464198423031848>",
    "<:Fw_190:1168464200570523648>",
    "<:Gazelle:1168464204089544714>",
    "<:I16:1168464206845190174>",
    "<:JF17:1168463734893719682>",
    "<:Ka50:1168464208732626954>",
    "<:L39ZA:1168464211609919579>",
    "<:Leopard_2_A7:1168464215196061716>",
    "<:MB339:1168464217733599264>",
    "<:Mi8P:1168464223383339018>",
    "<:MiG15:1168464225455308802>",
    "<:MiG19:1168464228592648202>",
    "<:MiG21:1168464231029542922>",
    "<:MiG29:1168464233604857916>",
    "<:Mi24P:1168464235844608040>",
    "<:Mirage_2000C:1168464237904023623>",
    "<:Mirage_F1:1168464241397862430>",
    "<:Mosquito:1168464292971024394>",
    "<:P47:1168464245835448330>",
    "<:P51D:1168464247706107937>",
    "<:Spitfire:1168464251845873684>",
    "<:Su25:1168464255188733953>",
    "<:Su27:1168464258368020490>",
    "<:Su33:1168464261094330409>",
    "<:UH1:1168464264336519188>",
    "<:Viggen:1168464391939829770>",
    "<:Yak52:1168464269734584380>"
]

emoji_to_role_dict = {}

for i in range(len(RolesV2)):
    emoji_to_role_dict[RolesV2[i]] = custom_emoji_id[i]  # .replace("<", "").replace(">", "")

print(emoji_to_role_dict)
emoji_to_role_dict = {v: k for k, v in emoji_to_role_dict.items()}
print(emoji_to_role_dict)


# End Emoji Variables

@bot.command()
async def reset_config(ctx):
    config['DEFAULT'] = {'ip': '<IP>',
                         'message_id1': '',
                         'message_id2': '',
                         'token': '',
                         'authorization': '',
                         'authorization_mode': 0}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)


@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)


@bot.command()
async def cleanup(ctx):
    print("Cleaning up")
    # Get the server (guild) from the context
    server = ctx.guild

    # Get all roles in the server
    roles = server.roles

    # Loop through the roles and delete those with no members
    for role in roles:
        if len(role.members) == 0:
            await role.delete()
            print(f'Deleted role: {role.name}')


@bot.command()
async def start(ctx):
    if authorize(ctx.message.author):
        server_online = os.system(f"ping  -c 1 {ip}")
        print(server_online)

        if server_online == 0:
            await ctx.reply("Server already online")

        else:
            await ctx.reply("Starting server")
            wakeonlan.send_magic_packet("D4:81:D7:B5:E7:13")
    else:
        await ctx.reply('NUH UH')


@bot.command()
async def stop(ctx):
    if authorize(ctx.message.author):
        server_online = os.system(f"ping  -c 1 {ip}")
        if server_online == 0:
            await ctx.reply("Stopping server")
            requests.get(f"{ip}:5000/poweroff")

        else:
            await ctx.reply("Server not online")
    else:
        await ctx.reply('NUH UH')


@bot.command()
async def status(ctx):
    server_online = False
    shutdown_available = False
    dcs_server_online = False

    if authorize(ctx.message.author):
        server_online = os.system(f"ping  -c 1 {ip}")
        if server_online == 0:
            server_online = True

        else:
            await ctx.reply(f"Server Online: {server_online}\n Shutdown Available: {shutdown_available}\n DCS Running: {dcs_server_online}")
            return

        if str(requests.get(f"{ip}:5000/test")).strip() == "test":
            shutdown_available = True

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex((ip, 10308)) == 0:
                dcs_server_online = True

        await ctx.reply(f"Server Online: {server_online}\n Shutdown Available: {shutdown_available}\n DCS Running: {dcs_server_online}")
    else:
        await ctx.reply('NUH UH')


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content == '!start reaktioner':
        await message.channel.send("Reager for at få roller")
        roles_react1 = await message.channel.send("Vælg roller (1/2)")
        config['DEFAULT']['message_id1'] = str(roles_react1.id)
        update_config(config)
        for i in range(0, len(custom_emoji_id)):
            if i == 20:
                break

            await roles_react1.add_reaction(custom_emoji_id[i])

        roles_react2 = await message.channel.send("Vælg roller (2/2)")
        config['DEFAULT']['message_id2'] = str(roles_react2.id)
        update_config(config)
        for i in range(20, len(custom_emoji_id)):
            if i == 40:
                break

            await roles_react2.add_reaction(custom_emoji_id[i])

        # roles_react3 = await message.channel.send("Vælg roller (3/3)")
        # for i in range(40, len(custom_emoji_id)):
        #     await roles_react3.add_reaction(custom_emoji_id[i])

    if message.content == '!Initialiser':
        for aircraft in RolesV2:
            await message.guild.create_role(name=aircraft)
            print(f"Creating role: {aircraft}")

    if message.content.startswith('!Ryd op'):
        print("Cleaning up")

        # Get the server (guild) from the message
        server = message.guild

        # Get all roles in the server
        roles = server.roles

        # Loop through the roles and delete those with no members
        for role in roles:
            if len(role.members) == 0:
                await role.delete()
                print(f'Deleted role: {role.name}')
    if message.content == "emoji":
        for ce in custom_emoji_id:
            await message.channel.send(ce)

    await bot.process_commands(message)


@bot.event
async def on_reaction_add(reaction, user):
    if user == bot.user:
        return

    if reaction_message(reaction.message.id):
        if str(reaction.emoji) in custom_emoji_id:
            await reaction.message.channel.send(f"{user.mention}, Reacted with {reaction.emoji}!")
            role = emoji_to_role_dict.get(str(reaction.emoji))
            print(role)
            dRole = discord.utils.get(user.guild.roles, name=role)
            await user.add_roles(dRole)


@bot.event
async def on_reaction_remove(reaction, user):
    if user == bot.user:
        return
    if reaction_message(reaction.message.id):
        if str(reaction.emoji) in custom_emoji_id:
            await reaction.message.channel.send(f"{user.mention}, Removed reaction {reaction.emoji}!")
            role = emoji_to_role_dict.get(str(reaction.emoji))
            print(role)
            dRole = discord.utils.get(user.guild.roles, name=role)
            await user.remove_roles(dRole)


bot.run(TOKEN)
