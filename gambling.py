import sqlite3, random
conn = sqlite3.connect("data_gamble.db")
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER,
        name TEXT,
        money INTEGER,
        credit INTEGER
    )
''')
async def buy_token(ctx, id):
    user_id = id
    bot = ctx.bot
    cursor.execute('SELECT * FROM users WHERE id=?', (user_id,))
    row = cursor.fetchone()
    if row:
        message = await ctx.send(
            "**Credits Score** \n"
            f"```Current Money: ${row[2]}``` \n"
            "```"
            "1. $30 - 5 token \n"
            "2. $50 - 10 token \n"
            "3. $60 - 20 token \n"
            "4. $100 - 30 token \n"
            "```"
        )
        select_num = ['1️⃣', '2️⃣', '3️⃣', '4️⃣']
        for emojis in select_num:
            await message.add_reaction(emojis)
        
        def check(reaction, user):
            return user != bot.user and reaction.message.id == message.id and str(reaction.emoji) in select_num
        try:
            reaction, user = await bot.wait_for("reaction_add", timeout=10.0, check=check)
            money_update = None
            credit_update = None
            success_update = False
            if str(reaction.emoji) == "1️⃣" and row[2] >=30:
                money_update = 30
                credit_update = 5
                success_update = True
                await ctx.send("**Transaction Successfully!**")
            elif str(reaction.emoji) == "2️⃣" and row[2] >=50:
                money_update = 50
                credit_update = 10
                success_update = True
                await ctx.send("**Transaction Successfully!**")
            elif str(reaction.emoji) == "3️⃣" and row[2] >=60:
                money_update = 60
                credit_update = 20
                success_update = True
                await ctx.send("**Transaction Successfully!**")
            elif str(reaction.emoji) == "4️⃣" and row[2] >=100:
                money_update = 100
                credit_update = 30
                success_update = True
                await ctx.send("**Transaction Successfully!**")
            else:
                await ctx.send("**You don't have enough money**")
            if success_update:
                cursor.execute('UPDATE users SET money = money - ? WHERE id=?', (money_update, user_id, ))
                cursor.execute('UPDATE users SET credit = credit + ? WHERE id=?', (credit_update, user_id,))
                cursor.execute('SELECT * FROM users WHERE id=?', (user_id,))
                update = cursor.fetchone()
                if update: await ctx.send(f"```Current Money ${update[2]}```")
            conn.commit()
        except Exception:
            await ctx.send("**Timeout please try again!!**")

async def check_money(ctx, id):
    user_id = id
    cursor.execute('SELECT * FROM users WHERE id=?', (user_id,))
    row = cursor.fetchone()
    if row:
        await ctx.send(f"```Current Money: ${row[2]}```")

async def gamble_start(ctx, id, name):
    bot = ctx.bot
    user_id = id
    user_name = name
    cursor.execute('SELECT * FROM users WHERE id=?', (user_id,))
    row = cursor.fetchone()
    if row:
        if row[3] <= 0:
            await ctx.send(f"**Sorry {row[1]}, you don't have enough credits to gamble.**")
            return
        message = await ctx.send(
            f"**{row[1]}! \n**"
            "```"
            f"Money: ${row[2]} \n"
            f"Credits: {row[3]} \n"
            "```"
            "**React: 🪙 - to start**"
        )
        await message.add_reaction('🪙')
        def check(reaction, user):
            return user != bot.user and str(reaction.emoji) == '🪙' and reaction.message.id == message.id
        try:
            await bot.wait_for("reaction_add", timeout=10.0, check=check)
            cursor.execute('UPDATE users SET credit = credit - 1 WHERE id=?', (user_id,))
            conn.commit()
            await ctx.send(
                "**Poll list***"
                "```"
                "🔵 - $30 \n"
                "🟣 - $60 \n"
                "🟡 - $90 \n"
                "🟢 - $120 \n"
                "💙 - $150"
                "```"
            )
            color_prizes = {
                "🔵": 10,
                "🟣": 20,
                "🟡": 30,
                "🟢": 40,
                "💙": 50
            }
            emoji_probabilities = {
                "🔵": 0.7,
                "🟣": 0.4,
                "🟡": 0.7,
                "🟢": 0.2,
                "💙": 0.01
            }
            emojis = list(emoji_probabilities.keys())
            probabilities = list(emoji_probabilities.values())
            slots = [None, None, None]
            threshold = 10
            spin = await ctx.send("**Spinning...**")
            for _ in range(threshold):
                slots[0] = random.choices(emojis, probabilities)[0]
                slots[1] = random.choices(emojis, probabilities)[0]
                slots[2] = random.choices(emojis, probabilities)[0]
                await spin.edit(content=f"```({slots[0]} | {slots[1]} | {slots[2]})```")
            if slots[0] == slots[1] == slots[2]:
                jackpot_prize = color_prizes[slots[0]] * 3
                await ctx.send(f"**JACKPOT! All slots are {slots[0]}! You win {jackpot_prize} money!**")
                cursor.execute(f'UPDATE users SET money = money + ? WHERE id=?', (jackpot_prize, user_id,))
            else:
                await ctx.send("**awwww dang it!!!**")
            conn.commit()

        except Exception:
            await ctx.send("**Timeout please try again!!**")
    else:
        await ctx.send("Your data has been uploaded")
        cursor.execute('INSERT INTO users(id, name, money, credit) VALUES(?, ?, ?, ?)', (user_id, user_name, 1000, 10))
        conn.commit()