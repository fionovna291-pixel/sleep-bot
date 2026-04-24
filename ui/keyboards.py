from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="😴 Сон начался"),
            KeyboardButton(text="🌞 Проснулся")
        ],
        [
            KeyboardButton(text="📊 Анализ дня")
        ]
    ],
    resize_keyboard=True
)