import os
import discord
from discord.ext import tasks, commands
import asyncio
# Intents settings
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# List of keywords
banned_words = ["words"]

everyone_everword = ["@everyone"]

# Regular expression for detecting Discord invite links
invite_links = ["discord.gg/", "discord.com/invite/"]

# Names of roles to be ignored
ignored_roles = ["ROLES"]

# Channels that are to be unmoderated (ID only)
exempted_channel_ids = [channel id]  # Here, enter the IDs of the channels that are to be excluded from moderation.

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return  # Ignoring errors "Command not found"
    print(f'Error: {error}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Check whether the message is sent in channels that are to be moderated
    if message.channel.id not in exempted_channel_ids:
    # Check if the author of the message has any of the ignored roles
        if any(role.name in ignored_roles for role in message.author.roles):
            await bot.process_commands(message)
            return

        # Checking whether a message contains prohibited words
        if any(word in message.content.lower() for word in banned_words):
            await message.delete()
            await message.author.ban(reason="MESSAGE")  # Enter the reason for the block here.
            await message.channel.send(f'{message.author.mention} REASON') # Enter the cause of the player being banned.

    # Check if the message contains a link to a Discord server invitation
        if any(link in message.content.lower() for link in invite_links):
            await message.delete()
            await message.author.ban(reason="Advertising other servers")
            await message.channel.send(f'{message.author.mention} was banned for sending links to other servers.')

        if any(everyone in message.content.lower() for everyone in everyone_everword):
            await message.delete()
            await message.author.ban(reason="Sending messages 'everyone'")
            await message.channel.send(f'{message.author.mention} was banned for sending messages using everyone function.')

        await bot.process_commands(message)

@bot.command()
async def reload_extension(ctx, extension):
    try:
        bot.reload_extension(extension)
        await ctx.send(f'Reloaded extension: {extension}')
    except commands.ExtensionError as e:
        await ctx.send(f'Error reloading extension {extension}: {str(e)}')

@bot.command()
@commands.has_permissions(administrator=True)
async def restart(ctx):
    await ctx.send("Restarting bot...")
    await bot.close()
    os.system("python bot.py")

# List of extensions to reload
extensions_to_reload = ['cogs.admin', 'cogs.fun']

# Reload all extensions from the list
async def reload_all_extensions():
    for extension in extensions_to_reload:
        try:
            bot.reload_extension(extension)
            print(f'Reloaded extension: {extension}')
        except commands.ExtensionError as e:
            print(f'Error reloading extension {extension}: {str(e)}')

# Load all extensions at startup
@bot.event
async def on_ready():
    for extension in extensions_to_reload:
        try:
            bot.load_extension(extension)
            print(f'Loaded extension: {extension}')
        except commands.ExtensionError as e:
            print(f'Error loading extension {extension}: {str(e)}')
            

bot.run('TOKEN') #Enter your Discord bot token here (DO NOT PUBLISH THIS TOKEN)