import os
import threading
import discord
from discord.ext import commands
from flask import Flask, render_template_string

# إعداد تطبيق Flask
app = Flask(__name__)

# تصميم واجهة الموقع الاحترافية (HTML & CSS)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>لوحة تحكم بوت ديسكورد</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Cairo', sans-serif;
        }
        body {
            background-color: #0f172a;
            color: #f8fafc;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .container {
            width: 100%;
            max-width: 800px;
            background: #1e293b;
            border-radius: 16px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
            overflow: hidden;
            border: 1px solid #334155;
        }
        .header {
            background: linear-gradient(135deg, #6366f1, #4f46e5);
            padding: 30px;
            text-align: center;
        }
        .header h1 {
            font-size: 26px;
            margin-bottom: 5px;
            color: #ffffff;
        }
        .header p {
            font-size: 14px;
            color: #e0e7ff;
        }
        .content {
            padding: 30px;
        }
        .status-card {
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: #0f172a;
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 20px;
            border: 1px solid #334155;
        }
        .status-info {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .dot {
            width: 12px;
            height: 12px;
            background-color: #22c55e;
            border-radius: 50%;
            box-shadow: 0 0 10px #22c55e;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { transform: scale(0.95); opacity: 0.8; }
            50% { transform: scale(1.1); opacity: 1; }
            100% { transform: scale(0.95); opacity: 0.8; }
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 25px;
        }
        .stat-box {
            background: #0f172a;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            border: 1px solid #334155;
        }
        .stat-box h3 {
            font-size: 22px;
            color: #6366f1;
            margin-bottom: 5px;
        }
        .stat-box span {
            font-size: 13px;
            color: #94a3b8;
        }
        .btn-group {
            display: flex;
            gap: 10px;
            justify-content: center;
        }
        .btn {
            background-color: #6366f1;
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.3s;
            text-decoration: none;
            font-size: 14px;
        }
        .btn:hover {
            background-color: #4f46e5;
        }
        .footer {
            text-align: center;
            padding: 15px;
            font-size: 12px;
            color: #64748b;
            background: #0f172a;
            border-top: 1px solid #334155;
        }
    </style>
</head>
<body>

    <div class="container">
        <div class="header">
            <h1>لوحة التحكم الرئيسية</h1>
            <p>إدارة ومتابعة بوت ديسكورد بكل سهولة</p>
        </div>
        
        <div class="content">
            <!-- حالة البوت -->
            <div class="status-card">
                <div class="status-info">
                    <div class="dot"></div>
                    <div>
                        <h4 style="font-size: 16px;">حالة البوت</h4>
                        <span style="font-size: 13px; color: #94a3b8;">متصل ويعمل بكفاءة عالية</span>
                    </div>
                </div>
                <span style="background: rgba(34, 197, 94, 0.1); color: #22c55e; padding: 6px 12px; border-radius: 20px; font-size: 12px; font-weight: 600;">أونلاين</span>
            </div>

            <!-- الإحصائيات -->
            <div class="stats-grid">
                <div class="stat-box">
                    <h3>{{ guilds_count }}</h3>
                    <span>السيرفرات المفعل بها</span>
                </div>
                <div class="stat-box">
                    <h3>نشط</h3>
                    <span>حالة الويب سيرفر</span>
                </div>
            </div>

            <!-- الأزرار -->
            <div class="btn-group">
                <a href="#" class="btn" onclick="alert('قريباً سيتم تفعيل الأوامر المخصصة!')">إعدادات البوت</a>
                <a href="https://discord.com" target="_blank" class="btn" style="background-color: #334155;">دعم ديسكورد</a>
            </div>
        </div>

        <div class="footer">
            تم التطوير والاستضافة مجاناً عبر Render 🚀
        </div>
    </div>

</body>
</html>
"""

@app.route('/')
def home():
    # جلب عدد السيرفرات المتصل بها البوت لعرضها في الموقع
    guilds_count = len(bot.guilds) if bot.is_ready() else 0
    return render_template_string(HTML_TEMPLATE, guilds_count=guilds_count)

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# إعداد بوت ديسكورد
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"تم تسجيل الدخول بنجاح باسم: {bot.user}")

# التشغيل المتزامن
if __name__ == "__main__":
    t = threading.Thread(target=run_web)
    t.start()
    
    TOKEN = os.environ.get("DISCORD_TOKEN")
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("خطأ: لم يتم العثور على توكن البوت في المتغيرات البيئية!")
        
