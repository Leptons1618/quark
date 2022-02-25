import discord
from discord.ext import commands
import akinator as ak
from discord_components import *

class Akinator(commands.Cog):
    
    def __init__(self, client):
        self.client = client


    @commands.command(aliases=["aki", "akinator"])
    async def akinate(self, ctx):
        """use !aki or !akinator or !akinate to start the game"""
        embed = discord.Embed(color = discord.Color.random())
        embed.description = "**Akinator is here to guess!**"
        m = await ctx.reply(embed = embed)

        buttons = [[
            Button(style=ButtonStyle.green, label="Yes", custom_id = "0"),
            Button(style=ButtonStyle.grey, label="No", custom_id = "1"),
            Button(style=ButtonStyle.blue, label="I Don't Know", custom_id = "2"),
            Button(style=ButtonStyle.blue, label="Probably", custom_id = "3"),
            Button(style=ButtonStyle.blue, label="Probably Not", custom_id = "4"),
        ],[
            Button(style=ButtonStyle.red, label="Back", custom_id = "5"),
            ]]
        dbuttons = [[
            Button(style=ButtonStyle.green, label="Yes", custom_id = "0", disabled = True),
            Button(style=ButtonStyle.grey, label="No", custom_id = "1", disabled = True),
            Button(style=ButtonStyle.blue, label="I Don't Know", custom_id = "2", disabled = True),
            Button(style=ButtonStyle.blue, label="Probably", custom_id = "3", disabled = True),
            Button(style=ButtonStyle.blue, label="Probably Not", custom_id = "4", disabled = True),
        ],[
            Button(style=ButtonStyle.red, label="Back", custom_id = "5", disabled = True),
            ]]
        try:
            aki = ak.Akinator()
            q = aki.start_game()
            s = 0
            while aki.progression <= 80:
                s += 1
                embed.title = f"Question - {'0' if s<10 else ''}{s}"
                embed.description = f"**{q}**"
                embed.set_thumbnail(url = "https://en.akinator.com/bundles/elokencesite/images/akinator.png?v94")
                await m.edit(embed = embed, components = buttons)
                def check(interaction):
                    return interaction.message == m and interaction.author == ctx.author
                interaction = await self.client.wait_for("button_click", check=check, timeout = 300)
                if interaction.custom_id == "5":
                    q = aki.back()
                    s = s - 2
                    await interaction.respond(components = buttons, type = 7)
                else:
                    q = aki.answer(interaction.component.label.lower())
                    await interaction.respond(components = buttons, type = 7)
            await m.edit(components = dbuttons)
            aki.win()
            embed.title = "The Game is ended!"
            embed.description = f"It's **{aki.first_guess['name']}**\n**Description :** {aki.first_guess['description']}!"
            embed.set_image(url = aki.first_guess['absolute_picture_path'])
            await ctx.send(embed =embed)
            embed = discord.Embed(color = discord.Color.random())
            embed.description = "**Was I correct? (Yes/No)**"
            ms = await ctx.send(embed = embed, components = [
                [Button(label = "Yes", style = ButtonStyle.green, custom_id = "yes"),
                Button(label = "No", style = ButtonStyle.grey, custom_id = "no")]
                ])
            def check(interaction):
                    return interaction.message == ms and interaction.author == ctx.author
            interaction = await self.client.wait_for("button_click", check=check, timeout = 300)
            if interaction.custom_id == "yes":
                embed.description = "Yah, I am right!"
                await interaction.respond(embed = embed, type = 7, components = [
                    [Button(label = "Yes", style = ButtonStyle.green, custom_id = "yes", disabled = True),
                     Button(label = "No", style = ButtonStyle.grey, custom_id = "no", disabled = True)]
                ])
            else:
                embed.description = "Oof, Something was wrong with me! Play next time I will try to guess correct."
                await interaction.respond(embed = embed, type = 7, components = [
                    [Button(label = "Yes", style = ButtonStyle.green, custom_id = "yes", disabled = True),
                     Button(label = "No", style = ButtonStyle.grey, custom_id = "no", disabled = True)]
                ])
        except Exception as e:
            await ctx.send(e)


def setup(client):
    client.add_cog(Akinator(client))
    print("Akinator is loaded!")