import os
import threading
import discord
from discord.ext import commands
from flask import Flask

# إعداد موقع الـ Web (Flask) عشان Render ما يقفل السيرفر
app = Flask(__name__)

@app.route('/')
def home():
    return "البوت والموقع يعملان بنجاح! 🚀"

def run_web():
    # تشغيل الموقع على البورت المطلوب للاستضافة
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# إعداد بوت ديسكورد
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"تم تسجيل الدخول بنجاح باسم: {bot.user}")

# تشغيل الموقع في خلفية البوت
if __name__ == "__main__":
    t = threading.Thread(target=run_web)
    t.start()
    
    # تشغيل البوت باستخدام التوكن اللي حطيناه في إعدادات المنصة
    TOKEN = os.environ.get("DISCORD_TOKEN")
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("خطأ: لم يتم العثور على توكن البوت في المتغيرات البيئية!")