import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery

from buttons import (
    asosiy_menyu,
    kurs_tugmalari,
    bekor_tugmasi,
    tasdiqlash_tugmalari,
)

TOKEN = "8954061624:AAGALn1_STqr1Xyjtq461mztr-2X4vBxAoo"

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())


class KursState(StatesGroup):
    ism = State()
    telefon = State()
    kurs = State()
    tasdiqlash = State()

@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()
    menu = await asosiy_menyu() if callable(asosiy_menyu) else asosiy_menyu
    await message.answer(
        "Yaxwimila😁",
        reply_markup=menu,
    )

@dp.message(F.text == "📚 Kurslar")
async def kurslar(message: Message):
    await message.answer(
        "📚 Karocci kurslar",
        reply_markup=kurs_tugmalari(),
    )

# 1. Avval FSM holatidagi kurs tanlash ishlaydi
@dp.callback_query(KursState.kurs, F.data.in_(["python", "web", "bot"]))
async def kurs_tanlash(callback: CallbackQuery, state: FSMContext):
    kurslar_dict = {
        "python": "Python",
        "web": "Web dasturlash",
        "bot": "Telegram bot",
    }

    await state.update_data(kurs=kurslar_dict[callback.data])
    data = await state.get_data()
    await state.set_state(KursState.tasdiqlash)

    await callback.message.answer(
        "📋 Ma'lumotlaringiz:\n\n"
        f"👤 Ism: {data['ism']}\n"
        f"📱 Telefon: {data['telefon']}\n"
        f"🎓 Kurs: {data['kurs']}\n\n"
        "Tasdiqlaysizmi?",
        reply_markup=tasdiqlash_tugmalari(),
    )
    await callback.answer()

# 2. Oddiy holatdagi kurs haqida ma'lumot olish
@dp.callback_query(F.data.in_(["python", "web", "bot"]))
async def kurs_haqida(callback: CallbackQuery, state: FSMContext):
    kurslar_dict = {
        "python": "Python",
        "web": "Web dasturlash",
        "bot": "Telegram bot",
    }
    await callback.message.answer(f"{kurslar_dict[callback.data]} kursini tanladin.")
    await callback.answer()

@dp.message(F.text == "📝 Kursga yoziliw")
async def yozilishni_boshlash(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(KursState.ism)

    await message.answer(
        "Ism familiyangizni kiriting:",
        reply_markup=bekor_tugmasi(),
    )

@dp.message(KursState.ism, F.text)
async def ism_olish(message: Message, state: FSMContext):
    ism = message.text.strip()

    if len(ism) < 3:
        await message.answer("Ism familiyani to'liqroq kiriting:")
        return

    await state.update_data(ism=ism)
    await state.set_state(KursState.telefon)

    await message.answer("Telefon raqamingizni kiriting:")

@dp.message(KursState.telefon, F.text)
async def telefon_olish(message: Message, state: FSMContext):
    telefon = message.text.strip()
    raqamlar = "".join(x for x in telefon if x.isdigit())

    if len(raqamlar) < 7:
         await message.answer("Telefon raqamni to'liq kiriting:")
         return

    await state.update_data(telefon=telefon)
    await state.set_state(KursState.kurs)

    await message.answer(
        "Qaysi kursni tanlaysiz?",
        reply_markup=kurs_tugmalari(),
    )

@dp.callback_query(KursState.tasdiqlash, F.data == "tasdiq")
async def tasdiqlash(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    menu = await asosiy_menyu() if callable(asosiy_menyu) else asosiy_menyu

    await callback.message.answer(
         "✅ Kursga yozilish muvaffaqiyatli!\n\n"
        f"🗿 Ism: {data['ism']}\n"
        f"🖋 Telefon: {data['telefon']}\n"
        f"🛎 Kurs: {data['kurs']}",
        reply_markup=menu,
    )

    await state.clear()
    await callback.answer("Tasdiqlandi!")

@dp.callback_query(F.data == "bekor")
async def bekor_inline(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    menu = await asosiy_menyu() if callable(asosiy_menyu) else asosiy_menyu

    await callback.message.answer(
        "🎃 Jarayon bekor qilindi.",
        reply_markup=menu,
    )
    await callback.answer("Bekor qilindi!")

@dp.message(F.text == "Bekor qiliw")
async def bekor_matn(message: Message, state: FSMContext):
    await state.clear()
    menu = await asosiy_menyu() if callable(asosiy_menyu) else asosiy_menyu

    await message.answer(
        "Jarayon bekor qilindi",
        reply_markup=menu,
    )

# "Markaz haqida" matnini xavfsiz tutish uchun lower() ishlatamiz
@dp.message(F.text.casefold().contains("markaz haqida"))
async def markaz_haqida(message: Message):
    await message.answer(
        "🏢 Markazimiz haqida ma'lumot:\n"
        "Bizda zamonaviy kasblar o'rgatiladi va yuqori darajadagi mutaxassislar tayyorlanadi."
    )

@dp.message(F.text == "📞 Aloqa")
async def aloqa(message: Message):
    await message.answer(
        "📞 Aloqa:\n"
        "Telefon: +998 90 123 45 67\n"
        "Manzil: Markaz manzili."
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())