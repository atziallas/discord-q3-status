from dataclasses import dataclass
from loggers import main_logger
import socket
import config
import functools
import asyncio

css_mapping = {
    '^0': 'black',
    '^1': 'red',
    '^2': 'green',
    '^3': 'yellow',
    '^4': 'blue',
    '^5': 'cyan',
    '^6': 'purple',
    '^7': 'white',
    '^8': 'orange',
    '^9': 'grey',
}

@dataclass
class Player:
    html_name: str
    ping: int


def socket_receive(sock):
    return sock.recv(8192)


async def send_q3_command(command):
    main_logger.info(f"Querying Q3 server: {command}")
    sock = None
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect((config.SERVER_IP, config.SERVER_PORT))
        sock.send(b'\xff\xff\xff\xff%b' % command.encode())
        sock.settimeout(5)
        loop = asyncio.get_event_loop()
        res = await loop.run_in_executor(None, functools.partial(socket_receive, sock=sock))
        sock.close()
        response = res.decode("cp1252")
    except socket.error as exception:
        main_logger.error(
            "Error while opening socket to server %s" % exception)
        return None
        
    main_logger.info("Q3 server response received:")
    main_logger.info(response)
    return response


async def edit_discord_channel(channel, new_name):
    try:
        await channel.edit(name=new_name)
        main_logger.info("Discord api call succesful")
    except Exception as e:
        main_logger.info("Exception on channel edit")
        main_logger.info(e)
