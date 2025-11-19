from http.client import responses

from aiogram import types
from aiogram.fsm.context import FSMContext
from states.category_form import CategoryForm, CategoryDeleteForm
from database import create_category ,  delete_category , get_all_categories , is_admin


async def command_create_category_handler(message: types.Message , state : FSMContext) -> None:

    if not is_admin(message.from_user.id):
        await message.answer("You do not have permission to create categories.")
        return
    await message.answer("Please enter the name of the new category:")
    await state.set_state(CategoryForm.category)

async def create_category_handler(message : types.Message , state : FSMContext) -> None:
    if message.text == '/back':
        await state.clear()
        await message.answer("Operation cancelled. You are back to the main menu.")
        return
    category_name = message.text

    existing_categories = get_all_categories()
    if any(category.name.lower() == category_name.lower() for category in existing_categories ):
        await message.answer(f"The category '{category_name}' already exists. Please choose a different name.")
        return
    if category_name.isdigit():
        await message.answer("Category name cannot be purely numeric. Please enter a valid name.")
        return

    create_category(category_name)
    await message.answer(f"Category '{category_name}' has been created successfully.")
    await state.clear()
    return






async def command_delete_category_handler(message : types.Message , state : FSMContext) -> None:

    if not is_admin(message.from_user.id):
        await message.answer("You do not have permission to delete categories.")
        return




    categories = get_all_categories()

    response = "Available categories:\n\n"
    for category in categories:
        response += f"- {category.name}  ID : {category.id}\n"


    response += f"\nPlease enter the id of the category to delete:"
    await message.answer(response)
    await state.set_state(CategoryDeleteForm.category_id)

async def delete_category_handler(message : types.Message , state : FSMContext) -> None:
    if message.text == '/back':
        await state.clear()
        await message.answer("Operation cancelled. You are back to the main menu.")
        return
    category_id = message.text

    existing_categories = get_all_categories()
    if not any(str(category.id) == category_id for category in existing_categories):
        await message.answer(f"The category '{category_id}' does not exist. Please check the id and try again.")
        return

    if delete_category(category_id):
        await message.answer(f"Category '{category_id}' has been deleted successfully.")
        await state.clear()
        return

    await message.answer("An error occurred while deleting the category. Please try again.")


async def command_see_categories_handler(message: types.Message) ->None:

    categories = get_all_categories()

    if not categories:
        await message.answer("No categories available.")
        return

    response = "Available categories:\n\n"
    for category in categories:
        response += f"- {category.name}  ID : {category.id}\n"

    await message.answer(response)