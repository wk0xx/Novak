from discord.ext import commands
import discord
from datetime import datetime

class KickCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member = None, *, reason="Não declarado"):
        if member is None:
            await ctx.reply("<:alerta:1369760471032533043> | Você precisa mencionar um membro para expulsá-lo!")
            return
        embed = discord.Embed(
            title="<:helper:1370769074841194567> Você foi Expulso!",
            color=discord.Color.red()
        )
        embed.add_field(name="<:SvPontoBranco:1370403290491256832> Servidor:", value=ctx.guild.name, inline=False)
        embed.add_field(name="<:SvPontoBranco:1370403290491256832> Admin:", value=ctx.author.mention, inline=False)
        embed.add_field(name="<:SvPontoBranco:1370403290491256832> Motivo:", value=reason, inline=False)
        embed.set_footer(text="Por favor, leia as regras e evite punições.")

        try:
            await member.send(embed=embed)
        except:
            await ctx.reply("<:alerta:1369760471032533043> | Não foi possível enviar a mensagem privada ao membro.")
        await member.kick(reason=reason)
        await ctx.reply(f'<:Offline:1372210713518411817> | {member} foi expulso por {ctx.author.mention}. Motivo: **{reason}**')

        # Criando a embed para enviar na DM do membro
        

async def setup(bot):
    await bot.add_cog(KickCommand(bot))