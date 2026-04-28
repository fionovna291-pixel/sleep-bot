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

    analysis = engine.analyze(state)
    result = engine.decide(analysis, state)

    text = format_response(result)

    await msg.answer(text, reply_markup=main_kb)