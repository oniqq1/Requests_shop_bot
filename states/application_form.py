from aiogram.fsm.state import StatesGroup, State

class ApplicationForm(StatesGroup):
    name = State()
    category = State()
    phone = State()
    comment = State()

class ApplicationDeleteForm(StatesGroup):
    application_id = State()