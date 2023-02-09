import os
from typing import *
from env import *

import discord
import json
from discord.ext import commands
import yaml

names: Dict[str, int]
messages: Dict[str, str] = {}
abbrevs: Dict[str, str]
travelers = {
    'bureaucrat',
    'thief',
    'gunslinger',
    'scapegoat',
    'beggar',

    'apprentice',
    'matron',
    'judge',
    'bishop',
    'voudon',

    'barista',
    'harlot',
    'butcher',
    'bonecollector',
    'deviant',

    'gangster',
}

with open('players.yaml', "w+") as f:
    names = yaml.safe_load(f)
    if names is None:
        names = {}
    print('players.yaml loaded successfully')

with open('abbrevs.yaml', "r") as f:
    abbrevs = yaml.safe_load(f)
    if abbrevs is None:
        abbrevs = {}
    print(f'Loaded {len(abbrevs)} abbreviations successfully')

for path in os.scandir('roles'):
    with open(path) as f:
        messages[path.name.removesuffix('.txt')] = f.read()

print(f'Loaded {len(messages)} role DMs successfully')

bot = commands.Bot()


@bot.slash_command(guild_ids=[GUILD])
async def addname(
        ctx: discord.ApplicationContext,
        name: discord.Option(str),
        user: discord.Option(discord.User)):
    name: str
    user: discord.User
    names[name.lower()] = user.id
    with open('players.yaml', "w") as f:
        yaml.safe_dump(names, f)
    await ctx.respond("Player added successfully")


@bot.slash_command(guild_ids=[GUILD])
async def getabbrevs(ctx: discord.ApplicationContext):
    with open('abbrevs.yaml') as f:
        await ctx.respond(f"""```yaml
{f.read()}
```""")


@bot.slash_command(guild_ids=[GUILD])
async def getnames(ctx: discord.ApplicationContext):
    await ctx.defer()
    s = []
    for name, i in names.items():
        user = await bot.get_or_fetch_user(i)
        s.append(f"{name}: {i} ({user.name}#{user.discriminator})")
    s = '\n'.join(s)
    await ctx.respond(f"""```yaml
{s}
```""")


async def send(ctx: discord.ApplicationContext, players: List[str], roles: List[str]):
    if len(players) != len(roles):
        await ctx.respond("Number of players / roles mismatch")
        return

    playerss = []
    for name in players:
        if (i := names.get(name.lower())) is not None:
            playerss.append(i)
        else:
            await ctx.respond(f'Unknown name {name}')
            return

    for i, r in enumerate(roles):
        text = messages.get(r.lower())
        if text is None:
            text = messages.get(abbrevs.get(r.lower()))
        if text is None:
            await ctx.respond(f'Unknown role name {r}')
            return
        roles[i] = text

    await ctx.defer()
    for i, text in enumerate(roles):
        user = await bot.get_or_fetch_user(playerss[i])
        dm = await user.create_dm()

        try:
            await dm.send(text)
        except discord.errors.DiscordException as ex:
            print(f"Failed to send message to {user.name}#{user.discriminator}: {ex}\n")

    await ctx.respond("Role DM's Sent.")


@bot.slash_command(guild_ids=[GUILD])
async def sendroles(ctx: discord.ApplicationContext, players: discord.Option(str), roles: discord.Option(str)):
    players: str
    roles: str

    await send(ctx, players.split(), roles.split())


@bot.slash_command(guild_ids=[GUILD])
async def sendgrim(ctx: discord.ApplicationContext, grim: discord.Option(str)):
    grim: str

    grim = grim.removeprefix('```').removeprefix('```json').removesuffix('```').strip()
    grimoire = json.loads(grim)
    players = []
    roles = []
    for p in grimoire['players']:
        if p['role'] not in travelers:
            players.append(p['name'])
            roles.append(p['role'])

    await send(ctx, players, roles)


print("Bot is running")
bot.run(TOKEN)
