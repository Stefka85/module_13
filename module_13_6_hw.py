from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api = "7687027126:AAETT9HHr9J24acv5YImFmExj4pBnNQiJTo"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

# Создание клавиатуры
kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
kb.add(button, button2)

kb2 = InlineKeyboardMarkup()
button3 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data = 'calories')
button4 = InlineKeyboardButton(text='Формулы расчёта', callback_data = 'formulas')
kb2.add(button3, button4)


kb_gender = ReplyKeyboardMarkup(resize_keyboard=True)
button_g_m = KeyboardButton(text="М")
button_g_w = KeyboardButton(text="Ж")
kb_gender.row(button_g_m, button_g_w)



@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(f"привет! я бот помагающий твоему здоровью."
                         "Чтобы посчитать суточную норму калорий, нажмите - '/Calories' ", reply_markup=kb)
    # оставил calories, вместо рассчитать, т.к. иначе приходиться вводить "рассчитать", а не нажимать в боте тг.

@dp.message_handler(text='Информация')
async def inform(message: types.Message):
    await message.answer('Этот бот рассчитывает суточную норму калорий на основе введенных данных.')

@dp.callback_query_handler(text="formulas")
async def get_formulas(call):
    await call.message.answer(
        "Упрощенная формула Миффлина-Сан Жеора: "
        "\n-для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5 "
        "\n-для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161"
    )
    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await call.answer()
    await UserState.age.set()

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    gender = State()

@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост (см):")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес (кг):")
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_gender(message: types.Message, state: FSMContext):
    await state.update_data(weight=message.text)
    await message.answer('Выберите свой пол:', reply_markup=kb_gender)
    await UserState.gender.set()

@dp.message_handler(state=UserState.gender)
async def calculate_calories(message: types.Message, state: FSMContext):
    await state.update_data(gender=message.text)
    data = await state.get_data()

    # Проверка на корректность введенного пола
    if data["gender"] not in ["М", "Ж"]:
        await message.answer("Пожалуйста, введите корректный пол (М или Ж).")
        return

    # Расчет калорий
    if data["gender"] == "М":
        calories = (int(data["weight"]) * 10 + int(data["growth"]) * 6.25 - int(data["age"]) * 5 + 5)
    else:  # data["gender"] == "Ж"
        calories = (int(data["weight"]) * 10 + int(data["growth"]) * 6.25 - int(data["age"]) * 5 - 161)
    await message.answer(f'Ваша суточная норма калорий: {calories} (ккал)')
    await state.finish()


@dp.message_handler()
async def all_messages(message: types.Message):
    await message.answer("Введите команду /start, чтобы начать общение.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)