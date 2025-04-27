import random, requests, discord
from io import BytesIO

def tenor_gif(query):
    tenor_apikey = "AIzaSyDL02XwLbQJxOFWwx3KdRYaRzmxkTftghY"
    tenor_limit = 10
    tenor_ckey = "mirei_kei"
    r = requests.get("https://tenor.googleapis.com/v2/search?q=%s&key=%s&client_key=%s&limit=%s" % (query, tenor_apikey, tenor_ckey,  tenor_limit))
    if r.status_code == 200:
        data = r.json()
        gifs = [result["media_formats"]["gif"]["url"] for result in data["results"]]
        if gifs:
            random_gif = random.choice(gifs)
            return random_gif
        else:
            return None

async def get_gif(ctx, user_id, query, title):
    try:
        mention_id = f"{user_id}"
        mention_bot = "<@1364861003002810370>"
        url = tenor_gif(query)
        response = requests.get(url)
        response.raise_for_status()
        file = discord.File(BytesIO(response.content), filename=url.split("/")[-1])
        if mention_id == mention_bot:
            res = "**Why?? :((**" if query == "anime killing" else "**That's so sweet >_<**"
            await ctx.send(f"{res}", file=file)
        else:
            await ctx.send(f"**{title}** {mention_id}", file=file)
    except:
        await ctx.send("Connection lost, please try again")