from aiogram import Router, F
from aiogram.types import Message
from datetime import datetime

from storage.db import load_state, save_state
from core.engine import SleepEngine
from ui.keyboards import main_kb

router = Router()
engine = SleepEngine()

def format_response(result):
    wb = result["wb"]
    mode = result["mode"]

    if mode == "overtired":
        text = "Похоже на перегул 😣\nПопробуй уложить раньше."
    elif mode == "undertired":
        text = "Похоже на недогул 🙂\nМожно чуть увеличить бодрствование."
    else:
        text = "Сейчас всё стабильно 👍"

    return f"""{text}

Ориентир следующего сна: ~{wb} минут бодрствования.
"""

@router.message(F.text == "/start")
async def start(msg: Message):
    await msg.answer("Я помогу следить за сном малыша 👶", reply_markup=main_kb)

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

@router.message(F.text == "📊 Анализ дня")
async def analyze(msg: Message):
    user_id = msg.from_user.id
    state = load_state(user_id)

    analysis = engine.analyze_day(state)

    if not analysis:
        await msg.answer("Пока недостаточно данных")
        return

    text = f"""
📊 Анализ дня:

Среднее ВБ: {analysis['avg_wb']} мин
Средний сон: {analysis['avg_nap']} мин
Дневных снов: {analysis['count_naps']}

{engine.recommend(analysis, state)}
"""

    await msg.answer(text)

@router.message()
async def dialog(msg: Message):
    user_id = msg.from_user.id
    state = load_state(user_id)

    step = state["dialog"]["step"]
    text = msg.text

    # Шаг 1 — возраст
    if step == "start":
        state["dialog"]["step"] = "age"
        save_state(user_id, state)
        await msg.answer("Сколько месяцев ребенку?")
        return

    elif step == "age":
        try:
            age = int(text)
            state["profile"]["age_months"] = age

            # простая логика норм ВБ
            if age < 6:
                wb = 90
            elif age < 12:
                wb = 120
            else:
                wb = 150

            state["profile"]["target_wb"] = wb

            state["dialog"]["step"] = "done"
            save_state(user_id, state)

            await msg.answer(f"Отлично! Будем ориентироваться на ~{wb} минут ВБ 👍")
            return
        except:
            await msg.answer("Напиши число, например: 6")
            return