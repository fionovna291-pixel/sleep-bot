from aiogram import Router, F
from aiogram.types import Message
from datetime import datetime

from storage.db import get_user, save_sleep_start, save_wakeup, save_wake_window
from services.sleep_engine import SleepEngine
from services.formatter import format_response
from ui.keyboards import main_kb

router = Router()
engine = SleepEngine()

@router.message(F.text == "/start")
async def start(message: Message):
    await message.answer("Привет! 👋\nСколько месяцев ребенку?")

@router.message(lambda m: m.text.isdigit())
async def set_age(message: Message):
    user = get_user(message.from_user.id)

    age = int(message.text)
    user["profile"]["age"] = age

    # простая логика
    if age <= 3:
        avg = 60
    elif age <= 6:
        avg = 90
    else:
        avg = 120

    user["profile"]["avg_wb"] = avg

    await message.answer(
        f"Ок 👍\nСреднее ВБ: ~{avg} минут",
        reply_markup=main_kb
    )

@router.message(F.text == "😴 Сон начался")
async def sleep_start(message: Message):
    save_sleep_start(message.from_user.id)
    await message.answer("Записала 😴")

@router.message(F.text == "🌞 Проснулся")
async def wake_up(message: Message):
    user_id = message.from_user.id

    duration = save_wakeup(user_id)

    if duration is None:
        await message.answer("Сначала нажми 'Сон начался'")
        return

    # считаем ВБ
    now = datetime.now()
    user = get_user(user_id)

    if user["today"]["wake_windows"]:
        last_sleep = now
        wb = duration  # упрощенно
    else:
        wb = duration

    save_wake_window(user_id, wb)

    await message.answer(f"Сон: {duration} мин")

@router.message(F.text == "📊 Анализ дня")
async def analyze(message: Message):
    user = get_user(message.from_user.id)

    analysis = engine.analyze(user)
    wb = engine.recommend(user, analysis)

    text = format_response(analysis, wb)

    await message.answer(text)

@router.message()
async def fallback(message: Message):
    await message.answer("Используй кнопки 👇", reply_markup=main_kb)