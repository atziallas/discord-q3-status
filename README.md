# discord-q3-status
Show player count from your Quake 3 based server through changing the name of a Discord channel on your guild.

<img src="https://img.shields.io/github/license/verdienste/discord-q3-status">

## 📋 Installation
This script needs Python 3 to run.
Only dependency is discord.py so you only need to run:<br>
<br>
```pip install discord.py```

## ⚙ Configuration
You'll need to create a bot and add it to your guild for the script to use.<br>
The bot just needs the manage "Manage Channels" permissions to work.

Also you'll need to create a channel for the script to rename with the status.<br>
People usually prefer using a voice channel as you don't have character limitations (you can use forward slash).

Then enter your specifics in config.py:
- SERVER_IP: Your Q3 based server IP
- SERVER_PORT: The port your server listens to
- BOT_ID: The Discord bot id that you created for this
- DISCORD_COUNT_CHANNEL: The id of the Discord voice channel that it's name will be changed to show the player count
- COUNT_UPDATE_INTERVAL: The interval on which the bot will update the channel in seconds<br>
(right now Discord allows voice channel name change every 5 minutes, so 300 is the minimum possible value for now)

## 🚀 How to run
Just run the stats.py script: <br><br>
```python stats.py``` <br>&nbsp;or<br> ```python3 stats.py```<br><br>
Script logs events to file ```player_count.log```


