import requests
import sqlite3
import datetime
import time
import telebot

key = "a30adaec-5ada-45dd-8227-cdb51f8a7dd3"
token = "1680890597:AAFpbqTWltFpkTX-RJlKRUX_oyvdkpbPGm4"

bot = telebot.TeleBot(token)
res = requests.get("https://api.emcd.io/v1/eth/workers/" + key)
data = res.json()

conn = sqlite3.connect("stats.db")
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS stats(
    time TEXT,
    fl INT,
    mr INT);
""")
conn.commit()

while True:
    res = requests.get("https://api.emcd.io/v1/eth/workers/" + key)
    data = res.json()
    for i in range(len(data["details"])):
        if data["details"][i]["worker"] == "flamer":
            fl = data["details"][i]["hashrate24h"] // 1000000
        elif data["details"][i]["worker"] == "MemoryFr":
            mr = data["details"][i]["hashrate24h"] // 1000000
    now = datetime.datetime.now().strftime("%m-%d %H:%M")
    stat = (now, fl, mr)
    bot.send_message(410124654, now + "\nflamer: " + str(fl) + " MH/s" + "\nMemoryFr: " + str(mr) + " MH/s")
    cur.execute("INSERT INTO stats VALUES(?, ?, ?);", stat)
    conn.commit()
    time.sleep(86400)