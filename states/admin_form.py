from aiogram.fsm.state import StatesGroup, State

class AdminForm(StatesGroup):
    user_id = State()

class AdminDeleteForm(StatesGroup):
    user_id = State()