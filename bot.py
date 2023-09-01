import discord
from discord import app_commands
import secret_token
import com_cot_image
import asyncio

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

short_version_text="Made by LunastroD, Aug 2023"
version_text=short_version_text+", for the Excelsior discord server and the awesome Cosmoteer community :3\n    -Check out the source code at https://github.com/lunastrod/cosmoteer-com"
help_text="""
/com: Calculates the center of mass of a cosmoteer ship.png
    -the center of mass of your ship will be drawn as a green circle
    -this tool is only a good aproximation of the com, total mass might be a bit off too
/version: """+version_text+"""
/help: Shows this message
"""

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="Cosmoteer (/help)"))
    print("Syncing slash commands")
    await tree.sync()
    print("Guilds:")
    for guild in client.guilds:
        print("\t- " + guild.name, guild.id)
    print("Bot is ready")

@tree.command(name="com", description="Calculates the center of mass of a cosmoteer ship.png")
async def com(interaction: discord.Interaction, ship: discord.Attachment):
    print("defer")
    await interaction.response.defer()
    print("deferred, saving")
    await ship.save('discord_bot\ship.ship.png')
    print("saved, calculating")
    try:
        data=com_cot_image.com_cot_image("discord_bot\ship.ship.png", "discord_bot\out.png")#calculate the center of mass
    except:
        await interaction.followup.send("Error: could not process ship")
        return
    print("calculated, sending")
    with open('discord_bot\out.png', 'rb') as f, open("discord_bot\ship.ship.png", "rb") as s:#send the output image
        picture = discord.File(f)
        ship = discord.File(s)
        files_to_send: list[discord.File] = [ship,picture]
        text="Center of mass: " + str(round(data[0],2)) + ", " + str(round(data[1],2)) + "\nTotal mass: " + str(round(data[2],2)) + "t"
        
        await asyncio.sleep(3)
        await interaction.followup.send(text,files=files_to_send)

@tree.command(name="version", description=short_version_text)
async def version(interaction: discord.Interaction):
    await interaction.response.send_message(version_text)

@tree.command(name="help", description="shows the list of commands")
async def help(interaction: discord.Interaction):
    await interaction.response.send_message(help_text)

client.run(secret_token.token)