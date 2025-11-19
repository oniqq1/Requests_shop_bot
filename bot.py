from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, URLInputFile , ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

import asyncio
import logging
import sys

from commands import (BotCommands, Commands)

from config import BOT_TOKEN as TOKEN


from states.application_form import ApplicationForm, ApplicationDeleteForm
from states.category_form import CategoryDeleteForm , CategoryForm
from states.admin_form import AdminDeleteForm , AdminForm

from database import init_db, add_owner_to_db
from states.chat_form import ChatForm

dp = Dispatcher(storage=MemoryStorage())




async def register_handlers(dp: Dispatcher) -> None:
    from handlers import application_handlers , admin_handlers , category_handlers , chat_handlers

    dp.message.register(application_handlers.command_start_handler, Commands[0])
    dp.message.register(application_handlers.command_help_handler, Commands[1])

    dp.message.register(application_handlers.command_create_request_handler , Commands[2])
    dp.message.register(application_handlers.request_name_handler , ApplicationForm.name , )
    dp.message.register(application_handlers.request_category_handler , ApplicationForm.category)
    dp.message.register(application_handlers.request_phone_number_handler , ApplicationForm.phone)
    dp.message.register(application_handlers.request_comment_handler , ApplicationForm.comment)

    dp.message.register(application_handlers.see_requests_handler , Commands[3])


    dp.message.register(application_handlers.delete_request_handler, Commands[4])
    dp.message.register(application_handlers.delete_ID_request_handler , ApplicationDeleteForm.application_id)

    dp.message.register(category_handlers.command_see_categories_handler , Commands[6])

    # for admin only
    dp.message.register(admin_handlers.command_admin_info_handler , Commands[10])

    dp.message.register(category_handlers.command_create_category_handler , Commands[5])
    dp.message.register(category_handlers.create_category_handler , CategoryForm.category)

    dp.message.register(category_handlers.command_delete_category_handler , Commands[7])
    dp.message.register(category_handlers.delete_category_handler , CategoryDeleteForm.category_id)

    # for owner only
    dp.message.register(admin_handlers.command_add_admin_handler , Commands[8])
    dp.message.register(admin_handlers.add_admin_handler , AdminForm.user_id)

    dp.message.register(admin_handlers.command_delete_admin_handler , Commands[9])
    dp.message.register(admin_handlers.delete_admin_handler , AdminDeleteForm.user_id)

    dp.message.register(admin_handlers.command_owner_info_handler , Commands[11])

    dp.message.register(chat_handlers.command_see_all_pending_requests_handler , Commands[12])
    dp.message.register(chat_handlers.command_write_to_user,ChatForm.user_id)
    dp.message.register(chat_handlers.admin_chat_handler, ChatForm.active)
    dp.message.register(chat_handlers.user_message_handler)


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await bot.set_my_commands(BotCommands)
    await register_handlers(dp)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    init_db()
    add_owner_to_db()
    asyncio.run(main())