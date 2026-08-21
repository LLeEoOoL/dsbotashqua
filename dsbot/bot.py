import os



import discord
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()


TOKEN = os.getenv("TOKEN")
ROLE_IDS = {
    "games":1538923137595473971,
    "dota":1540477418026958868

}

intents = discord.Intents.default()

bot = discord.Client(intents=intents)

tree = app_commands.CommandTree(bot)

@bot.event
async def on_ready():
    await tree.sync()
    print(f"бот запущен как {bot.user}")

class RoleView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    async def toggle_role(
        self,
        interaction: discord.Interaction,
        role_id: int,
        role_name: str
    ):
        role = interaction.guild.get_role(role_id)
        if role is None:
            await interaction.response.send_message(
                f"❌ Роль **{role_name}** не найдена.",
                ephemeral=True
            )
            return
        member = interaction.user
        if role in member.roles:
            await member.remove_roles(role)
            await interaction.response.send_message(
                f"❌ Роль **{role_name}** снята.",
                ephemeral=True
            )
        else:
            await member.add_roles(role)
            await interaction.response.send_message(
                f"✅ Роль **{role_name}** выдана!",
                ephemeral=True
            )
    @discord.ui.button(
        label="Игровая",
        emoji="🎮",
        style=discord.ButtonStyle.primary,
        custom_id="games"
    )
    async def games_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        await self.toggle_role(
            interaction,
            ROLE_IDS["games"],
            "🎮 игровая"
        )

 




@tree.command(name="ping", description="check bot fr work")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("sosi")


@tree.command(name="roles", description="Панель выбора ролей")
async def roles(interaction: discord.Interaction):
    await interaction.response.send_message(
        """[❓] Здесь вы можете получить роль <@&1538923137595473971> для доступа в соответствующий раздел.
Для снятии роли нажмите повторно на кнопку.""",
        view=RoleView()
    )
bot.run(TOKEN)