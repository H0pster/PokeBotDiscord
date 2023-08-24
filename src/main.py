import bot
from src import databaseSetup

if __name__ == '__main__':
    conn = databaseSetup.run_database()
    bot.run_discord_bot(conn)
