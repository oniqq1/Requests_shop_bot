from email import message

from aiogram import types , html
from aiogram.fsm.context import FSMContext
from states.admin_form import AdminForm , AdminDeleteForm
from database import is_admin , create_admin , delete_admin
from models.admin_model import AdminModel
from config import OWNER_ID


async def command_admin_info_handler(message: types.Message) -> None:
    if not is_admin(message.from_user.id):
        await message.answer("You do not have permission to access the admin page.")
        return
    await message.answer(f"Welcome to the admin page, {html.bold(message.from_user.full_name)}!\n\n"
                         f"Available commands:\n"
                         f"/create_category - Create a new category\n"
                         f"/see_categories - See all categories\n"
                         f"/delete_category - Delete an existing category\n\n"
                         )

async def command_owner_info_handler(message: types.Message) -> None:
    if message.from_user.id != OWNER_ID:
        await message.answer("You do not have permission to access the admin page.")
        return
    await message.answer(f"Welcome to the OWNER page, {html.bold(message.from_user.full_name)}!\n\n"
                         f"Available commands:\n"
                         f"for admins too\n"
                         f"/create_category - Create a new category\n"
                         f"/see_categories - See all categories\n"
                         f"/delete_category - Delete an existing category\n\n"
                         f"for owner only:\n"
                         f"/add_admin - Add a new admin\n"
                         f"/delete_admin - Delete an existing admin\n"
                         )

async def command_add_admin_handler(message: types.Message , state : FSMContext) -> None:
    if message.text == '/back':
        await state.clear()
        await command_owner_info_handler(message)
        return

    if message.from_user.id != OWNER_ID:
        await message.answer("You do not have permission to add admins.")
        return
    await message.answer("Please enter the user ID of the new admin:")
    await state.set_state(AdminForm.user_id)

async def add_admin_handler(message : types.Message , state : FSMContext) -> None:
    if not message.text.isdigit():
        await message.answer("Invalid user ID. Please enter a numeric user ID.")
        return
    if is_admin(int(message.text)):
        await message.answer(f"The user ID '{message.text}' is already an admin.")
        return

    create_admin(int(message.text))
    await message.answer(f"User ID '{message.text}' has been added as an admin successfully.")
    await state.clear()



async def command_delete_admin_handler(message : types.Message , state : FSMContext) -> None:
    if message.text == '/back':
        await state.clear()
        await command_owner_info_handler(message)
        return

    if message.from_user.id != OWNER_ID:
        await message.answer("You do not have permission to delete admins.")
        return
    await message.answer("Please enter the user ID of the admin to delete:")
    await state.set_state(AdminDeleteForm.user_id)

async def delete_admin_handler(message : types.Message , state : FSMContext) -> None:
    if not message.text.isdigit():
        await message.answer("Invalid user ID. Please enter a numeric user ID.")
        return
    user_id = int(message.text)

    if not is_admin(user_id):
        await message.answer(f"The user ID '{message.text}' is not an admin.")
        return

    delete_admin(user_id)
    await message.answer(f"User ID '{message.text}' has been removed from admins successfully.")
    await state.clear()
