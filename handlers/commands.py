from telegram import Update
from telegram.ext import ContextTypes

from handlers.keyboards import main_menu_markup, job_keyboard_markup


async def start(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):
    chat_id = update.effective_chat.id
    text = "Главной меню бота созданного \nдля тестового задания."
    await context.bot.send_message(chat_id=chat_id, text=text, reply_markup=main_menu_markup)


async def test(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):
    chat_id = update.effective_chat.id
    text = "123"
    await context.bot.send_message(chat_id=chat_id, text=text, reply_markup=job_keyboard_markup)
