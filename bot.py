import os

import discord
from discord.ext import commands

import PokeRPS
import checks
import randomInt
import responses
import dotenv


async def send_message(message, user_message, is_private):
    try:
        response = await responses.handle_response(message, user_message)
        if isinstance(response, str):
            await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)


def run_discord_bot():
    intents = discord.Intents.default()
    intents.message_content = True

    client = commands.Bot(command_prefix="$", intents=intents)

    @client.event
    async def on_ready():
        print(f'{client} is now running')

    @client.command()
    async def roll(ctx):
        num = randomInt.rolling()
        await ctx.send("You rolled a " + str(num))

    @client.command()
    async def fwg(ctx, p1: discord.Member=None):
        if p1 is None:
            await ctx.send("You need to @ another person!")
            return
        else:
            print(str(p1.id))
            player2 = str(p1.id)
            await ctx.send(" <@" + player2 + "> Do you want to play? \n (y) yes or (n) no")
            their_message = await client.wait_for("message", check=checks.checkYorN(p1))
            if their_message.content == 'y':
                await ctx.send("You are about to play PokeRPS with <@" + player2 + ">")
                await PokeRPS.run_rps(client, ctx, p1)
            elif their_message.content == 'n':
                await ctx.send("<@" + player2 + "> does not want to play")
            else:
                await their_message.channel.send("Game canceled cause I don't understand what you typed")

    dotenv.load_dotenv()
    token = str(os.getenv("TOKEN"))
    client.run(token)