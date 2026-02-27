import discord
from discord.ext import commands
import asyncio
import random
import re

# ID do cargo autorizado
CARGO_REQUERIDO_ID = 1369838853728505856  # Substitua pelo ID real

# Função para converter tempo
def converter_tempo(tempo_str):
    tempo_str = tempo_str.lower()
    padroes = {
        's': 1, 'seg': 1,
        'm': 60, 'min': 60,
        'h': 3600, 'hora': 3600,
        'd': 86400, 'dia': 86400
    }
    match = re.fullmatch(r'(\d+)([a-zA-Z]+)', tempo_str)
    if match:
        valor, unidade = match.groups()
        return int(valor) * padroes.get(unidade, 0)
    return 0

# Função para formatar tempo
def formatar_tempo(segundos):
    m, s = divmod(segundos, 60)
    h, m = divmod(m, 60)
    partes = []
    if h: partes.append(f"{h}h")
    if m: partes.append(f"{m}m")
    if s or not partes: partes.append(f"{s}s")
    return ' '.join(partes)

# View com botão de participação
class SorteioView(discord.ui.View):
    def __init__(self, timeout: int):
        super().__init__(timeout=timeout)
        self.participantes = set()

    @discord.ui.button(label="🎉 Participar", style=discord.ButtonStyle.green)
    async def participar(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.user
        if user.id in self.participantes:
            await interaction.response.send_message("Você já está participando!", ephemeral=True)
        else:
            self.participantes.add(user.id)
            await interaction.response.send_message("Você entrou no sorteio!", ephemeral=True)

# Cog principal
class Sorteio(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="sorteio")
    async def sorteio(self, ctx, tempo: str, ganhadores: int, *, premio: str):
        cargo_autorizado = discord.utils.get(ctx.author.roles, id=CARGO_REQUERIDO_ID)
        if not cargo_autorizado:
            return await ctx.reply("<:matteobravo:1370104694852292681> | Você não tem permissão para usar este comando.")

        tempo_segundos = converter_tempo(tempo)
        if tempo_segundos <= 0 or ganhadores <= 0:
            return await ctx.reply("<:matteobravo:1370104694852292681> | O tempo e a quantidade de ganhadores devem ser válidos.")

        view = SorteioView(timeout=tempo_segundos)
        embed = discord.Embed(
            title="<:moneymatteo:1369235455652139099> | Novo Sorteio!",
            description="<:matteoteo:1370110174500622576> Clique no botão abaixo para participar!",
            color=discord.Color.green()
        )
        embed.add_field(name="<:SvPontoBranco:1370403290491256832> Prêmio", value=f"<:seta:1370757772333023232> **{premio}**")
        embed.add_field(name="<:SvPontoBranco:1370403290491256832> Ganhadores", value=f"<:seta:1370757772333023232> **{ganhadores}**")
        embed.add_field(name="<:SvPontoBranco:1370403290491256832> Tempo", value=f"<:seta:1370757772333023232> **{formatar_tempo(tempo_segundos)}**", inline=False)

        tempo_msg = await ctx.reply(embed=embed, view=view)

        for restante in range(tempo_segundos, 0, -1):
            if restante % 10 == 0 or restante <= 5:
                embed.set_field_at(index=2, name="<:SvPontoBranco:1370403290491256832> Tempo", value=f"<:seta:1370757772333023232> **{formatar_tempo(restante)}**", inline=False)
                await tempo_msg.edit(embed=embed)
            await asyncio.sleep(1)

        view.stop()

        if not view.participantes:
            return await ctx.reply("<:matteosad:1370155131626328254> | Ninguém participou do sorteio.")

        if ganhadores > len(view.participantes):
            ganhadores = len(view.participantes)

        vencedores_ids = random.sample(list(view.participantes), k=ganhadores)
        vencedores = [await self.bot.fetch_user(uid) for uid in vencedores_ids]
        mencoes = ", ".join(v.mention for v in vencedores)

        await ctx.reply(f"<:matteofeliz:1370103769081319514> | Parabéns {mencoes}, vocês ganharam **{premio}**!")

    @sorteio.error
    async def sorteio_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("<:matteobravo:1370104694852292681> | Uso incorreto!\nUse: `hsorteio tempo ganhadores prêmio`")
        else:
            raise error

# Adicionar a cog
async def setup(bot):
    await bot.add_cog(Sorteio(bot))