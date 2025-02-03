import asyncio
import os
import requests

from aiogram import *
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, \
    KeyboardButton
from dotenv import *
from keep_alive import keep_alive

keep_alive()


load_dotenv(".env")
TOKEN = os.getenv("BOT_TOKEN")
SERVER_URL = os.getenv("SERVER_URL")
bot = Bot(TOKEN)
disp = Dispatcher()

main_keyboard_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Сайт університету", url="https://suitt.edu.ua/")],
        [InlineKeyboardButton(text="Освітня програма", url="https://suitt.edu.ua/wp-content/uploads/2023/12/121-OPP-2-13-04-B.pdf")],
        [InlineKeyboardButton(text="Навчальний план", url="https://suitt.edu.ua/wp-content/uploads/2023/11/NP_B_121_2023.pdf")],
        [InlineKeyboardButton(text="Силабуси", url="https://suitt.edu.ua/sylabusy-121-inzheneriia-prohramnoho-zabezpechennia-bakalavr/")],
        [InlineKeyboardButton(text="Відгуки", url="https://suitt-software-engineering-feedbacks.pages.dev/")],
        [InlineKeyboardButton(text="Залишити відгук", callback_data="feedback")],
    ]
)

menu_markup = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text="☰ Меню ☰")]
    ]
)

class GiveFeedback(StatesGroup):
    read_feedback = State()

async def save_feedback(username: str, first_name: str, text: str):
    feedback = {
        "username": username,
        "first_name": first_name,
        "text": text
    }
    response = requests.post(SERVER_URL + "/feedbacks", json=feedback)



@disp.message(CommandStart())
async def start_handler(msg: Message):
    await msg.answer_photo(
        photo=types.FSInputFile("img/menu_img.jpg"),
        caption="Шановні студенти і викладачі! Ласкаво прошу  приєднатись до обговорення освітньої програми \"Інженерія програмного забезпечення\" кафедри ІПЗ ДУІТЗ 😉\n"
                "Залишайте свої пропозиції, зауваження, міркування як до самої ОП, так і до складу вибіркових дисциплін, а також взагалі - до всієї системи освіти в ДУІТЗ. З повагою та очікуваннями Чат-бот кафедри ІПЗ.",
        reply_markup=menu_markup,
    )

@disp.message(F.text == "☰ Меню ☰")
async def menu_handler(msg: Message):
    await msg.answer_photo(
        photo=types.FSInputFile("img/menu_img.jpg"),
        caption="☰ Меню ☰",
        reply_markup=main_keyboard_markup,
    )

@disp.callback_query(F.data == "feedback")
async def feedback_handler(query: CallbackQuery, state:FSMContext):
    await state.set_state(GiveFeedback.read_feedback)
    await bot.send_message(query.from_user.id, "Введіть ваш відгук: ")

@disp.message(GiveFeedback.read_feedback)
async def save_feedback_handler(msg: Message, state:FSMContext):
    await state.clear()

    text = msg.text
    first_name = msg.from_user.first_name
    username = msg.from_user.username

    await save_feedback(username, first_name, text)
    await msg.answer("Дякую за ваш відгук!", reply_markup=menu_markup)

async def main():
    await disp.start_polling(bot)


asyncio.run(main())
