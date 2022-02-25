import discord
from discord.ext import commands
from discord.ext.commands import bot
import akinator as ak
from discord_components import *


client = commands.Bot(command_prefix = commands.when_mentioned_or('!'))
client.remove_command('help')
DiscordComponents(client)

@client.event
async def on_ready():
  print('Bot Is Ready')


@client.event
async def on_message(message):
    try:
        if message.mentions[0] == client.user:
            embed = discord.Embed(
              title = client.user, 
              description = f'```\nUse ! prifix to use the bot and for more information use !help\n```',
              color = discord.Color.green(),
            )
            await message.channel.send(embed = embed)
    except:
        pass
    await client.process_commands(message)




@client.command()
async def help(ctx, command = None):
  if not command:
    button = [Button(style = ButtonStyle.URL, url = 'https://discord.com/api/oauth2/authorize?client_id=795670723343286343&permissions=8&scope=bot', label = 'invite me')]
    embed = discord.Embed(color = discord.Color.blue())
    embed.set_author(name = client.user.name, icon_url = client.user.avatar_url)
    embed.title = 'Commands Categories'
    embed.description = '> `!hello          :` chatbot\n' \
                        '> `!akinator/!aki  :` akinator guess bot'
    embed.set_thumbnail(url = client.user.avatar_url)
    embed.set_footer(text = f'Requesed by {ctx.author.name}')
    await ctx.send(embed = embed, components = button)
  else:
    cmd = client.get_command(command)
    if not command: return await ctx.send("Command not found!")
    embed = discord.Embed(
      title = f"Command : {cmd.name}",
      description = cmd.description,
      color = discord.Color.random()
    )
    if not cmd.aliases:
      aliases = "None"
    else:
      aliases = ", ".join(cmd.aliases)

    embed.add_field(
      name = "Aliases",
      value = f"`{aliases}`",
      inline = False
    ).add_field(
      name = "Usage",
      value = f"`{ctx.prefix}{cmd.name} {cmd.usage}`",
      inline = False
    ).add_field(
      name = "Example",
      value = f"`{ctx.prefix}{cmd.name} {cmd.brief}`",
      inline = False
    )
    embed.set_thumbnail(url = client.user.avatar_url)
    await ctx.send(embed = embed)
    


@client.command()
async def invite(message):
    embed = discord.Embed(description = '[Click Here](https://discord.com/api/oauth2/authorize?client_id=795670723343286343&permissions=8&scope=bot)', color = 0x00ff00)
    embed.set_footer(text = 'made by Leptons#4142', icon_url = 'https://cdn.discordapp.com/attachments/781843712489685076/795690819130097664/539043631c7bdee39d16fe326897df6e.jpg')
    await message.send(embed = embed)
    

client.load_extension("Akinator.aki")
client.load_extension("ChatBot.chatbot")

client.run('Nzk1NjcwNzIzMzQzMjg2MzQz.X_MwGw.ZXsbs2eWNMtngowLT-c_5LvmyeM')
