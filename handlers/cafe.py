from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

router_cafe = Router()

class CafeProduct(StatesGroup):
    name = State()

cafe_db = []

#Легкий уровень
@router_cafe.message(Command('menu'))
async def cmd_menu(message: Message):
    menu_text = (
        "☕ Наше Меню команд:\n"
        "/start — Перезапуск бота\n"
        "/menu — Список всех команд кафе\n"
        "/add_drink — Добавить напиток в базу\n"
        "/drinks — Посмотреть список напитков"
    )
    await message.answer(menu_text)

@router_cafe.message(F.text.lower() == "пока")
async def say_goodbye(message: Message):
    await message.answer("До встречи!")


# Средний и сложный уровень

@router_cafe.callback_query(F.data == 'about')
async def about_cafe(callback: CallbackQuery):
    await callback.message.answer("☕ Наше кафе — это место с самым вкусным кофе!")
    await callback.answer()

@router_cafe.message(Command('add_drink'))
async def start_add_product(message: Message, state: FSMContext):
    await message.answer("Введите название напитка:")
    await state.set_state(CafeProduct.name)

@router_cafe.message(CafeProduct.name)
async def process_product_name(message: Message, state: FSMContext):
    if message.text is None:  # Если прислали не текст, а фото или там стикер
        await message.answer("Ошибка! Введите название напитка текстом:")
        return

    cafe_db.append(message.text)
    await message.answer(f"Напиток '{message.text}' успешно добавлен в меню!")
    await state.clear()

@router_cafe.message(Command('drinks'))
async def show_drinks(message: Message):
    if not cafe_db:
        await message.answer("Menu пока пустое(")
        return
    
    drinks_list = "☕ Список напитков в меню:\n\n" + "\n".join([f"— {drink}" for drink in cafe_db])
    await message.answer(drinks_list)
