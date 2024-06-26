import discord
from discord.ext import commands, tasks
import asyncio
import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect("bot_python.db")
c = conn.cursor()

alarms = {}
# Intents
intents = discord.Intents.default()
intents.typing = False
intents.dm_messages = True  # Enable DM messages intent
intents.presences = False

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    await bot.wait_until_ready()
    
    

@bot.event
async def on_message(message): 
    text = message.content.split(' ')
    cal_calculate  = [
         'วันนี้กิน' , 'cal' , 'วันนี้ซื้อ' , 'จ่าย'
         ]
    cal_showdata_day = [
        'รายงาน' , 'report' , 'แสดงรายการวันนี้'
    ] 
    cal_showdata_all = [
         'รายงานทั้งหมด' , 'all_report' , 'แสดงรายการทั้งหมด'
    ]
    ##print(text in cal_calculate  , text[0] , '==' , cal_calculate)
    if(datetime.now().strftime("%H:%M:%S")  == "14:38:00"):
        await message.channel.send("hi")

    if (text[0] in cal_calculate) and message.author != bot.user:


        c.execute("INSERT INTO menu_cal (user_id, date, menu, timestamp, price) VALUES (?, ?, ?,  ? , ?)", 
                      (message.author.id, datetime.now().strftime("%Y-%m-%d"),text[1], datetime.now().strftime("%H:%M:%S"), text[2]))
        conn.commit()

        await message.channel.send(select_all())
    
    if(text[0] in cal_showdata_day): 
         await message.channel.send(report_day())
    if(text[0] in cal_showdata_all): 
         await message.channel.send(report_all())
         
    await bot.process_commands(message)  



def select_all():
    date =  datetime.now().strftime("%Y-%m-%d")
    print(date)
    c.execute(f"SELECT * FROM menu_cal" )
    rows = c.fetchall()
    if rows:
           response = "\n".join([f"{row[2]}  :  {row[3]}  :  {row[4]} : {row[5]}" for row in rows])
    return response



def report_day():
#"SELECT date , sum(price) FROM menu_cal group by "
     date = datetime.now().strftime("%Y-%m-%d")
     print("SELECT sum(price) FROM menu_cal group by date having date = ?", (date,))
     c.execute("SELECT date, menu, price FROM menu_cal WHERE date = ?", (date,))
     rows = c.fetchall()
     c.execute("SELECT sum(price) FROM menu_cal group by date having date = ?", (date,))
     sum = c.fetchall()
    
     if rows:
           response = "\n".join([f"วันที่ {row[0]} :{row[1]}: {row[2]} Bath" for row in rows])
           return f"{response} \n Total :: {sum[0] } Bath  "

def report_all():
   
     c.execute("SELECT date,sum(price) FROM menu_cal group by date ") 
     rows = c.fetchall()
     if rows:
           response = "\n".join([f"วันที่ {row[0]} : {row[1]} Bath" for row in rows])
           return response
     



@tasks.loop(seconds = 5)  
async def check_notifications():
     print("Hi")


@check_notifications.before_loop
async def before_check_notifications():
    # Ensure bot is fully ready before starting the loop
    await bot.wait_until_ready()
    check_notifications.start()

bot.run('ODAzMjg2NDQ0NjAwODUyNTIw.GAlRs9.49kLPVdypliC592ELfiq_gIAyeSnBz2VV_jUAo')
