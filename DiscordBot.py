import discord
import glob
from discord.ext import commands
from pretty_help import PrettyHelp, EmojiMenu
import random

PREFIX = ("!")
global languageFilter
languageFilter = False

with open('BadWords.txt', 'r') as f:
    words = f.read()
    badwords = words.splitlines()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
    

bot = commands.Bot(
    command_prefix = PREFIX, 
    activity = discord.Activity(type=discord.ActivityType.listening, name="!help"), 
    status=discord.Status.online, 
    description = 'Just your average Tim Bot :)', 
    help_command=PrettyHelp(color = discord.Colour.gold(), 
    index_title = "Tim Bot's Commands"), 
    menu = EmojiMenu('◀️', '▶️', '❌'), 
    intents = intents
    )

@bot.event
async def on_ready():
    print("Bot Running!")
    channel = bot.get_channel(785593784389337089)
    ruleChannel = bot.get_channel(470733661906665474)
    await channel.purge(limit=100) 
    text= "React to this message to change your roll!"
    moji = await channel.send(text)
    ruleMsg = await ruleChannel.fetch_message(470734425609601034)
    await moji.add_reaction('🧑‍🍳')
    await moji.add_reaction('💪')
    await ruleMsg.add_reaction('🔥')

@bot.event
async def on_reaction_add(reaction, user):
    mastapastaID = discord.utils.get(user.guild.roles, id = 625859592748007444)
    chadsID = discord.utils.get(user.guild.roles, id = 625860478039752736)
    eliteID = discord.utils.get(user.guild.roles, id = 401862477488455682)
    roleChannel = bot.get_channel(785593784389337089)
    ruleChannel = bot.get_channel(470733661906665474)
    if user == bot.user:
        return
    if reaction.message.channel.id == roleChannel.id:
        if reaction.emoji == "🧑‍🍳":
            await user.add_roles(mastapastaID)
            await user.remove_roles(chadsID)
            await reaction.message.remove_reaction('💪', user)
        if reaction.emoji == "💪":
            await user.add_roles(chadsID)
            await user.remove_roles(mastapastaID)
            await reaction.message.remove_reaction('🧑‍🍳', user)

    if reaction.message.channel.id == ruleChannel.id:
        if reaction.emoji == "🔥":
            await user.add_roles(eliteID)

@bot.event
async def on_reaction_remove(reaction, user):
    mastapastaID = 625859592748007444
    chadsID = 625860478039752736
    channel = bot.get_channel(785593784389337089)
    if reaction.message.channel.id != channel.id:
        return
    if reaction.emoji == "🧑‍🍳":
      Role = discord.utils.get(user.guild.roles, id = mastapastaID)
      await user.remove_roles(Role)
    if reaction.emoji == "💪":
      Role = discord.utils.get(user.guild.roles, id = chadsID)
      await user.remove_roles(Role)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.content.lower() == 'pretty please':
        await message.channel.send(message.author.mention + " did say pretty please...")
    
    if languageFilter:
        for word in badwords:
            if word in message.content.lower():
                await message.delete()
                await message.channel.send(message.author.mention + " don't use that word!")
                break

    await bot.process_commands(message)


@bot.command(brief = 'Flips Helen Keller!', aliases = ['CoinFlip', 'coinFlip'])
async def coinflip(ctx):
    try:
        if random.random() < .5:
            await ctx.send("https://www.usmint.gov/wordpress/wp-content/uploads/2016/06/2003-50-state-quarters-coin-alabama-proof-reverse.jpg")
        else:
            await ctx.send("https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/2006_Quarter_Proof.png/800px-2006_Quarter_Proof.png")
    except:
        await ctx.send("Invalid use of command!")

@bot.command(brief = 'Rolls a die.', aliases = ['dieroll', 'DieRoll'])
async def dieRoll(ctx):
    try:
        await ctx.send("Rolled: " + str(random.randint(1, 6)))
    except:
        await ctx.send("Invalid use of command!")
   
@bot.command(brief = 'Randal finder', aliases = ['Randel', 'Randal', 'randal'])
async def randel(ctx):
    try:
        file_path_type = "./randelImages/*.jpg"
        images = glob.glob((file_path_type))
        random_image = random.choice(images)
        await ctx.send(file=discord.File(random_image))
    except:
        await ctx.send('Use !randal to get a random picture of randal')

@bot.command(brief = 'Returns metioned avatar', aliases = ['Avatar'])
async def avatar(ctx, *,  avamember : discord.Member=None):
    try:
        await ctx.send("Here is " + avamember.mention + "'s pfp")
        await ctx.send(avamember.avatar)
    except:
        await ctx.send("You need to mentions someone after !avatar for this command to work.")

@bot.command(brief = 'toggles the language filter', aliases = ['ToggleFilter', 'toggleFilter'])
async def togglefilter(ctx):
    global languageFilter
    if languageFilter:
        await ctx.send(ctx.message.author.mention + " has turned off the language filter.")
        languageFilter = False
    else:
        await ctx.send(ctx.message.author.mention + " has turned on the language filter.")
        languageFilter = True
        
@bot.command(brief='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))


@bot.command(brief = 'Tells you when mentioned user joined server')
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')

bot.run('NzUzMzIzNjU2OTI2NzI0MTU4.G9BSse.adk5sPw21hDgW7fHNfkvAVaAW-WG7Bq1zVgKCU')

