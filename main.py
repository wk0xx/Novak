import discord
from discord.ext import commands
import os
def get_prefix(bot, message):

    return ['n', 'N']

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True  # Necessário para verificar cargos

bot = commands.Bot(command_prefix=get_prefix, intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f'Logado como {bot.user.name}')
    for filename in os.listdir('./commands'):
        if filename.endswith('.py'):
            await bot.load_extension(f'commands.{filename[:-3]}')


    

bot.run(os.getenv("TOKEN"))