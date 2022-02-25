import discord
from discord.ext import commands
import requests

class chatbot(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command(
    name = "hello",
    aliases = [],
    description = "",
    usage = "",
    brief = ""
  )
  async def hello(self, messg):
    if not messg.guild:
      return
    if messg.author.bot:
      return
    def check(message):
      return message.author == messg.author and message.channel == messg.channel


    # with open('data.json', 'r') as r:
    #   data = r.read()

    url = f'https://api-docs.pgamerx.com/v/docs/reference/free/ai-response/ai'
    response = requests.get(url).json()
    
      
    await messg.reply(response.get('cnt'), mention_author = False)
    while True:
      message = await self.client.wait_for('message', timeout = 60, check = check)
    # if message.content.startswith(self.client.user.mention):
      msg = message.content
      
      url = f'https://api-docs.pgamerx.com/v/docs/reference/free/ai-response/ai'
      response = requests.get(url).json()
      
      await message.reply(response.get('cnt'), mention_author = False)
      

def setup(client):
  client.add_cog(chatbot(client))
  print("chatbot loaded")
