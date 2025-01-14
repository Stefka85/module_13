from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

api = "____"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

# Создание клавиатуры
kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
kb.add(button, button2)

@dp.message_handler(text='Информация')
async def inform(message: types.Message):
    await message.answer('Бот, считающий, количество калорий.')

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    gender = State()

@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer("привет! я бот помагающий твоему здоровью."
                         "Чтобы посчитать суточную норму калорий нажмите - /Рассчитать", reply_markup=kb)


@dp.message_handler(text='/Рассчитать')
async def set_age(message: types.Message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()


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
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    await message.answer(f'Введите свой пол (М или Ж):')
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
