import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

def main_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📚 Профессии", callback_data="prof")],
        [InlineKeyboardButton("🏫 Как поступить", callback_data="enter")],
        [InlineKeyboardButton("🏠 Общежитие", callback_data="hostel")],
        [InlineKeyboardButton("⭐ Староста", callback_data="starosta")],
        [InlineKeyboardButton("👨‍🏫 Преподаватели", callback_data="prepod")]
    ])

def back_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Назад в меню", callback_data="menu")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! 👋\nЯ БелПедГид — бот колледжа.\nВыбери раздел:",
        reply_markup=main_keyboard()
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "menu":
        await query.edit_message_text(
            "Главное меню:",
            reply_markup=main_keyboard()
        )
        return

    responses = {
        "prof": "Доступные направления:\n• Дошкольное образование\n• Начальное образование\n• Педагогика\n• Физическая культура",
        "enter": "Как поступить:\n1. Паспорт\n2. Аттестат\n3. Подать заявление",
        "hostel": "Общежитие предоставляется иногородним студентам.",
        "starosta": "Староста выбирается голосованием группы.",
        "prepod": "Преподаватели:\n• Иванова И.И. – русский язык\n• Петров П.П. – математика\n• Сидорова С.С. – педагогика"
    }

    text = responses.get(query.data, "Информация не найдена.")
    await query.edit_message_text(text, reply_markup=back_keyboard())

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

app.run_polling()
