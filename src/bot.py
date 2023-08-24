import os

import discord
from discord.ext import commands

import PokeRPS
import checks
import randomInt
import dotenv

from src import databaseSetup


def run_discord_bot(conn):
    intents = discord.Intents.default()
    intents.message_content = True

    client = commands.Bot(command_prefix="$", intents=intents)

    @client.event
    async def on_ready():
        print(f'{client} is now running')

    @client.command()
    async def PokeHelp(ctx):
        embed = discord.Embed(
            title="Help",
            color=discord.Color.green()
        )
        embed.add_field(name="Command List", value="$start \n $stats \n $roll \n $fwg @name")
        embed.add_field(name="Description", value="Start recording stats and having profile! \n View your stats \n" +
                                                  "Roll a 6 sided dice" +
                                                  "\n Play Fire Water Grass with someone")
        print("Posted Stats to discord!")
        await ctx.send(embed=embed)

    @client.command()
    async def start(ctx):
        await databaseSetup.insert_user(conn, ctx)

    @client.command()
    async def stats(ctx):
        users = databaseSetup.get_users(conn)
        user = users.fetchall()
        check_a = [(ctx.author.id,)]

        if check_a[0] not in user:
            await ctx.send("You needs to call $start")
            return

        result = databaseSetup.get_stats(conn, ctx.author.id)
        results = result.fetchall()

        if not results:
            embed = discord.Embed(
                title="Stats of @" + str(ctx.author.name),
                color=discord.Color.green()
            )
            embed.add_field(name="Games", value="FWG")
            embed.add_field(name="Wins", value=str(0))
            print("Posted Stats to discord!")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Stats of @" + str(ctx.author.name),
                color=discord.Color.green()
            )
            embed.add_field(name="Games", value="FWG")
            embed.add_field(name="Wins", value=str(results[0][0]))
            print("Posted Stats to discord!")
            await ctx.send(embed=embed)

    @client.command()
    async def roll(ctx):
        num = randomInt.rolling()
        await ctx.send("You rolled a " + str(num))

    @client.command()
    async def fwg(ctx, p1: discord.Member = None):
        if p1 is None:
            await ctx.send("You need to @ another person!")
            return
        else:
            users = databaseSetup.get_users(conn)
            user = users.fetchall()
            check_a = [(ctx.author.id,), (p1.id,)]

            if check_a[0] not in user or check_a[1] not in user:
                await ctx.send("You or the person you @ needs to call $start")
                return
            print(str(p1.id))
            player2 = str(p1.id)
            await ctx.send(" <@" + player2 + "> Do you want to play? \n (y) yes or (n) no")
            their_message = await client.wait_for("message", check=checks.checkYorN(p1))
            if their_message.content == 'y':
                await ctx.send("You are about to play PokeRPS with <@" + player2 + ">")
                await PokeRPS.run_rps(client, ctx, p1, conn)
            elif their_message.content == 'n':
                await ctx.send("<@" + player2 + "> does not want to play")
            else:
                await their_message.channel.send("Game canceled cause I don't understand what you typed")

    dotenv.load_dotenv()
    token = str(os.getenv("TOKEN"))
    client.run(token)
