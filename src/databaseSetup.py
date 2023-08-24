import sqlite3


def run_database():
    conn = sqlite3.connect('PokeBase.db')

    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 id Int NOT NULL,
                 Primary Key(id))''')

    c.execute('''CREATE TABLE IF NOT EXISTS FWGgames(
                 id Integer Primary Key AUTOINCREMENT NOT NULL,
                 winner Integer NOT NULL,
                 Foreign Key (winner) REFERENCES users (id))''')

    conn.commit()
    return conn


async def insert_user(conn, ctx):
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users VALUES (?)', (ctx.author.id,))
        conn.commit()
        await ctx.send("You are all set!")
    except Exception as e:
        await ctx.send("You already have a profile!")


async def insert_FWG(conn, aid):
    c = conn.cursor()
    try:
        c.execute('INSERT INTO FWGgames(winner) VALUES (?)', (aid,))
        conn.commit()
    except Exception as e:
        print("Not Inserted")


def get_stats(conn, aid):
    c = conn.cursor()
    result = c.execute(f'SELECT count(*) From FWGgames Where FWGgames.winner = {aid} Group By FWGgames.winner')
    return result


def get_users(conn):
    c = conn.cursor()
    result = c.execute('SELECT * FROM users')
    return result
