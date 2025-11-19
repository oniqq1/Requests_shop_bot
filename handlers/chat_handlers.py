from aiogram import types, html
from aiogram.fsm.context import FSMContext
from keyboards import build_standard_keyboard, build_back_keyboard
from states.chat_form import ChatForm
from database import is_admin, get_all_applications_pending , get_applications_by_user



active_chats = {}


async def command_see_all_pending_requests_handler(message: types.Message, state: FSMContext) -> None:
    applications = get_all_applications_pending()
    if not applications:
        await message.answer("Any pending requests.", reply_markup=build_standard_keyboard())
        return

    response = f"Here are pending requests, {html.bold(message.from_user.full_name)}:\n\n"
    for app in applications:
        response += (
            f"Request ID: {app.id}\n"
            f"Name: {app.name}\n"
            f"Contact Info: {app.phone}\n"
            f"Category: {app.category}\n"
            f"Description: {app.comment}\n"
            f"-----------------------\n"
        )
    response += "\nPlease enter the Request ID you want to write to:"
    await state.set_state(ChatForm.user_id)
    await message.answer(response, reply_markup=build_back_keyboard())


async def command_write_to_user(message: types.Message, state: FSMContext) -> None:
    if not is_admin(message.from_user.id):
        await message.answer(
            "You do not have permission to write to users.",
            reply_markup=build_standard_keyboard()
        )
        return

    if message.text == '/back':
        await state.clear()
        await command_see_all_pending_requests_handler(message, state)
        return

    existing_pending = get_all_applications_pending()
    entered_id = message.text.strip()


    selected_app = next((p for p in existing_pending if str(p.id) == entered_id), None)
    if not selected_app:
        await message.answer(
            f"Invalid request ID {entered_id}. Please enter a valid pending request ID.",
            reply_markup=build_back_keyboard()
        )
        return


    user_chat_id = getattr(selected_app, "user_id", None)
    if not user_chat_id:
        await message.answer(
            "Cannot determine user's Telegram ID. Make sure the application stores telegram user_id.",
            reply_markup=build_back_keyboard()
        )
        return


    admin_id = message.from_user.id
    active_chats[admin_id] = user_chat_id


    await state.update_data(chat_user_id=user_chat_id, chat_app_id=selected_app.id)
    await state.set_state(ChatForm.active)

    await message.answer(
        f"Chat started with user {user_chat_id} (Application {selected_app.id}).\n"
        f"Send messages — they will be forwarded. Send /end to finish.",
        reply_markup=build_back_keyboard()
    )


async def admin_chat_handler(message: types.Message, state: FSMContext):
    admin_id = message.from_user.id

    if message.text == "/end" and is_admin(admin_id):
        active_chats.pop(admin_id, None)
        await state.clear()
        await message.answer("Chat closed.", reply_markup=build_standard_keyboard())
        return


    user_id = active_chats.get(admin_id)
    if not user_id:
        await message.answer(
            "No active chat. Start one by selecting a request.",
            reply_markup=build_standard_keyboard()
        )
        await state.clear()
        return


    await message.bot.send_message(
        chat_id=user_id,
        text=f"Admin:\n{message.text}"
    )
    await message.answer("Message sent.", reply_markup=build_back_keyboard())


async def user_message_handler(message: types.Message):
    user_id = message.from_user.id

    for admin_id, target_user in active_chats.items():
        if target_user == user_id:
            name = get_applications_by_user(user_id)[0].name
            await message.bot.send_message(
                chat_id=admin_id,
                text=f"User {name}:\n{message.text}"
            )
            break
