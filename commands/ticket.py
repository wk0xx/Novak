import discord
from discord.ext import commands
from discord.ui import View, Select
import io

TICKET_CHANNEL_ID = 1476740114309710006
LOG_CHANNEL_ID    = 1476740201471545488
PING_ROLE_ID      = 1476739826995826841


def file_from_text(content: str) -> discord.File:
    buffer = io.BytesIO(content.encode())
    return discord.File(buffer, filename="ticket_log.txt")


class TicketMenu(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Inscrição", value="Inscrição"),
            discord.SelectOption(label="Dúvida", value="Dúvida"),
        ]
        super().init(
            placeholder="Selecione uma opção",
            options=options,
            min_values=1,
            max_values=1,
            custom_id="ticket_menu"
        )

    async def callback(self, interaction: discord.Interaction):
        tipo = self.values[0]
        member = interaction.user
        guild = interaction.guild
        chan = guild.get_channel(TICKET_CHANNEL_ID)

        thread_name = f"{tipo}-{member.name}"

        # VERIFICA THREADS ABERTAS (PERSISTENTES)
        threads = [t async for t in chan.threads() if not t.archived]
        if any(t.name == thread_name for t in threads):
            return await interaction.response.send_message(
                "Você já possui um ticket aberto.",
                ephemeral=True
            )

        thread = await chan.create_thread(
            name=thread_name,
            type=discord.ChannelType.private_thread,
            invitable=False
        )
        await thread.add_user(member)

        embed = discord.Embed(
            title=f"Ticket do tipo {tipo} Criado!",
            description=f"{member.mention}, seu ticket foi criado.\nClique abaixo para fechar quando terminar.",
            color=discord.Color.blue()
        )

        await thread.send(f"<@&{PING_ROLE_ID}>")
        await thread.send(embed=embed, view=CloseTicketView())

        await interaction.response.send_message(
            ":Discord: | Thread criada com sucesso!",
            ephemeral=True
        )


class TicketMenuView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketMenu())


class CloseTicketView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Fechar Thread",
        style=discord.ButtonStyle.red,
        custom_id="close_ticket"
    )
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        thread = interaction.channel

        msgs = []
        async for msg in thread.history(limit=None, oldest_first=True):
            ts = msg.created_at.strftime("%Y-%m-%d %H:%M")
            msgs.append(f"[{ts}] {msg.author}: {msg.content}")

        content = "\n".join(msgs) or "Sem mensagens registradas."
        file = file_from_text(content)

        log_chan = interaction.guild.get_channel(LOG_CHANNEL_ID)

        embed = discord.Embed(
            title="Ticket Fechado",
            color=discord.Color.red(),
            timestamp=discord.utils.utcnow()
        )

        embed.add_field(name="Thread", value=thread.mention, inline=False)
        embed.add_field(name="Fechado por", value=interaction.user.mention, inline=True)

        if log_chan:
            await log_chan.send(embed=embed, file=file)

        await thread.send("Thread fechado com sucesso.")
        await thread.edit(archived=True, locked=True)

class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # REGISTRA VIEWS PERSISTENTES
        bot.add_view(TicketMenuView())
        bot.add_view(CloseTicketView())

    @commands.command(name="ticketsadmin7")
    async def ticketsadmin(self, ctx):
        embed = discord.Embed(
            title="📩 Menu Suporte",
            description="Selecione a categoria abaixo para abrir um ticket:",
            color=discord.Color.blue()
        )

        embed.add_field(
            name="Inscrição",
            value="Inscrição para família",
            inline=False
        )

        embed.add_field(
            name="Dúvida",
            value="Abrir ticket para tirar dúvidas gerais.",
            inline=False
        )

        await ctx.send(embed=embed, view=TicketMenuView())  # opcional se quiser reenviar o painel


async def setup(bot):
    await bot.add_cog(Ticket(bot))
