from discord.ext import commands
import discord

class BanCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member = None, *, motivo: str = "Não declarado"):
        if member is None:
            await ctx.reply("<:Pontobranco:1476726754457550929> | Uso incorreto! Você deve mencionar um membro e especificar um motivo.")
            return

        try:
            # Criar embed para a DM
            embed = discord.Embed(title="❗ Você foi banido!", color=discord.Color.red())
            embed.add_field(name="<:Pontobranco:1476726754457550929> Servidor", value=ctx.guild.name, inline=False)
            embed.add_field(name="<:Pontobranco:1476726754457550929> Admin", value=ctx.author.name, inline=False)
            embed.add_field(name="<:Pontobranco:1476726754457550929> Motivo", value=motivo, inline=False)
            embed.set_footer(text="Caso tenha dúvidas, entre em contato com a administração.")

            await member.send(embed=embed)
        except discord.Forbidden:
            await ctx.reply(f"<:Pontobranco:1476726754457550929> | Não foi possível enviar uma mensagem privada para {member.mention}. O usuário pode ter mensagens diretas desativadas.")

        await ctx.guild.ban(member, reason=motivo)
        await ctx.reply(f"<:Pontobranco:1476726754457550929> | {member.mention} foi banido por {ctx.author.mention}. Motivo: **{motivo}**.")

async def setup(bot):
    await bot.add_cog(BanCommand(bot))