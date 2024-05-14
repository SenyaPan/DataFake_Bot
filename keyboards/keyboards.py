from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_begin_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    process_button = InlineKeyboardButton(text="Process photo",
                                          callback_data="photo button")
    start_button = InlineKeyboardButton(text="Main menu",
                                        callback_data="start")

    keyboard.add(process_button)
    keyboard.add(start_button)

    return keyboard


def get_after_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    button_2 = InlineKeyboardButton(text="Process another photo",
                                    callback_data="another photo button")
    button_3 = InlineKeyboardButton(text="Main menu",
                                    callback_data="start")

    keyboard.add(button_2)
    keyboard.add(button_3)

    return keyboard


def get_feedback_keyboard(filename: str, class_name: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    button_1 = InlineKeyboardButton(text="Yes:)",
                                    callback_data=f'we are right {filename} {class_name}')  # right result
    button_2 = InlineKeyboardButton(text="No:(",
                                    callback_data=f'we are wrong {filename} {class_name}')  # wrong result

    keyboard.add(button_1, button_2)

    return keyboard


def get_start_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    begin_button = InlineKeyboardButton(text="Begin detection",
                                        callback_data="begin")
    info_button = InlineKeyboardButton(text="Info",
                                       callback_data="help")
    keyboard.add(begin_button)
    keyboard.add(info_button)
    return keyboard


def get_start_keyboard_for_Rogovoy() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    begin_button = InlineKeyboardButton(text="Begin detection",
                                        callback_data="begin")
    info_button = InlineKeyboardButton(text="Info",
                                       callback_data="help")
    choose_model = InlineKeyboardButton(text="Choose model",
                                        callback_data="choose")
    keyboard.add(begin_button)
    keyboard.add(info_button)
    keyboard.add(choose_model)
    return keyboard


def get_choose_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=4)
    button1 = InlineKeyboardButton(text="1", callback_data="switch to 1")
    button2 = InlineKeyboardButton(text="2", callback_data="switch to 2")
    button3 = InlineKeyboardButton(text="3", callback_data="switch to 3")
    button4 = InlineKeyboardButton(text="4", callback_data="switch to 4")
    button5 = InlineKeyboardButton(text="5", callback_data="switch to 5")
    button6 = InlineKeyboardButton(text="5", callback_data="switch to 6")
    button7 = InlineKeyboardButton(text="latest", callback_data="switch to 6")
    keyboard.add(button1, button2, button3, button4, button5, button6, button7)
    return keyboard


def get_close_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    button_1 = InlineKeyboardButton(text="Close",
                                    callback_data="close")
    keyboard.add(button_1)
    return keyboard
