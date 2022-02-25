import discord
from discord.ext import commands
import akinator as ak


class Akinator(commands.Cog):
    
    def __init__(self, client):
        self.client = client


    @commands.command(aliases=["aki", "akinator"])
    async def akinate(self, ctx):
        embed = discord.Embed(color = discord.Color.random())
        embed.description = "**Akinator is here to guess!**"
        await ctx.reply(embed = embed)
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ["y", "n","p","b"]
        try:
            aki = ak.Akinator()
            q = aki.start_game()
            s = 0
            while aki.progression <= 80:
                s += 1
                embed.title = f"Question - {'0' if s<10 else ''}{s}"
                embed.description = f"**{q}**\n\nYour Answer : `(y/n/p/b)`"
                embed.set_thumbnail(url = "https://en.akinator.com/bundles/elokencesite/images/akinator.png?v94")
                await ctx.reply(embed = embed)
                msg = await self.client.wait_for("message", check=check)
                if msg.content.lower() == "b":
                    try:
                        q=aki.back()
                    except ak.CantGoBackAnyFurther as e:
                        await ctx.send(e)
                        continue
                else:
                    try:
                        q = aki.answer(msg.content.lower())
                    except ak.InvalidAnswerError as e:
                        await ctx.send(e)
                        continue
            aki.win()
            embed.title = "The Game is ended!"
            embed.description = f"It's **{aki.first_guess['name']}** ({aki.first_guess['description']})! Was I correct? (`y/n`)"
            embed.set_image(url = aki.first_guess['absolute_picture_path'])
            await ctx.send(embed =embed)
            correct = await self.client.wait_for("message", check=check)
            if correct.content.lower() == "y":
                await ctx.send("Yay\n")
            else:
                await ctx.send("Oof\n")
        except Exception as e:
            await ctx.send(e)


def setup(client):
    client.add_cog(Akinator(client))
    print("Akinator is loaded!")