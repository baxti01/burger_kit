import os

import pygsheets
from telegram import Update
from telegram.ext import ContextTypes

from handlers.keyboards import job_keyboard_markup
from utils import clean_duplicates, send_notifications


async def task_status_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    jobs = context.job_queue.get_jobs_by_name(
        str(update.effective_chat.id) + query.message.text
    )
    job = jobs[0]
    user_id = job.user_id
    job.schedule_removal()

    text = 'Пользователь с таким идентификатором: {} \n {} задание: \n "{}"'

    if query.data == "task_status_completed":
        text = text.format(update.effective_chat.id, "выполнил", query.message.text)
    if query.data == "task_status_not_complete":
        text = text.format(update.effective_chat.id, "не выполнил", query.message.text)

    await context.bot.send_message(chat_id=user_id, text=text)

    await query.edit_message_text(text="Ответ отправлен.")


async def task_ignored(context: ContextTypes.DEFAULT_TYPE):
    text = f'Пользователь с таким идентификатором: {context.job.chat_id} \n' \
           f'проигнорировал задание: \n "{context.job.data["text"]}"'

    await context.bot.delete_message(
        chat_id=context.job.chat_id,
        message_id=context.job.data["message_id"]
    )

    await context.bot.send_message(chat_id=context.job.user_id, text=text)


async def set_reminder_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    gc = pygsheets.authorize(service_file="cred.json")
    spreadsheet = gc.open_by_url(os.getenv("SPREADSHEET_URL"))
    worksheet = spreadsheet.sheet1
    all_data = worksheet.get_all_values(
        include_tailing_empty=False,
        include_tailing_empty_rows=False
    )

    # удаляем дубликаты и проверяем на
    # валидность данных
    cleaned_data = clean_duplicates(all_data)

    await send_notifications(
        context=context,
        owner_id=update.effective_chat.id,
        callback=task_ignored,
        rows=cleaned_data,
        reply_markup=job_keyboard_markup
    )

    await query.edit_message_text(text="Задачи созданы.")
