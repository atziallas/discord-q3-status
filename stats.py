import asyncio
import functools
import logging
import re
import socket
from logging import StreamHandler
from logging.handlers import RotatingFileHandler

import discord

import config

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
stream_handler = StreamHandler()
stream_handler.setFormatter(formatter)

logger_count = logging.getLogger('player_count')
logger_count.setLevel(logging.INFO)
count_handler = RotatingFileHandler('player_count.log', maxBytes=2000000, backupCount=5)
count_handler.setFormatter(formatter)
logger_count.addHandler(count_handler)
logger_count.addHandler(stream_handler)

logger_list = logging.getLogger('player_list')
logger_list.setLevel(logging.INFO)
list_handler = RotatingFileHandler('player_list.log', maxBytes=2000000, backupCount=5)
list_handler.setFormatter(formatter)
logger_list.addHandler(count_handler)
logger_list.addHandler(stream_handler)


def socket_receive(sock):
    return sock.recv(8192)


async def edit_channel(channel, new_name):
    try:
        await channel.edit(name=new_name)
        logger_count.info("Discord api call succesful")
    except Exception as e:
        logger_count.info("Exception on channel edit")
        logger_count.info(e)


async def update_player_count():
    edit_task = None
    while True:
        logger_count.info("================== START UPDATE ===================")
        response = await send_command("getinfo")
        try:
            players_count = re.match(r'.*?g_humanplayers\\(\d*?)\\.*', response, re.DOTALL).groups()[0]
            logger_count.info("Getting discord channel")
            channel = client.get_channel(config.DISCORD_COUNT_CHANNEL)
            new_name = 'Players: ' + players_count + '/32'
            if edit_task:
                if not edit_task.done():
                    logger_count.info("Cancelling previous discord API task")
                    edit_task.cancel()
            logger_count.info("Changing discord channel name")
            edit_task = asyncio.ensure_future(edit_channel(channel, new_name))
            logger_count.info("Channel name change sent to discord api with name: " + new_name)
            logger_count.info("======= SLEEP FOR %s seconds =======" % config.COUNT_UPDATE_INTERVAL)
            await asyncio.sleep(config.COUNT_UPDATE_INTERVAL)
        except Exception as e:
            logger_count.error(e)


async def send_command(command):
    logger_count.info("Querying Q3 server")
    sock = None
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error as exception:
        logger_count.error("error while opening socket to server %s" % exception)
    sock.connect((config.SERVER_IP, config.SERVER_PORT))
    sock.send(b'\xff\xff\xff\xff%b' % command.encode())
    sock.settimeout(5)
    loop = asyncio.get_event_loop()
    res = await loop.run_in_executor(None, functools.partial(socket_receive, sock=sock))
    sock.close()
    response = res.decode("cp1252")
    logger_count.info("Q3 server response received:")
    logger_count.info(response)
    return response


# async def update_player_names():
# coming soon


class Q3DiscordClient(discord.Client):
    async def on_ready(self):
        logger_count.info("Daemon started")
        task = client.loop.create_task(update_player_count())
        # task = client.loop.create_task(update_player_names())


client = Q3DiscordClient()
client.run(config.BOT_ID)
