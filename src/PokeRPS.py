import discord
from discord.ui import View

import checks
from src import databaseSetup


class MyView(View):

    def __init__(self, ctx, p1):
        super().__init__(timeout=30)
        self.op = None
        self.us = None
        self.ctx = ctx
        self.player1 = p1

    @discord.ui.button(label="Fire", style=discord.ButtonStyle.red, emoji="🔥")
    async def fire_button_callback(self, button, interaction):
        print("Pressed Fire Button")
        if interaction.user == self.player1:
            self.op = "Fire"
            await interaction.response.send_message("<@" + str(interaction.user.id) + "> selected an option")
        elif interaction.user == self.ctx.author:
            self.us = "Fire"
            await interaction.response.send_message("<@" + str(interaction.user.id) + "> selected an option")

    @discord.ui.button(label="Water", style=discord.ButtonStyle.primary, emoji="💧")
    async def water_button_callback(self, button, interaction):
        print("Pressed Water Button")
        if interaction.user == self.player1:
            self.op = "Water"
            await interaction.response.send_message("<@" + str(interaction.user.id) + "> selected an option")
        elif interaction.user == self.ctx.author:
            self.us = "Water"
            await interaction.response.send_message("<@" + str(interaction.user.id) + "> selected an option")

    @discord.ui.button(label="Grass", style=discord.ButtonStyle.green, emoji="🌿")
    async def grass_button_callback(self, button, interaction):
        print("Pressed Grass Button")
        if interaction.user == self.player1:
            self.op = "Grass"
            await interaction.response.send_message("<@" + str(interaction.user.id) + "> selected an option")
        elif interaction.user == self.ctx.author:
            self.us = "Grass"
            await interaction.response.send_message("<@" + str(interaction.user.id) + "> selected an option")

    async def on_timeout(self) -> None:
        self.disable_all_items()
        try:
            await self.message.edit(content="You took too long! None of the buttons work now!")
            await self.message.delete()
        except Exception as e:
            print(e)


async def run_rps(client, ctx, p1, conn):
    done = True

    print("Before Loop")
    while done:
        print("Loop Menu")
        view = MyView(ctx, p1)
        mes_view = await ctx.send("Play PokeRPS with me!", view=view)

        mes = await client.wait_for("message", check=checks.check_a(p1, ctx.author))
        await client.wait_for("message", check=checks.check_a2(p1, ctx.author, mes))

        await mes_view.delete()

        if view.op == "Fire" and view.us == "Fire":
            await ctx.send("Tie play again!")
        elif view.op == "Fire" and view.us == "Water":
            await ctx.send("Water beats Fire so <@" + str(ctx.author.id) + "> won!")
            await databaseSetup.insert_FWG(conn, ctx.author.id)
            done = False
        elif view.op == "Fire" and view.us == "Grass":
            await ctx.send("Fire beats Grass so <@" + str(p1.id) + "> won!")
            await databaseSetup.insert_FWG(conn, p1.id)
            done = False
        elif view.op == "Water" and view.us == "Fire":
            await ctx.send("Water beats Fire so <@" + str(p1.id) + "> won!")
            await databaseSetup.insert_FWG(conn, p1.id)
            done = False
        elif view.op == "Water" and view.us == "Water":
            await ctx.send("Tie play again!")
        elif view.op == "Water" and view.us == "Grass":
            await ctx.send("Grass beats Water so <@" + str(ctx.author.id) + "> won!")
            await databaseSetup.insert_FWG(conn, ctx.author.id)
            done = False
        elif view.op == "Grass" and view.us == "Fire":
            await ctx.send("Fire beats Grass so <@" + str(ctx.author.id) + "> won!")
            await databaseSetup.insert_FWG(conn, ctx.author.id)
            done = False
        elif view.op == "Grass" and view.us == "Water":
            await ctx.send("Grass beats Water so <@" + str(p1.id) + "> won!")
            await databaseSetup.insert_FWG(conn, p1.id)
            done = False
        elif view.op == "Grass" and view.us == "Grass":
            await ctx.send("Tie play again!")
