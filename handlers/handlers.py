from datetime import datetime

import numpy as np

from keyboards.keyboards import get_after_keyboard, get_close_keyboard, get_start_keyboard, get_begin_keyboard, \
    get_choose_keyboard, get_start_keyboard_for_Rogovoy, get_feedback_keyboard
from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
import os
from lexicon.lexicon import LEXICON_EN
import requests
from asgiref.sync import sync_to_async

from environs import Env


async def process_start_command(message: Message):
    if message.chat.id == 1084029137 or message.chat.id == 385148863:
        keyboard = get_start_keyboard_for_Rogovoy()
    else:
        keyboard = get_start_keyboard()
    await message.answer(text=LEXICON_EN['/start'], reply_markup=keyboard)


async def process_help_command(query: CallbackQuery):
    keyboard = get_close_keyboard()
    await query.message.answer(text=LEXICON_EN['/help'], reply_markup=keyboard)


async def close(query: CallbackQuery):
    await query.message.delete()


async def begin_handler(query: CallbackQuery):
    keyboard = get_begin_keyboard()
    await query.message.answer(text=LEXICON_EN['options'], reply_markup=keyboard)


@sync_to_async(thread_sensitive=False)
def send_to_detafake(file_path: str, model_num=None, return_path=False):
    env = Env()
    env.read_env('.env')
    url = env('IP_ADDRESS')
    url = f'http://localhost:5000/api/v1/files/analyze?'
    if model_num:
        url += f'model_num={model_num}'
    url += f'&return_path={return_path}'
    headers = {'Accept': 'application/json'}
    with open(file_path, "rb") as f:
        return requests.post(url, headers=headers, files={'uploaded_file': f})


@sync_to_async(thread_sensitive=False)
def get_face_from_detafake(photo_path: str):
    env = Env()
    env.read_env('.env')
    url = env('IP_ADDRESS')
    url = f'http://localhost:5000/api/v1/files/{photo_path}'
    headers = {'Accept': 'application/json'}
    return requests.get(url)


# Загрузка идентификаторов пользователей из файла
def load_whitelist():
    with open('whitelist.txt', 'r') as file:
        return [line.strip() for line in file]


# Проверка, есть ли пользователь в вайтлисте
def is_whitelisted(user_id, whitelist):
    return str(user_id) in whitelist


async def process_photo(message: Message):
    # uncomment strings below when the whitelist would be needed

    # whitelist = load_whitelist()
    # if not is_whitelisted(message.from_user.id, whitelist):
    #     await message.answer(text="Sorry, you have no access to this bot.")
    #     return 1

    await message.answer(text=LEXICON_EN['processing'])
    path_for_photo = 'data/' + str(message.from_user.id)
    try:
        os.mkdir(path_for_photo)
    except:
        pass

    photo_path = f'{path_for_photo}/received_{str(datetime.now().strftime("%y%m%d_%H%M%S"))}.jpg'
    await message.photo[-1].download(destination_file=photo_path)

    if message.chat.id == 1084029137 or message.chat.id == 385148863:
        env = Env()
        env.read_env('.env')
        model_num = env(f'MODEL{message.chat.id}')
        result = await send_to_detafake(photo_path, model_num, True)
    else:
        result = await send_to_detafake(photo_path, return_path=True)

    if result.status_code == 250:
        answer = result.json().get('message')
    elif result.status_code == 200:
        results = result.json().get('response')
        path = result.json().get('path').split('.')[0]
        results_len = len(results)

        for i in range(results_len):
            result_photo_path = f'{path}/{i}.jpg'
            result = await get_face_from_detafake(result_photo_path)
            if not os.path.isdir(f'data/{path}'):
                os.mkdir(f'data/{path}')
            with open(f'data/{result_photo_path}', 'wb') as f:
                f.write(result.content)
            photo = open(f'data/{result_photo_path}', 'rb')
            result_percent = round(results[str(i)] * 100, 2)
            answer = "We think it's fake!" if result_percent > 50 else "We think it's real!"
            await message.answer_photo(photo, caption=f'{result_percent}%\n' + answer)
            keyboard = get_feedback_keyboard(filename=f'data/{result_photo_path}',
                                             class_name='real' if result_percent <= 50 else 'false')
            await message.answer(text=LEXICON_EN['feedback'], reply_markup=keyboard)

        answer = 'All faces were analyzed successfully!'
    else:
        answer = 'Sorry, there was some mistake :('

    await message.answer(text=answer)
    keyboard = get_after_keyboard()
    await message.answer(text=LEXICON_EN['add'], reply_markup=keyboard)
    os.remove(photo_path)


async def process_video(message: Message):
    # uncomment strings below when the whitelist would be needed

    # whitelist = load_whitelist()
    # if not is_whitelisted(message.from_user.id, whitelist):
    #     await message.answer(text="Sorry, you haven't access to this bot.")
    #     return 1

    await message.answer(text=LEXICON_EN['processing'])
    path_for_video = 'data/' + str(message.from_user.id)
    try:
        os.mkdir(path_for_video)
    except:
        pass

    video_path = f'{path_for_video}/received_{str(datetime.now().strftime("%y%m%d_%H%M%S"))}.mp4'
    try:
        await message.video_note.download(destination_file=video_path)
    except:
        await message.video.download(destination_file=video_path)

    if message.chat.id == 1084029137 or message.chat.id == 385148863:
        env = Env()
        env.read_env('.env')
        model_num = env(f'MODEL{message.chat.id}')
        result = await send_to_detafake(video_path, model_num, True)
    else:
        result = await send_to_detafake(video_path, return_path=True)

    if result.status_code == 250:
        answer = result.json().get('message')
    elif result.status_code == 200:
        results = result.json().get('response')
        path = result.json().get('path').split('.')[0]
        results_len = len(list(results.keys()))

        for i in range(results_len):
            result_video_path = f'{path}/{i}.jpg'
            face = await get_face_from_detafake(result_video_path)
            if not os.path.isdir(f'data/{path}'):
                os.mkdir(f'data/{path}')
            with open(f'data/{result_video_path}', 'wb') as f:
                f.write(face.content)
            photo = open(f'data/{result_video_path}', 'rb')
            result_without_none = [x for x in results[str(i)] if x is not None]
            result_percent = round(np.mean(result_without_none) * 100, 2)
            answer = "We think it's fake!" if result_percent > 50 else "We think it's real!"
            await message.answer_photo(photo, caption=f'{result_percent}%\n' + answer)
            keyboard = get_feedback_keyboard(filename=f'data/{result_video_path}',
                                             class_name='real' if result_percent <= 50 else 'fake')
            await message.answer(text=LEXICON_EN['feedback'], reply_markup=keyboard)

        answer = 'All faces were analyzed successfully!'
    else:
        answer = 'Sorry, there was some mistake :('

    await message.answer(text=answer)
    keyboard = get_after_keyboard()
    await message.answer(text=LEXICON_EN['add'], reply_markup=keyboard)
    os.remove(video_path)


async def send_photo(query: CallbackQuery):
    await query.message.delete()
    await query.message.answer(text="Please, upload photo!")


async def send_another_photo(query: CallbackQuery):
    await query.message.delete()
    await query.message.answer(text="Please, upload another photo!")


async def return_to_main_menu(query: CallbackQuery):
    await query.message.delete()
    if query['from']['id'] == 1084029137 or query['from']['id'] == 385148863:
        keyboard = get_start_keyboard_for_Rogovoy()
    else:
        keyboard = get_start_keyboard()

    await query.message.answer(text=LEXICON_EN['/start'], reply_markup=keyboard)


async def choose_model(query: CallbackQuery):
    # await query.message.delete()
    keyboard = get_choose_keyboard()
    await query.message.answer(text='Please choose model version', reply_markup=keyboard)


async def switch_model(query: CallbackQuery):
    # await query.message.delete()
    model_num = query.data.split(' ')[-1]
    os.environ[f'MODEL{query["from"]["id"]}'] = model_num

    await query.message.answer(text=f'Model was switched to {model_num}')


async def write_feedback(query: CallbackQuery):
    _, _, feedback, filename, class_name = query.data.split(' ')

    if feedback == 'right':
        with open("bot_feedback.txt", "a") as text_file:
            text_file.write(f'{filename}, {class_name}, true\n')
    else:
        with open("bot_feedback.txt", "a") as text_file:
            text_file.write(f'{filename}, {class_name}, false\n')
    await query.message.edit_text("Thanks for your feedback!")


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(process_start_command, commands='start')
    dp.register_callback_query_handler(process_help_command, text='help')
    dp.register_callback_query_handler(begin_handler, text='begin')
    dp.register_callback_query_handler(close, text='close')
    dp.register_callback_query_handler(send_photo, text='photo button')
    dp.register_callback_query_handler(send_another_photo, text='another photo button')
    dp.register_callback_query_handler(return_to_main_menu, text='start')
    dp.register_callback_query_handler(choose_model, text='choose')
    dp.register_callback_query_handler(switch_model, regexp=r'switch to \d')
    dp.register_callback_query_handler(write_feedback, regexp=r'we are .*')
    dp.register_message_handler(process_photo, content_types=['photo'])
    dp.register_message_handler(process_video, content_types=['video', 'video_note'])
