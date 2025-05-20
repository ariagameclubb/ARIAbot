from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import random

players = ["علی", "خشی", "نگین", "هانیه", "سامی", "فرزاد", "مرجان", "روژین", "آریا"]
current_index = 0

questions = {
    "تصمیم‌گیری سخت": [
        "اگه قرار باشه یکی از اعضای گروه رو انتخاب کنی که فقط اون زنده بمونه، کیو انتخاب می‌کنی؟",
        "اگه فقط یک نفر بتونه حافظه‌شو نگه داره و بقیه همه‌چی رو فراموش کنن، کیو انتخاب می‌کنی؟"
    ],
    "همه علیه تو": [
        "اگه بفهمی همه پشت سرت حرفی زدن جز یک نفر، حدس می‌زنی اون کیه؟"
    ],
    "قفل‌شده (شدید)": [
        "تنها راه نجات گروه اینه که با یکی از افراد رابطه برقرار کنی، انتخابت؟"
    ]
}

asked = {player: set() for player in players}

def get_question(player):
    for _ in range(50):
        cat = random.choice(list(questions.keys()))
        q = random.choice(questions[cat])
        key = f"{cat}|{q}"
        if key not in asked[player]:
            asked[player].add(key)
            locked = "قفل" in cat
            return f"[سوال {'قفل‌شده' if locked else cat}]\n{q}"
    return "همه سوال‌ها برای این بازیکن تموم شده!"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("بازی شروع شد! برای دیدن سوال، /next رو بفرست.")

async def next(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_index
    player = players[current_index]
    q = get_question(player)
    await update.message.reply_text(f"نوبت: {player}\n{q}")

async def skip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_index
    current_index = (current_index + 1) % len(players)
    player = players[current_index]
    await update.message.reply_text(f"نوبت رد شد! حالا نوبت: {player}\n/next برای سوال")

app = ApplicationBuilder().token("7896922744:AAGfnL1K0PJLZMwgPdEYHMOPu5pyNrS9Hns").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("next", next))
app.add_handler(CommandHandler("skip", skip))

app.run_polling()