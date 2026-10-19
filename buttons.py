from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


async def asosiy_menyu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📚 Kurslar"),
                KeyboardButton(text="📝 Kursga yozilish")
            ],
            [
                KeyboardButton(text="ℹ️ Markaz haqida"),
                KeyboardButton(text="📞 Aloqa")
            ],
        ],
        resize_keyboard=True,
        input_field_placeholder="Kerakli bo'limni tanlang",
    )


def kurs_tugmalari():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Python",
                    callback_data="python",
                )
            ],
            [
                InlineKeyboardButton(
                    text="Web dasturlash",
                    callback_data="web",
                )
            ],
            [
                InlineKeyboardButton(
                    text="Telegram bot",
                    callback_data="bot",
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Bekor qilish",
                    callback_data="bekor",
                )
            ],
        ]
    )


def bekor_tugmasi():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Bekor qilish")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Ma'lumot kiriting",
    )


def tasdiqlash_tugmalari():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Tasdiqlash",
                    callback_data="tasdiq",
                ),
                InlineKeyboardButton(
                    text="❌ Bekor qilish",
                    callback_data="bekor",
                ),
            ]
        ]
    )