from discord.ext import commands
import discord
import re

class AntiLink(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        # Expressão regular para detectar links e convites do Discord
        link_pattern = r"https?://(?:www\.)?\S+\.\S+"
        invite_pattern = r"(discord\.gg|discord\.com/invite)/\S+"

        if re.search(link_pattern, message.content) or re.search(invite_pattern, message.content):
            try:
                await message.delete()
                await message.channel.send(f"<:alerta:1369760471032533043> | {message.author.mention}, links e convites não são permitidos!", delete_after=5)
            except discord.Forbidden:
                await message.channel.send("<:alerta:1369760471032533043> | Não tenho permissão para excluir mensagens!")

async def setup(bot):
    await bot.add_cog(AntiLink(bot))