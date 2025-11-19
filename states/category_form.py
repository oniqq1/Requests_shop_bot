from aiogram.fsm.state import StatesGroup, State

class CategoryForm(StatesGroup):
    category = State()


class CategoryDeleteForm(StatesGroup):
    category_id = State()