from aiogram import Router
from aiogram.types import Message

from storage.db import load_state, save_state
from core.engine import SleepEngine
from services.formatter import format_response
from ui.keyboards import main_kb

router = Router()

@router.message()
async def handle(message: Message):

    user_id = message.from_user.id

    state = await load_state(user_id)

    if not state:
        state = {
            "today": {"wake_windows": [], "naps": []},
            "profile": {"avg_wb": 120}
        }

    engine = SleepEngine()

    analysis = engine.analyze(state)
    decision = engine.decide(analysis, state)

    text = format_response(analysis, decision)

    await save_state(user_id, state)

    await message.answer(text, reply_markup=main_kb)



