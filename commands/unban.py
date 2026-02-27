from discord.ext import commands
import discord

class UnbanCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member_id: str = None):
        if member_id is None or not member_id.isdigit():
            await ctx.reply("<:alerta:1369760471032533043> | Uso incorreto! Você deve inserir um ID válido do usuário a ser desbanido.")
            return
        
        member_id = int(member_id)  # Converter para número inteiro

        try:
            async for ban_entry in ctx.guild.bans():  # Iterar corretamente sobre os bans
                user = ban_entry.user
                if user.id == member_id:
                    await ctx.guild.unban(user)
                    await ctx.reply(f"<:matteofeliz:1370103769081319514> | {user} foi desbanido com sucesso!")
                    return
            
            await ctx.reply("<:alerta:1369760471032533043> | Usuário não encontrado na lista de banidos. Certifique-se de que o ID está correto.")
        
        except discord.Forbidden:
            await ctx.reply("<:alerta:1369760471032533043> | Não tenho permissão para visualizar a lista de banidos!")

async def setup(bot):
    await bot.add_cog(UnbanCommand(bot))