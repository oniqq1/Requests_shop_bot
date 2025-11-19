from aiogram.types.bot_command import BotCommand
from aiogram.filters import Command

BotCommands = [
    BotCommand(command="start", description="Start the bot"),
    BotCommand(command="help", description="Get help information"),

    BotCommand(command="leave_a_request", description="Leave a request"),
    BotCommand(command="see_requests", description="View your requests"),
    BotCommand(command="delete_request", description="Delete a request"),

    BotCommand(command="create_category", description="Create a new category (Admin only)"),
    BotCommand(command="see_categories", description="View all categories"),
    BotCommand(command="delete_category", description="Delete a category (Admin only)"),

    BotCommand(command="add_admin", description="Add admin rights (Owner only)"),
    BotCommand(command="delete_admin", description="Delete admin rights (Owner only)"),

    BotCommand(command="admin", description="Admin page (Admin only)"),
    BotCommand(command="owner", description="Owner page (Owner only)"),

    BotCommand(command="start_chat", description="Start a chat with with user (Admin only)"),
    ]

Commands = [
    Command("start"),
    Command("help"),

    Command("leave_a_request"),
    Command("see_requests"),
    Command("delete_request"),

    Command("create_category"),
    Command("see_categories"),
    Command("delete_category"),

    Command("add_admin"),
    Command("delete_admin"),

    Command("admin"),
    Command("owner"),

    Command("start_chat"),
]