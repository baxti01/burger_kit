from datetime import datetime
from typing import List, Callable

from telegram._utils.types import ReplyMarkup
from telegram.ext import ContextTypes


def clean_duplicates(rows: List):
    data_ = set()
    date_format = "%d.%m.%Y %H:%M:%S"
    for row in rows:
        chat_id = int(row[0])
        text = row[1]
        answer_time = datetime.strptime(row[-1], date_format)

        data_.add((chat_id, text, answer_time))

    return data_


async def send_notifications(
        context: ContextTypes.DEFAULT_TYPE,
        owner_id: int,
        callback: Callable,
        rows: List,
        reply_markup: ReplyMarkup
):
    for chat_id, text, answer_time in rows:
        message = await context.bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=reply_markup
        )
        context.job_queue.run_once(
            callback=callback,
            when=answer_time - datetime.now(),
            name=str(chat_id) + text,
            chat_id=chat_id,
            user_id=owner_id,
            data={"text": text, "message_id": message.id}
        )
