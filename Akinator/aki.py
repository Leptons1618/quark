import discord
from discord.ext import commands
import akinator as ak
from discord_components import *

class Akinator(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    @commands.command(
        name = "akilang",
        description = "Get list of languages of akinator game.",
        aliases = ["langofaki"],
        usage = "",
        brief = ""
        )
    async def akilang(self, ctx):
        languages = "• `en:` English (default)\n" \
                    "• `en_objects:` English server for guessing objects. Here, Akinator will attempt to guess the object you're thinking instead of a character\n" \
                    "• `en_animals:` English server for guessing animals. Here, Akinator will attempt to guess the animal you're thinking instead of a character\n" \
                    "• `ar:` Arabic\n" \
                    "• `cn:` Chinese\n" \
                    "• `de:` German\n" \
                    "• `de_animals:` German server for guessing animals\n" \
                    "• `es:` Spanish\n" \
                    "• `es_animals:` Spanish server for guessing animals\n" \
                    "• `fr:` French\n" \
                    "• `fr_animals:` French server for guessing animals\n" \
                    "• `fr_objects:` French server for guessing objects\n" \
                    "• `il:` Hebrew\n" \
                    "• `it:` Italian\n" \
                    "• `it_animals:` Italian server for guessing animals\n" \
                    "• `jp:` Japanese\n" \
                    "• `jp_animals:` Japanese server for guessing animals\n" \
                    "• `kr:` Korean\n" \
                    "• `nl:` Dutch\n" \
                    "• `pl:` Polish\n" \
                    "• `pt:` Portuguese\n" \
                    "• `ru:` Russian\n" \
                    "• `tr:` Turkish\n" \
                    "• `id:` Indonesian\n"
        embed = discord.Embed(
            title = "Languages of Akinator",
            description = languages,
            color = discord.Color.random()
            )
        await ctx.send(embed = embed)


    @commands.command(
        name = "akinator",
        description = "Akinator will guess who/what you're thinking of!",
        aliases = ["aki", "akinate"],
        usage = "(language)",
        brief = "en"
        )
    async def akinate(self, ctx, language = "en"):
        languages = ["cn", "ar", "en_animals", "en_objects", "en",
                     "fr", "es_animals", "es", "de_animals", "de",
                     "it_animals", "it", "il", "fr_objects", "fr_animals",
                     "pl", "nl", "kr", "jp_animals", "jp", "id",
                     "tr", "ru", "pt"]
        if language.lower() not in languages: return await ctx.send(f"Couldn't find that language, use `{ctx.prefix}akilang` to get the list of languages.")
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
            Button(style=ButtonStyle.red, label="End", custom_id = "6"),
            ]]
        dbuttons = [[
            Button(style=ButtonStyle.green, label="Yes", custom_id = "0", disabled = True),
            Button(style=ButtonStyle.grey, label="No", custom_id = "1", disabled = True),
            Button(style=ButtonStyle.blue, label="I Don't Know", custom_id = "2", disabled = True),
            Button(style=ButtonStyle.blue, label="Probably", custom_id = "3", disabled = True),
            Button(style=ButtonStyle.blue, label="Probably Not", custom_id = "4", disabled = True),
        ],[
            Button(style=ButtonStyle.red, label="Back", custom_id = "5", disabled = True),
            Button(style=ButtonStyle.red, label="End", custom_id = "6", disabled = True),
            ]]

        try:
            aki = ak.Akinator()
            q = aki.start_game(language = language)
            s = 0
            while aki.progression <= 80:
                s += 1
                embed.title = f"Question - {'0' if s<10 else ''}{s}"
                embed.description = f"**{q}**"
                embed.set_thumbnail(url = "https://en.akinator.com/bundles/elokencesite/images/akinator.png?v94")
                await m.edit(embed = embed, components = buttons)
                def check(interaction):
                    return interaction.message == m and interaction.author == ctx.author
                try:
                    interaction = await self.client.wait_for("button_click", check=check, timeout = 300)
                except:
                    embed.title = "The Game has Ended!"
                    embed.description = "You've failed to reply within time."
                    return await m.edit(embed = embed, components = dbuttons)
                if interaction.custom_id == "5":
                    q = aki.back()
                    s = s - 2
                    await interaction.respond(components = buttons, type = 7)
                elif interaction.custom_id == "6":
                    embed = discord.Embed(color = discord.Color.random())
                    embed.title = "The Game has Ended!"
                    await interaction.respond(embed = embed, components = dbuttons, type = 7)
                    return
                else:
                    q = aki.answer(interaction.component.label.lower())
                    await interaction.respond(components = buttons, type = 7)
            await m.edit(components = dbuttons)
            aki.win()
            embed.title = "The Game has Ended!"
            embed.description = f"It's **{aki.first_guess['name']}**\n**Description :** {aki.first_guess['description']}!"
            embed.set_image(url = aki.first_guess['absolute_picture_path'])
            await ctx.send(embed =embed)
            embed = discord.Embed(color = discord.Color.random())
            embed.description = "**Am I right? (Yes/No)**"
            ms = await ctx.send(embed = embed, components = [
                [Button(label = "Yes", style = ButtonStyle.green, custom_id = "yes"),
                Button(label = "No", style = ButtonStyle.grey, custom_id = "no")]
                ])
            def check(interaction):
                    return interaction.message == ms and interaction.author == ctx.author
            interaction = await self.client.wait_for("button_click", check=check, timeout = 300)
            if interaction.custom_id == "yes":
                embed.title = "Yah, I am right!"
                embed.description = ""
                embed.description = "I enjoyed playing with you!"
                await interaction.respond(embed = embed, type = 7, components = [
                    [Button(label = "Yes", style = ButtonStyle.green, custom_id = "yes", disabled = True),
                     Button(label = "No", style = ButtonStyle.grey, custom_id = "no", disabled = True)]
                ])
            else:
                embed.title = "Oof, you win"
                embed.description = "I enjoyed playing with you!"
                await interaction.respond(embed = embed, type = 7, components = [
                    [Button(label = "Yes", style = ButtonStyle.green, custom_id = "yes", disabled = True),
                     Button(label = "No", style = ButtonStyle.grey, custom_id = "no", disabled = True)]
                ])
        except Exception as e:
            await ctx.send(e)


def setup(client):
    client.add_cog(Akinator(client))
    print("Akinator is Loaded!")