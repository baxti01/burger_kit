import logging
import os

from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler

from handlers.callbacks import task_status_handler, set_reminder_handler
from handlers.commands import start, test

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

if __name__ == '__main__':
    load_dotenv(".env")

    application = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
    job_queue = application.job_queue

    start_handler = CommandHandler('start', start)
    test_handler = CommandHandler('test', test)

    task_callbacks_handler = CallbackQueryHandler(task_status_handler, pattern=r'task_status_')
    reminder_callbacks_handler = CallbackQueryHandler(set_reminder_handler, pattern=r'reminder_')

    application.add_handler(start_handler)
    application.add_handler(test_handler)
    application.add_handler(task_callbacks_handler)
    application.add_handler(reminder_callbacks_handler)

    application.run_polling()
