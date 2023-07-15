from telegram import InlineKeyboardButton, InlineKeyboardMarkup

main_menu = [
    [InlineKeyboardButton("Создать задачи", callback_data="reminder_set")]
]
main_menu_markup = InlineKeyboardMarkup(main_menu)

job_keyboard = [
    [
        InlineKeyboardButton("Выполнено", callback_data='task_status_completed'),
        InlineKeyboardButton("Не выполено", callback_data='task_status_not_complete')
    ],
]
job_keyboard_markup = InlineKeyboardMarkup(job_keyboard)
