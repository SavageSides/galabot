import discord
import json
import datetime
import asyncio
from discord.ext import commands

TOKEN = "NDk0Njc0ODM0MjI4NTEwNzIw.Do29kQ.IsaaxeeZs8R8DdCJiErgJjctVbU"

client = commands.Bot(command_prefix="g?")
client.remove_command('help')

@client.event
async def on_ready():
    print("Ready")

@client.command(pass_context=True)
async def warn(ctx, member: discord.Member):
    with open("warnings.json", "r") as f:
        warnings = json.load(f)
    author = ctx.message.author
    if author == member:
        await client.say("You can't warn your self!")
        return
    if not ctx.message.server.id in warnings:
        warnings[ctx.message.server.id] = {}
    if not member.id in warnings[ctx.message.server.id]:
        warnings[ctx.message.server.id][member.id] = 0
    warnings[ctx.message.server.id][member.id] += 1
    embed = discord.Embed(color=0xf00000, timestamp=datetime.datetime.utcnow())
    embed.add_field(name="***__Warned:__***", value=f"I have warned {member.mention}.", inline=True)
    embed.set_footer(icon_url=member.avatar_url, text="Removed Warnings.")
    await client.say(embed=embed)
    if warnings[ctx.message.server.id][member.id] == 3:
        MutedRole = discord.utils.get(ctx.message.server.roles, name="Muted")
        await client.add_roles(member, MutedRole)
        await client.say(f"{member.mention} has been muted because of the following: ``3 Warnings``")
        await asyncio.sleep(1880)
        await client.remove_roles(member, MutedRole)
        await client.say(f"{member.mention} has been unmuted.")
        return
    with open("warnings.json", "w") as f:
        json.dump(warnings, f, indent=4)

@client.command(pass_context=True)
async def rwarns(ctx, member: discord.Member):
    with open("warnings.json", "r") as f:
        warnings = json.load(f)
    author = ctx.message.author
    warns = warnings[ctx.message.server.id][member.id]
    if warnings[ctx.message.server.id][member.id] == 0:
        await client.say(f"{member.mention}'s warns can't be removed. Because, he has none! :joy:")
        return
    if not ctx.message.server.id in warnings:
        warnings[ctx.message.server.id] = {}
    if not member.id in warnings[ctx.message.server.id]:
        warnings[ctx.message.server.id][member.id] = 0
    warnings[ctx.message.server.id][member.id] -= warns
    embed = discord.Embed(color=0xf00000, timestamp=datetime.datetime.utcnow())
    embed.add_field(name="***__Removed:__***", value=f"{member.mention}'s warns have been removed.", inline=False)
    embed.set_footer(icon_url=member.avatar_url, text="Removed Warnings.")
    await client.say(embed=embed)
    with open("warnings.json", "w") as f:
        json.dump(warnings, f, indent=4)

@client.command(pass_context=True)
async def warnings(ctx, member: discord.Member):
    with open("warnings.json", "r") as f:
        warnings = json.load(f)
    if not member.id in warnings[ctx.message.server.id]:
        warnings[ctx.message.server.id][member.id] = 0
    warns = warnings[ctx.message.server.id][member.id]
    embed = discord.Embed(color=0xf00000, timestamp=datetime.datetime.utcnow())
    embed.add_field(name="***__Warnings:__***", value=f"{member.mention} Has {warns} At the moment!", inline=False)
    embed.set_footer(icon_url=member.avatar_url, text="Warnings.")
    await client.say(embed=embed)
    with open("warnings.json", "w") as f:
        json.dump(warnings, f, indent=4)

@client.command(pass_context=True)
async def kick(ctx, member: discord.Member = None):
    author = ctx.message.author
    channels = ctx.message.channel
    if ctx.message.author.server_permissions.kick_members:
        if member is None:
            await client.say(f"{author.mention} I can't preform this action without a user.")
        else:
            await client.kick(member)
            embed = discord.Embed(color=0xf00000, timestamp=datetime.datetime.utcnow())
            embed.add_field(name="***__Kicked:__***", value=f"I have kicked {member.mention}.", inline=True)
            await client.say(embed=embed)
            channel = discord.utils.get(ctx.message.server.channels, name="mod-log")
            embed = discord.Embed(color=0xf00000, timestamp=datetime.datetime.utcnow())
            embed.add_field(name="***__Kicked:__***", value=f"I have kicked {member.mention}.", inline=True)
            embed.add_field(name="***__Author:__***", value=f"{author.mention}", inline=False)
            embed.add_field(name="***__Location:__***", value=f"{channels.mention}", inline=True)
            await client.send_message(channel, embed=embed)
    else:
        await client.say(f"{author.mention} You can't use this commands! Permissions: ``Kick_Members``")

@client.command(pass_context=True)
async def ban(ctx, member: discord.Member = None):
    author = ctx.message.author
    channels = ctx.message.channel
    if ctx.message.author.server_permissions.ban_members:
        if member is None:
            await client.say(f"{author.mention} I can't preform this action without a user.")
        else:
            await client.ban(member)
            embed = discord.Embed(color=0xf00000, timestamp=datetime.datetime.utcnow())
            embed.add_field(name="***__Banned:__***", value=f"I have Banned {member.mention}.", inline=True)
            await client.say(embed=embed)
            channel = discord.utils.get(ctx.message.server.channels, name="mod-log")
            embed = discord.Embed(color=0xf00000, timestamp=datetime.datetime.utcnow())
            embed.add_field(name="***__Banned:__***", value=f"I have Banned {member.mention}.", inline=True)
            embed.add_field(name="***__Author:__***", value=f"{author.mention}", inline=False)
            embed.add_field(name="***__Location:__***", value=f"{channels.mention}", inline=True)
            await client.send_message(channel, embed=embed)
    else:
        await client.say(f"{author.mention} You can't use this commands! Permissions: ``Ban_Members``")

@client.command(pass_context=True)
async def mute(ctx, user: discord.Member = None):
    author = ctx.message.author
    channels = ctx.message.channel
    if ctx.message.author.server_permissions.mute_members:
        MutedRole = discord.utils.get(ctx.message.server.roles, name='Muted')
        if user is None:
             await client.say(f"{author.mention} Please specify a mentioned user for me to mute.")
             return
        embed = discord.Embed(color=0xf00000, timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Muted", value=f"{user.mention}", inline=True)
        await client.say(embed=embed)
        channel = discord.utils.get(ctx.message.server.channels, name="mod-log")
        embed = discord.Embed(color=0xf00000, timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Muted", value=f"{user.mention}", inline=True)
        embed.add_field(name="***__Author:__***", value=f"{author.mention}", inline=False)
        embed.add_field(name="***__Location:__***", value=f"{channels.mention}", inline=True)
        await client.send_message(channel, embed=embed)
        await client.add_roles(user, MutedRole)
    else:
        await client.say(f"{author.mention} You can't use this commands! Permissions: ``Mute_Members``")

@client.command(pass_context=True)
async def unmute(ctx, user: discord.Member = None):
    author = ctx.message.author
    channels = ctx.message.channel
    if ctx.message.author.server_permissions.mute_members:
        MutedRole = discord.utils.get(ctx.message.server.roles, name='Muted')
        if user is None:
             await client.say(f"{author.mention} Please specify a mentioned user for me to unmute.")
             return
        embed = discord.Embed(color=0xf00000, timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Unmuted", value=f"{user.mention}", inline=True)
        await client.say(embed=embed)
        channel = discord.utils.get(ctx.message.server.channels, name="mod-log")
        embed = discord.Embed(color=0xf00000, timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Unmuted", value=f"{user.mention}", inline=True)
        embed.add_field(name="***__Author:__***", value=f"{author.mention}", inline=False)
        embed.add_field(name="***__Location:__***", value=f"{channels.mention}", inline=True)
        await client.send_message(channel, embed=embed)
        await client.remove_roles(user, MutedRole)
    else:
        await client.say(f"{author.mention} You can't use this commands! Permissions: ``Mute_Members``")

@client.command(pass_context=True)
async def clear(ctx, amount=0):
    author = ctx.message.author
    if ctx.message.author.server_permissions.manage_messages:
        channel = ctx.message.channel
        messages = []
        async for message in client.logs_from(channel, limit=int(amount)):
            messages.append(message)
        await client.delete_messages(messages)
        channels = discord.utils.get(ctx.message.server.channels, name="mod-log")
        embed = discord.Embed(color=0xf00000, timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Cleared the chat", value=f"{author.mention}", inline=True)
        await client.say(embed=embed)
        embed = discord.Embed(color=0xf00000, timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Cleared the chat", value=f"{author.mention}", inline=True)
        await client.send_message(channels, embed=embed)
    else:
        await client.say(f"{author.mention} You can't use this commands! Permissions: ``Mute_Members``")

@client.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author
    embed = discord.Embed(color=0xf00000, timestamp=datetime.datetime.utcnow())
    embed.add_field(name="***__Moderation:__***", value="**g?kick @user** Will kick the user \n **g?ban @User** Will ban the user \n **g?warn @user** Will warn the user \n **g?rwarn @user** Will remove the users warns \n **g?warnings @user** Will show you the warnings the user has \n **g?mute @User** Will give the muted role \n **g?unmute @user** Will remove the Muted Role \n **g?clear <amount>** Will clear that amount", inline=False)
    embed.add_field(name="***_Fun:__***", value="**g?milk @user** This will just make a meme command xD \n **g?avatar** Will show the users/your avatar \n **g?serverinfo** Will show the servers info \n **g?userinfo @User** Shows the users information \n ***g?dm @User <message>** Will send this user a DM on my part", inline=True)
    embed.add_field(name="***__Verifacation:__***", value="**g?apply** Will send you a PM that contains the questions \n **g?confirm <Ansewers>** Will send your answers to the staff members \n **g?verify @User** Will verify the user", inline=False)
    await client.send_message(author, embed=embed)
    await client.say(f"{author.mention} sent you the help message!")

@client.event
async def on_member_join(member):
    with open('level.json', 'r') as f:
        users = json.load(f)

    await update_data(users, member)
    

    with open('level.json', 'w') as f:
        json.dump(users, f)
    server = member.server
    channel = discord.utils.get(server.channels, name="welcome-and-goodbye")
    NewRole = discord.utils.get(server.roles, name="verification")
    await client.send_message(channel, f"Welcome {member.mention} to **{server.name}**! I hope you enjoy your stay!")
    await client.add_roles(member, NewRole)
    await client.send_message(member, f"Welcome to **{server.name}**! To be verified, Say g?apply in response to this message and the **{server.name}** application will begin, then the leader or admins will read your application then decide if you are to be verified or not. Thank you for your time!")

@client.event
async def on_member_remove(member):
    server = member.server
    channel = discord.utils.get(server.channels, name='welcome-and-goodbye')
    await client.send_message(channel, f"Bye Bye {member.mention}! You was pretty gay anyways :smiley:")

    
@client.event
async def on_message(message):
    await client.process_commands(message)
    if message.author.bot:
        return
    with open('level.json', 'r') as f:
        users = json.load(f)

    await update_data(users, message.author)
    await add_experience(users, message.author, 5)
    await level_up(users, message.author, message.channel)

    with open('level.json', 'w') as f:
        json.dump(users, f)

async def update_data(users, user):
    if not user.id in users:
        users[user.id] = {}
        users[user.id]['experience'] = 0
        users[user.id]['level'] = 1

async def add_experience(users, user, exp):
    users[user.id]['experience'] += exp

async def level_up(users, user, channel):
    experience = users[user.id]['experience']
    lvl_start = users[user.id]['level']
    lvl_end = int(experience ** (1/4))

    if lvl_start < lvl_end:
        await client.send_message(channel, f"{user.mention} You leveled up to {lvl_end}!")
        users[user.id]['level'] = lvl_end

@client.command(pass_context=True)
async def event(ctx, *, remind):
    author = ctx.message.author
    channel = discord.utils.get(ctx.message.server.channels, name="events")
    embed = discord.Embed(color=0xf00000, timestamp=datetime.datetime.utcnow())
    embed.add_field(name="***__Event!__***", value=f"{remind}", inline=False)
    embed.add_field(name="***__Created By:__***", value=f"{author.mention}", inline=True)
    await client.send_message(channel, embed=embed)

@client.command(pass_context=True)
async def milk(ctx, user: discord.Member):
    embed = discord.Embed(color=0xf00000, timestamp=datetime.datetime.utcnow())
    embed.add_field(name="You need some milk!", value=f"{user.mention} You needz some milk boi!", inline=False)
    embed.set_image(url="https://cdn.discordapp.com/attachments/491062701213220884/494996214027255828/th.jpg")
    await client.say(embed=embed)

@client.command(pass_context=True)
async def dm(ctx, user: discord.Member, *, text):
    author = ctx.message.author
    embed = discord.Embed(color=0xf00000, timestamp=datetime.datetime.utcnow())
    embed.add_field(name="Message:", value=f"{text}", inline=False)
    embed.add_field(name="Sent By:", value=f"{author.mention}", inline=True)
    await client.send_message(user, embed=embed)
    await client.say("Sent to the user!")

@client.command(pass_context=True)
async def apply(ctx):
    author = ctx.message.author
    await client.say(f"{author.mention} We have sent you the application. Please answer in the Verifacation chat.")
    embed = discord.Embed(color=0xf00000, timestamp=datetime.datetime.utcnow())
    embed.add_field(name="***__Application process:__***", value="What is your Discord Name and Tag? \n Why do you want to join? \n What clans have you been in and currently are in? \n Rate your skill in moomoo.io from 1-10", inline=False)
    embed.set_footer(icon_url=author.avatar_url, text="Application")
    await client.send_message(author, embed=embed)

@client.command(pass_context=True)
async def confirm(ctx, *, text = None):
    author = ctx.message.author
    if text is None:
        await client.say(f"{author.mention}, Sorry. We can't accept blank confirm pages.")
        return
    channel = discord.utils.get(ctx.message.server.channels, name="app-logs")
    embed = discord.Embed(color=0xf00000, timestamp=datetime.datetime.utcnow())
    embed.add_field(name="Users Application:", value=f"{text}", inline=False)
    embed.add_field(name="Author:", value=f"{author.mention}", inline=True)
    await client.send_message(channel, embed=embed)
    await client.say(f"{author.mention}, We have sent the staff team a message. We will get back to you ASAP. Please wait patiently.")

@client.command(pass_context=True)
async def verify(ctx, user: discord.Member = None):
    author = ctx.message.author
    if ctx.message.author.server_permissions.manage_roles:
        if user is None:
            await client.say(f"{author.mention} Please supply a mentioned user for me to accept into the clan!")
            return
        embed = discord.Embed(color=0xf00000, timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Verified!", value="Yay! One more member to the clan!", inline=True)
        embed.add_field(name="Current Member count!", value=len(ctx.message.server.members), inline=False)
        await client.say(embed=embed)
        UnverifiedRole = discord.utils.get(ctx.message.server.roles, name="Verification")
        VerifiedRole = discord.utils.get(ctx.message.server.roles, name="Verified")
        await client.remove_roles(user, UnverifiedRole)
        await client.add_roles(user, VerifiedRole)
        await client.remove_roles(user, UnverifiedRole)
    else:
        await client.say(f"{author.mention} You can't use this command! Permissions: ``Manage_Roles``")

@client.command(pass_context=True)
async def avatar(ctx, user: discord.Member = None):
    author = ctx.message.author
    if user is None:
        embed = discord.Embed(color=0xf00000, timestamp=datetime.datetime.utcnow())
        embed.add_field(name='Your avatar!', value=f"{author.mention}'s avatar!", inline=True)
        embed.set_image(url=author.avatar_url)
        embed.set_footer(text='Your avatar! Reminder: You can say: !avatar <user> for there profile picture!')
        await client.say(embed=embed)
    else:
        embed = discord.Embed(color=0xf00000, timestamp=datetime.datetime.utcnow())
        embed.add_field(name='You asked for an avatar!', value=f'{user.mention}s avatar!', inline=True)
        embed.set_image(url=user.avatar_url)
        embed.set_footer(text='The avatar!')
        await client.say(embed=embed)

@client.command(pass_context=True)
async def serverinfo(ctx):
    embed = discord.Embed(color=0xf00000, timestamp=datetime.datetime.utcnow())
    embed.set_author(name="Server info")
    embed.add_field(name="Name", value=ctx.message.server.name, inline=True)
    embed.add_field(name="ID", value=ctx.message.server.id, inline=True)
    embed.add_field(name="Roles", value=len(ctx.message.server.roles), inline=True)
    embed.add_field(name="Members", value=len(ctx.message.server.members))
    embed.set_thumbnail(url=ctx.message.server.icon_url)
    await client.say(embed=embed)

@client.command(pass_context=True)
async def userinfo(ctx, user: discord.Member = None):
    author = ctx.message.author
    if user is None:
        await client.say(f"{author.mention} Please specify a mentioned user!")
        return
    embed = discord.Embed(color=0xf00000, timestamp=datetime.datetime.utcnow())
    embed.add_field(name="Name", value=user.name, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="Status", value=user.status, inline=True)
    embed.add_field(name="Highest role", value=user.top_role)
    embed.add_field(name="Joined", value=user.joined_at)
    embed.set_thumbnail(url=user.avatar_url)
    await client.say(embed=embed)

    

    

client.run(TOKEN)

