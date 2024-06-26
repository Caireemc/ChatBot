
import sqlite3
conn = sqlite3.connect("bot_python.db")

c = conn.cursor()

c.execute("DELETE FROM menu_cal")

conn.commit()
