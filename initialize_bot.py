import discord
from discord.ext import commands
from tenor import get_gif
from gambling import gamble_start, check_money, buy_token

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="%", intents=intents)

#commands
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")

@bot.command(name="guide")
async def guide(ctx):
    page_list = [
        "**Command List**"
        "```"
        "1. hugs - hugs the mention user \n"
        "2. kiss - kiss the mention user \n"
        "3. pat - pat the mention user \n"
        "4. kick - kick the mention user \n"
        "5. smack - smack the mention user \n"
        "```",
        "**Command List**"
        "```"
        "6. cuddle - cuddle the mention user\n"
        "7. guide - shows the list of commands"
        "```"
    ]
    current_page = 0
    message = await ctx.send(page_list[current_page])
    await message.add_reaction("⬅️")
    await message.add_reaction("➡️")
    def check(reaction, user):
        return (user == ctx.author and reaction.message.id == message.id and str(reaction.emoji) in ["⬅️", "➡️"])
    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", timeout=10.0, check=check)
            if str(reaction.emoji) == "➡️":
                if current_page < len(page_list) - 1:
                    current_page += 1
                    await message.edit(content=page_list[current_page])
            elif str(reaction.emoji) == "⬅️":
                if current_page > 0:
                    current_page -= 1
                    await message.edit(content=page_list[current_page])
        except Exception:
            await ctx.send("**Timeout please try again!!**")
            break

@bot.command(name="hugs")
async def hugs(ctx, member : discord.Member):
    await get_gif(ctx, member.mention, "anime hug", "Pats you!")

@bot.command(name="kiss")
async def kiss(ctx, member : discord.Member):
    await get_gif(ctx, member.mention, "anime kiss", "Kiss you!")

@bot.command(name="pat")
async def pat(ctx, member : discord.Member):
    await get_gif(ctx, member.mention, "anime pat", "Pats you!") 

@bot.command(name="kick")
async def kick(ctx, member : discord.Member):
    await get_gif(ctx, member.mention, "anime kick", "Kicks you!") 

@bot.command(name="smack")
async def smack(ctx, member : discord.Member):
    await get_gif(ctx, member.mention, "anime smack", "Smacks you!")

@bot.command(name="cuddle")
async def cuddle(ctx, member : discord.Member):
    await get_gif(ctx, member.mention, "anime cuddle", "Cuddles you!")

@bot.command(name="kill")
async def kill(ctx, member : discord.Member):
    await get_gif(ctx, member.mention, "anime killing", "Kill you!")

@bot.command(name="gamble")
async def gambling(ctx):
    await gamble_start(ctx, ctx.author.id, ctx.author.name)

@bot.command(name="balance")
async def balance(ctx):
    await check_money(ctx, ctx.author.id)

@bot.command(name="token")
async def token(ctx):
    await buy_token(ctx, ctx.author.id)

bot.run("")