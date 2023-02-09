# BOTC Token Bag

BOTC Token Bag is a Discord Bot designed to help you play Blood on the Clocktower in-person when you don't own the game.

It's intended to be used in combination with [the online app](https://clocktower.online/).

## Running the Bot

1. Create an app for the bot [here](https://discord.com/developers/applications). The bot requires no permissions, as all it does is use slash commands and DM users.
2. Create a server for managing the bot.
3. Copy `env.example.py` into `env.py` and set the TOKEN variable to your bot token, and the GUILD variable to the id of the server you want to use commands in.
4. Run the bot with `python3 app.py`.

## Using the Bot

First, add the names of the players and their discord accounts using `/addname`. You can get a list of names using `/getnames`. These are permanently saved to `players.yaml`, so you only have to do it once for each new player.

Next, you can send roles by doing `/sendroles`. For example, `/sendroles players:tom dick harry roles:imp poisoner mayor`.

(Note: In order to send the messages, the bot needs to be in at least one server as each of the users)

Alternatively, you can use `/sendgrim` to send out characters.
