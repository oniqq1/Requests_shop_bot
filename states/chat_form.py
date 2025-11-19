from aiogram.fsm.state import StatesGroup, State

class ChatForm(StatesGroup):
    user_id = State()
    active = State()