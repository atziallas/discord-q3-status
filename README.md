# discord-q3-status
Show player count from your Quake 3 based server on a discord channel on your guild.

<p align="center">
    <img src="https://img.shields.io/github/license/verdienste/discord-q3-status">
</p>

## 📋 Installation
This script needs Python 3 to run.
Only dependency is discord.py so you only need to run:<br>
<br>
```pip install discord.py```

## ⚙ Configuration
Enter your specifics in config.py:<br>
- SERVER_IP: Your Q3 based server IP<br>
- SERVER_PORT: The port your server listens to<br>
- BOT_ID: The discord bot ID that u will add to your guild<br>
- DISCORD_COUNT_CHANNEL: The Id of the discord voice channel that it's name will be changed to show the player count <br>
- COUNT_UPDATE_INTERVAL: The interval on which the bot will update the channel in seconds<br>
(right now discord allows voice channel name change every 5 minutes, so 300 is the minimum possible value for now)

## 🚀 How to run
Just run the stats.py script: <br><br>
```python stats.py``` <br>&nbsp;or<br> ```python3 stats.py```<br><br>
Script logs events to file ```player_count.log```


