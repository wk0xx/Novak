from discord.ext import commands
import discord
import asyncio
import re

class MuteCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member = None, duration: str = None):
        if member is None or duration is None:
            await ctx.reply("**ERRO** | Uso incorreto! Você deve mencionar um membro e especificar o tempo (exemplo: `hmute @usuario 10m`).")
            return
        
        # Expressão regular para validar e converter tempo
        match = re.match(r"(\d+)([smh])?", duration)
        if not match:
            await ctx.reply("**ERRO** | Formato inválido! Use um número seguido de `s` (segundos), `m` (minutos) ou `h` (horas). Exemplo: `10m`.")
            return
        
        time_value = int(match.group(1))
        time_unit = match.group(2) or "m"  # Padrão para minutos

        # Converter para segundos
        time_multiplier = {"s": 1, "m": 60, "h": 3600}
        mute_seconds = time_value * time_multiplier[time_unit]

        mute_role = discord.utils.get(ctx.guild.roles, name="Mutado")
        if not mute_role:
            mute_role = await ctx.guild.create_role(name="Mutado")
            for channel in ctx.guild.channels:
                await channel.set_permissions(mute_role, speak=False, send_messages=False)

        await member.add_roles(mute_role)
        await ctx.reply(f"<:Pontobranco:1476726754457550929>  | {member.mention} foi mutado por {ctx.author.mention}, Tempo: **{time_value}{time_unit}**.")

        # Criar embed para a mensagem privada
        embed = discord.Embed(title="❗ | Você foi mutado!", color=discord.Color.red())
        embed.add_field(name="<:Pontobranco:1476726754457550929> Servidor", value=ctx.guild.name, inline=False)
        embed.add_field(name="<:Pontobranco:1476726754457550929> Admin", value=ctx.author.name, inline=False)
        embed.add_field(name="<:Pontobranco:1476726754457550929> Tempo", value=f"{time_value}{time_unit}", inline=False)
        embed.set_footer(text="Por favor, siga as regras para evitar punições futuras.")

        # Enviar mensagem privada ao usuário mutado
        try:
            await member.send(embed=embed)
        except discord.Forbidden:
            await ctx.reply(f"Não foi possível enviar uma mensagem privada para {member.mention}. O usuário pode ter mensagens diretas desativadas.")

        await asyncio.sleep(mute_seconds)
        await member.remove_roles(mute_role)
        await ctx.reply(f"<:Pontobranco:1476726754457550929>  | {member.mention} foi desmutado automaticamente.")

async def setup(bot):
    await bot.add_cog(MuteCommand(bot))