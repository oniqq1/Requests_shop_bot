from databases import get_all_categories , get_all_applications_pending


from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def build_categories_name_keyboard():
    categories = get_all_categories()

    keyboard = [
        [KeyboardButton(text=category.name)] for category in categories
    ]

    keyboard.append([KeyboardButton(text="/back")])

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )

def build_categories_id_keyboard():
    categories = get_all_categories()

    keyboard = [
        [KeyboardButton(text=category.id)] for category in categories
    ]

    keyboard.append([KeyboardButton(text="/back")])

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )


def build_standard_keyboard():
    keyboard = [
        [KeyboardButton(text="/help")],
        [KeyboardButton(text="/leave_a_request")],
        [KeyboardButton(text="/see_requests")],
        [KeyboardButton(text="/delete_request")],
    ]

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )

def build_back_keyboard():
    keyboard = [
        [KeyboardButton(text="/back")],
    ]

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )

def build_admin_keyboard():
    pendings = get_all_applications_pending()

    keyboard = [ [KeyboardButton(text=pending.id)] for pending in pendings
    ]

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )