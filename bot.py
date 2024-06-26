import asyncio
import re
import discord
import config
import imgkit
from io import BytesIO
from dataclasses import dataclass
from discord import app_commands
from discord.ext import commands
from loggers import main_logger
from utils import Player, css_mapping, edit_discord_channel, send_q3_command
from jinja2 import Template


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)
cached_image = None

class Q3DiscordClient(discord.Client):
    async def on_ready(self):
        # await tree.sync(guild=discord.Object(id=config.DISCORD_SERVER_ID))
        await tree.sync()
        main_logger.info("Command Tree synced!")
        if config.ENABLE_COUNT_CHANNEL:
            main_logger.info("Players Daemon started")
            task = client.loop.create_task(update_player_count())


client = Q3DiscordClient(intents=intents)
tree = app_commands.CommandTree(client)

async def update_player_count():
    edit_task = None
    while True:
        main_logger.info(
            "================== START UPDATE ===================")
        response = await send_q3_command("getinfo")
        try:
            players_count = re.match(
                r'.*?g_humanplayers\\(\d*?)\\.*', response, re.DOTALL).groups()[0]
            max_players = re.match(
                r'.*?sv_maxclients\\(\d*?)\\.*', response, re.DOTALL).groups()[0]
            main_logger.info("Getting discord channel")
            channel = client.get_channel(config.DISCORD_COUNT_CHANNEL_ID)
            new_name = f'Players: {players_count}/{max_players}'
            if edit_task:
                if not edit_task.done():
                    main_logger.info("Cancelling previous discord API task")
                    edit_task.cancel()
            main_logger.info("Changing discord channel name")
            edit_task = asyncio.ensure_future(
                edit_discord_channel(channel, new_name))
            main_logger.info(
                "Channel name change sent to discord api with name: " + new_name)
            main_logger.info(
                "============== SLEEP FOR %s seconds ==============" % config.COUNT_UPDATE_INTERVAL)
            await asyncio.sleep(config.COUNT_UPDATE_INTERVAL)
        except Exception as e:
            main_logger.error(e)


@tree.command(
    name="players",
    description="Show players list from server",
    # guild=discord.Object(id=config.DISCORD_SERVER_ID)
)
@app_commands.checks.cooldown(1, 7.0, key=lambda i: (i.guild_id, i.user.id))
async def players_list(interaction: discord.Interaction):
    await interaction.response.defer()
    try:
        server_response = await send_q3_command("getstatus")
        if not server_response:
            cached_image_or_error(interaction=interaction)
            return
        players_text = re.match(r'.*statusResponse\n.*?\n(.*)',
                                server_response, re.DOTALL).groups()[0]
        # split players_text by new line and loop on the pieces
        players_info = players_text.split("\n")
        del players_info[-1]
        players = []
        if len(players_info) == 0:
            await interaction.followup.send("No players on the server 🙁")
            return
        for player_info in players_info:
            matches = re.match(r'-?\d* (\d*) "(.*)"', player_info, re.DOTALL)
            groups = matches.groups()

            ping = groups[0]
            q3_player_name = groups[1]

            html_player_name = convert_to_html(q3_player_name)
            player = Player(html_name=html_player_name, ping=ping)
            players.append(player)
        img = create_players_img(players)
    except Exception as e:
        main_logger.error(e)
        await cached_image_or_error(interaction)
    await interaction.followup.send("Players list", file=discord.File(fp=BytesIO(img), filename="players_list.png"))

async def cached_image_or_error(interaction):
    if cached_image:
        await interaction.followup.send("Players list", file=discord.File(fp=BytesIO(cached_image), filename="players_list.jpg"))
    else: 
        await interaction.followup.send("Server non-responsive. Please try again 🙂")

def convert_to_html(q3_player_name: str):
    # split on the color character, for example: ^1
    name_chunks = re.split(r'(\^\d)', q3_player_name)
    if len(name_chunks) == 1:
        html = f"<span class='white'>{q3_player_name}</span>"
    else:
        html = ""
        previous_html = ""
        for chunk in name_chunks:
            if re.match(r'\^\d', chunk):
                html += f"<span class='{css_mapping[chunk]}'>"
            else:
                if "<span" not in previous_html:
                    html += f"<span class='white'>{chunk}</span>"
                else:
                    html += f"{chunk}</span>"
            previous_html = html
    return html

def create_players_img(players: list[Player]):
    with open("templates/players_list.html") as f:
        options = {
            'format': 'jpg',
            'zoom': 2,
            'width': '600',
            'quality': '98',
        }
        template = Template(f.read())
        rendered_template = template.render(players=players)
        # save rendered_template to a file
        img = imgkit.from_string(rendered_template, False, options=options)
        cached_image = img
        return img

client.run(config.BOT_TOKEN)
