import asyncio
import os
import requests

from aiogram import *
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
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
        [InlineKeyboardButton(text="Сайт уныверситету", url="https://suitt.edu.ua/")],
        [InlineKeyboardButton(text="Освітня програма", url="https://suitt.edu.ua/wp-content/uploads/2023/12/121-OPP-2-13-04-B.pdf")],
        [InlineKeyboardButton(text="Навчальний план", url="https://suitt.edu.ua/wp-content/uploads/2023/11/NP_B_121_2023.pdf")],
        [InlineKeyboardButton(text="Силабуси", url="https://suitt.edu.ua/sylabusy-121-inzheneriia-prohramnoho-zabezpechennia-bakalavr/")],
        [InlineKeyboardButton(text="Відгуки", url="https://suitt-software-engineering-feedbacks.pages.dev/")],
        [InlineKeyboardButton(text="Залишити відгук", callback_data="feedback")],
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
    await msg.answer(
        "Ласкаво просимо до телеграм боту освітньо-професійної програми \"Інженерія програмного забезпечення\" Державного університету інтелектуальних технологій і зв'язку! 😉"
        "\nТут ви можете залишити свої пропозиції щодо освітньої програми",
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
    await msg.answer("Дякую за ваш відгук!", reply_markup=main_keyboard_markup)

async def main():
    await disp.start_polling(bot)


asyncio.run(main())
