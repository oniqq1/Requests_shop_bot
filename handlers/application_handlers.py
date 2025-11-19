from aiogram import types , html
from aiogram.fsm.context import FSMContext

from keyboards import build_categories_name_keyboard , build_categories_id_keyboard , build_standard_keyboard , build_back_keyboard
from states.application_form import ApplicationForm, ApplicationDeleteForm
from databases.applications import create_application , get_applications_by_user , delete_application
from databases.categories import get_all_categories
from models.application_model import ApplicationModel
import re

async def command_start_handler(message: types.Message) -> None:

    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}! \n"
                         f"I'am showy project of shop|business\n"
                         f"There you can : leave a request , see your requests , connect to a manager\n"
                         f"\n"
                         f"All comands:\n\n"
                         f"/start\n"
                         f"/leave_a_request\n"
                         f"/see_requests\n"
                         f"/delete_request\n"
                         f"/admin\n"
                         f"/owner\n"
                         f"/help\n" , reply_markup=build_standard_keyboard())


async def command_help_handler(message: types.Message) -> None:
    await message.answer(f"Here is a list of available commands:\n\n"
                         f"/start - Start the bot and see the welcome message\n"
                         f"/leave_a_request - Leave a request for our services\n"
                         f"/see_requests - View your submitted requests\n"
                         f"/delete_request - Delete a specific request by its ID\n"
                         f"/admin - Access the admin page (if you have permissions)\n"
                         f"/owner - Access the owner page (if you have permissions)\n"
                         f"/help - Get help information about using the bot\n" , reply_markup=build_standard_keyboard())




async def command_create_request_handler(message: types.Message , state : FSMContext) -> None:
    if message.text == '/back':
        await state.clear()
        await message.answer("Operation cancelled. You are back to the main menu." , reply_markup=build_standard_keyboard())
        return

    await message.answer("Please provide the following details to leave a request:\n")
    await message.answer("1. Your full name:", reply_markup=build_back_keyboard())
    await state.set_state(ApplicationForm.name)

async def request_name_handler(message: types.Message , state : FSMContext) -> None:
    if message.text == '/back':
        await state.clear()
        await message.answer("Operation cancelled. You are back to the main menu.")
        return
    NAME_RE = re.compile(r'^[A-Za-zА-Яа-яЁё\s\-]{2,100}$')
    if not NAME_RE.match(message.text):
        await message.answer("Invalid name format. Please enter a valid full name (2-100 characters, letters, spaces, and hyphens only):")
        return
    await state.update_data(name=message.text)
    await message.answer("2. Please choose a category from the following list:", reply_markup=build_categories_name_keyboard())
    await state.set_state(ApplicationForm.category )

async def request_category_handler(message: types.Message , state : FSMContext) -> None:
    if message.text == '/back':
        await state.clear()
        await message.answer("Operation cancelled. You are back to the main menu.", reply_markup=build_standard_keyboard())
        return
    if message.text not in [category.name for category in get_all_categories()]:
        print(get_all_categories())
        await message.answer("Invalid category. Please choose a valid category from the list below:\n" +
                             "\n".join([category.name for category in get_all_categories()]))
        return
    await state.update_data(category=message.text)
    await message.answer("3. Your phone number:" , reply_markup=build_back_keyboard())
    await state.set_state(ApplicationForm.phone)

async def request_phone_number_handler(message: types.Message , state : FSMContext) -> None:
    if message.text == '/back':
        await state.clear()
        await message.answer("Operation cancelled. You are back to the main menu.", reply_markup=build_standard_keyboard())
        return

    PHONE_RE = re.compile(r'^\+?\d{10,15}$')
    if not PHONE_RE.match(message.text):
        await message.answer("Invalid phone number format. Please enter a valid phone number (10-15 digits, optional leading +):", reply_markup=build_back_keyboard())
        return
    await state.update_data(phone=message.text)
    await message.answer("4. Any additional comments (optional):")
    await state.set_state(ApplicationForm.comment)




async def request_comment_handler(message: types.Message , state : FSMContext) -> None:
    await state.update_data(comment=message.text)
    data = await state.get_data()


    App = ApplicationModel(
        user_id=message.from_user.id,
        name=data['name'],
        category=data['category'],
        phone=data['phone'],
        comment=data['comment'], )

    ID = create_application(App)


    await message.answer(f"Thank you for your request!\n\n"
                         f"ID: {ID}\n"
                         f"Name: {data['name']}\n"
                         f"Category: {data['category']}\n"
                         f"Phone: {data['phone']}\n"
                         f"Comment: {data['comment']}\n" , reply_markup=build_standard_keyboard() )

    await state.clear()


async def see_requests_handler(message: types.Message) ->None:


    applications = get_applications_by_user(message.from_user.id)

    if not applications:
        await message.answer("You have no requests.", reply_markup=build_standard_keyboard())
        return

    response = "Your requests:\n\n"
    for app in applications:
        response += (f"ID: {app.id}\n"
                     f"Name: {app.name}\n"
                     f"Category: {app.category}\n"
                     f"Phone: {app.phone}\n"
                     f"Comment: {app.comment}\n"
                     f"Status: {app.status}\n"
                     f"Created At: {app.created_at}\n\n")

    await message.answer(response , reply_markup=build_standard_keyboard())

async def delete_request_handler(message: types.Message , state:FSMContext) ->None:




    applications = get_applications_by_user(message.from_user.id)

    if not applications:
        await message.answer("You have no requests.")
        return

    response = "Your requests:\n\n"
    for app in applications:
        response += (f"ID: {app.id}\n"
                     f"Category: {app.category}\n\n")

    await message.answer(response)
    await message.answer("Please provide the ID of the request you want to delete.\n", reply_markup=build_categories_id_keyboard())
    await state.set_state(ApplicationDeleteForm.application_id)



async def delete_ID_request_handler(message: types.Message , state:FSMContext) ->None:
    if message.text == '/back':
        await state.clear()
        await message.answer("Operation cancelled. You are back to the main menu.", reply_markup=build_standard_keyboard())
        return


    if not message.text.isdigit():
        await message.answer("Please provide a valid request ID to delete.", reply_markup=types.ReplyKeyboardRemove())
        return

    application_id = int(message.text)
    success = delete_application(application_id)

    await state.clear()

    if success:
        await message.answer(f"Request with ID {application_id} has been deleted.", reply_markup=build_standard_keyboard())
        return
    await message.answer(f"Request with ID {application_id} not found.", reply_markup=types.ReplyKeyboardRemove())
