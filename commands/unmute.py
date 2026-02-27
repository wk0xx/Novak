from discord.ext import commands
import discord

class UnmuteCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.reply("<:Offline:1476766855174819963> | Uso incorreto! Você deve mencionar um membro para desmutá-lo.")
            return
        
        mute_role = discord.utils.get(ctx.guild.roles, name="Mutado")
        if mute_role in member.roles:
            await member.remove_roles(mute_role)
            await ctx.reply(f"<:Offline:1476766855174819963> | {member.mention} foi desmutado com sucesso!")
        else:
            await ctx.reply("<:Offline:1476766855174819963> | Este membro não está mutado!")

async def setup(bot):
    await bot.add_cog(UnmuteCommand(bot))