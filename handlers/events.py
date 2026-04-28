from aiogram import Router, F
from aiogram.types import Message
from datetime import datetime

from storage.db import load_state, save_state
from core.engine import SleepEngine
from ui.keyboards import main_kb

router = Router()
engine = SleepEngine()

# --- СТАРТ И ДИАЛОГ ---

@router.message(F.text == "/start")
async def start(msg: Message):
    user_id = msg.from_user.id
    state = load_state(user_id)

    state["dialog"]["step"] = "age"
    save_state(user_id, state)

    await msg.answer("Привет! 👋\nСколько месяцев ребенку?")

@router.message()
async def dialog(msg: Message):
    user_id = msg.from_user.id
    state = load_state(user_id)

    step = state["dialog"]["step"]
    text = msg.text

    # Ввод возраста
    if step == "age":
        try:
            age = int(text)
            state["profile"]["age_months"] = age

            # простая логика норм
            if age < 6:
                wb = 90
            elif age < 12:
                wb = 120
            else:
                wb = 150

            state["profile"]["target_wb"] = wb

            state["dialog"]["step"] = "done"
            save_state(user_id, state)

            await msg.answer(
                f"Отлично 👍\nБудем ориентироваться на ~{wb} минут бодрствования",
                reply_markup=main_kb
            )
            return

        except:
            await msg.answer("Напиши число, например: 6")
            return

    # если профиль уже заполнен — игнорируем лишний текст
    if step == "done":
        await msg.answer("Используй кнопки ниже 👇", reply_markup=main_kb)

# --- СОБЫТИЯ ДНЯ ---

@router.message(F.text == "🌞 Проснулся")
async def wake(msg: Message):
    user_id = msg.from_user.id
    state = load_state(user_id)

    now = datetime.now()

    sleep_start = state["today"].get("sleep_start")

    if sleep_start:
        nap = (now - sleep_start).total_seconds() / 60
        state["today"]["naps"].append(int(nap))

    state["today"]["last_wake"] = now

    save_state(user_id, state)

    await msg.answer("Записала пробуждение 🌞", reply_markup=main_kb)

@router.message(F.text == "😴 Сон начался")
async def sleep(msg: Message):
    user_id = msg.from_user.id
    state = load_state(user_id)

    now = datetime.now()

    last_wake = state["today"].get("last_wake")

    if last_wake:
        wb = (now - last_wake).total_seconds() / 60
        state["today"]["wake_windows"].append(int(wb))

    state["today"]["sleep_start"] = now

    save_state(user_id, state)

    await msg.answer("Записала начало сна 😴", reply_markup=main_kb)

# --- АНАЛИЗ ---

@router.message(F.text == "📊 Анализ дня")
async def analyze(msg: Message):
    user_id = msg.from_user.id
    state = load_state(user_id)

    analysis = engine.analyze_day(state)

    if not analysis:
        await msg.answer("Пока недостаточно данных 🙂")
        return

    text = f"""
📊 Анализ дня:

Среднее ВБ: {analysis['avg_wb']} мин
Средний сон: {analysis['avg_nap']} мин
Дневных снов: {analysis['count_naps']}

{engine.recommend(analysis, state)}
"""

    await msg.answer(text, reply_markup=main_kb)