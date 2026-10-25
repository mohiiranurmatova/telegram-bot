import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# BotFather'dan olgan tokeningizni quyidagi qo'shtirnoq ichiga yozing:
TOKEN = "8189132659:AAFIVVfgapYe9IfGzCwOQB89QxyL1riWg3I"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ==========================================
# BAZA: HAR BIR FAN UCHUN 10 TA BOSQICHLI SAVOLLAR
# ==========================================
QUESTIONS = {
    "math": [
        {"level": "🟢 Oson (1/10)", "q": "5 + 7 * 2 = ?", "options": [("17", "opt1"), ("24", "opt2"), ("19", "opt3")], "correct": "opt3"},
        {"level": "🟢 Oson (2/10)", "q": "120 / 4 + 15 = ?", "options": [("45", "opt1"), ("35", "opt2"), ("50", "opt3")], "correct": "opt1"},
        {"level": "🟢 Oson (3/10)", "q": "15 * 4 - 30 = ?", "options": [("20", "opt1"), ("30", "opt2"), ("40", "opt3")], "correct": "opt2"},
        {"level": "🟢 Oson (4/10)", "q": "Agar x + 15 = 40 bo'lsa, x ni toping:", "options": [("15", "opt1"), ("20", "opt2"), ("25", "opt3")], "correct": "opt3"},
        {"level": "🟡 O'rta (5/10)", "q": "2x + 10 = 30 tenglamadagi x ni toping:", "options": [("10", "opt1"), ("15", "opt2"), ("20", "opt3")], "correct": "opt1"},
        {"level": "🟡 O'rta (6/10)", "q": "4/5 qismi 20 ga teng bo'lgan sonni toping:", "options": [("20", "opt1"), ("25", "opt2"), ("30", "opt3")], "correct": "opt2"},
        {"level": "🟡 O'rta (7/10)", "q": "3x - 5 = 10 + 2x tenglamadagi x ni toping:", "options": [("12", "opt1"), ("15", "opt2"), ("18", "opt3")], "correct": "opt2"},
        {"level": "🟡 O'rta (8/10)", "q": "Kvadratning perimetri 36 sm bo'lsa, uning yuzasi nechiga teng?", "options": [("36", "opt1"), ("64", "opt2"), ("81", "opt3")], "correct": "opt3"},
        {"level": "🔴 Qiyin (9/10)", "q": "Ikki sonning yig'indisi 30, ayirmasi 10 ga teng. Shu sonlarni toping:", "options": [("20 va 10", "opt1"), ("15 va 15", "opt2"), ("25 va 5", "opt3")], "correct": "opt1"},
        {"level": "🔴 Qiyin (10/10)", "q": "Log2(32) + 3^2 ni hisoblang:", "options": [("12", "opt1"), ("14", "opt2"), ("16", "opt3")], "correct": "opt2"}
    ],
    "uzb": [
        {"level": "🟢 Oson (1/10)", "q": "Alifboda nechta harf bor?", "options": [("28 ta", "opt1"), ("29 ta", "opt2"), ("30 ta", "opt3")], "correct": "opt2"},
        {"level": "🟢 Oson (2/10)", "q": "Qaysi qatordagi barcha so'zlar unli harf bilan boshlanadi?", "options": [("Anor, daftar", "opt1"), ("O'rik, olma", "opt2"), ("Maktab, qalam", "opt3")], "correct": "opt2"},
        {"level": "🟢 Oson (3/10)", "q": "Ot so'z turkumiga qaysi so'z kiradi?", "options": [("Kitob", "opt1"), ("Yugurmoq", "opt2"), ("Chiroyli", "opt3")], "correct": "opt1"},
        {"level": "🟢 Oson (4/10)", "q": "\"Kitoblar\" so'zidagi qo'shimcha turini toping:", "options": [("Egalik", "opt1"), ("Ko'plik", "opt2"), ("Kelishik", "opt3")], "correct": "opt2"},
        {"level": "🟡 O'rta (5/10)", "q": "Quyidagilardan qaysi biri fe'l?", "options": [("Go'zal", "opt1"), ("O'qimoq", "opt2"), ("Tosh", "opt3")], "correct": "opt2"},
        {"level": "🟡 O'rta (6/10)", "q": "Berilganlardan qaysi biri egalik qo'shimchasini olgan?", "options": [("Kitoblar", "opt1"), ("Kitobim", "opt2"), ("Kitobga", "opt3")], "correct": "opt2"},
        {"level": "🟡 O'rta (7/10)", "q": "\"Yaxshi\" so'zining antonimi qaysi?", "options": [("Katta", "opt1"), ("Yomon", "opt2"), ("Shirin", "opt3")], "correct": "opt2"},
        {"level": "🟡 O'rta (8/10)", "q": "Qaysi qo'shma so'z qo'shib yoziladi?", "options": [("Temir yo'l", "opt1"), ("Oq bilak", "opt2"), ("Oqqush", "opt3")], "correct": "opt3"},
        {"level": "🔴 Qiyin (9/10)", "q": "Sifat darajasi: \"Eng shirin\" birikmasi qaysi darajada?", "options": [("Oddiy", "opt1"), ("Orttirma", "opt2"), ("Qiyosiy", "opt3")], "correct": "opt2"},
        {"level": "🔴 Qiyin (10/10)", "q": "Qaysi gapda uyushiq bo'laklar qatnashgan?", "options": [("Bog'da olma, o'rik, gilos pishdi.", "opt1"), ("Kecha yomg'ir yog'di.", "opt2"), ("O'quvchi dars qildi.", "opt3")], "correct": "opt1"}
    ],
    "eng": [
        {"level": "🟢 Oson (1/10)", "q": "Choose the correct pronoun: '___ is a smart student.'", "options": [("He", "opt1"), ("They", "opt2"), ("We", "opt3")], "correct": "opt1"},
        {"level": "🟢 Oson (2/10)", "q": "What is the plural form of 'child'?", "options": [("Childs", "opt1"), ("Children", "opt2"), ("Childes", "opt3")], "correct": "opt2"},
        {"level": "🟢 Oson (3/10)", "q": "Choose the correct verb: 'I ___ to school every day.'", "options": [("goes", "opt1"), ("go", "opt2"), ("going", "opt3")], "correct": "opt2"},
        {"level": "🟢 Oson (4/10)", "q": "What is the Past Simple form of 'go'?", "options": [("Goed", "opt1"), ("Gone", "opt2"), ("Went", "opt3")], "correct": "opt3"},
        {"level": "🟡 O'rta (5/10)", "q": "Choose the correct preposition: 'The book is ___ the table.'", "options": [("in", "opt1"), ("on", "opt2"), ("at", "opt3")], "correct": "opt2"},
        {"level": "🟡 O'rta (6/10)", "q": "What is the comparative form of 'big'?", "options": [("more big", "opt1"), ("bigger", "opt2"), ("biggest", "opt3")], "correct": "opt2"},
        {"level": "🟡 O'rta (7/10)", "q": "Choose the correct modal verb: 'You ___ obey the rules.'", "options": [("can", "opt1"), ("must", "opt2"), ("may", "opt3")], "correct": "opt2"},
        {"level": "🟡 O'rta (8/10)", "q": "What is the Past Participle of 'write'?", "options": [("wrote", "opt1"), ("written", "opt2"), ("writing", "opt3")], "correct": "opt2"},
        {"level": "🔴 Qiyin (9/10)", "q": "Choose the correct Passive Voice: 'They build houses.'", "options": [("Houses are built by them.", "opt1"), ("Houses were built", "opt2"), ("Houses is built", "opt3")], "correct": "opt1"},
        {"level": "🔴 Qiyin (10/10)", "q": "Choose the correct First Conditional sentence:", "options": [("If it rains, I will stay at home.", "opt1"), ("If it rains, I stay.", "opt2"), ("If it rained, I would stay.", "opt3")], "correct": "opt1"}
    ],
    "fiz": [
        {"level": "🟢 Oson (1/10)", "q": "Tezlikni topish formulasi qaysi?", "options": [("v = s / t", "opt1"), ("v = a * t", "opt2"), ("v = F / m", "opt3")], "correct": "opt1"},
        {"level": "🟢 Oson (2/10)", "q": "Massaning XHdagi asosiy birligi nima?", "options": [("metr", "opt1"), ("kilogramm", "opt2"), ("soniya", "opt3")], "correct": "opt2"},
        {"level": "🟢 Oson (3/10)", "q": "Kuch birligi kim sharafiga qo'yilgan?", "options": [("Nyuton", "opt1"), ("Joul", "opt2"), ("Watt", "opt3")], "correct": "opt1"},
        {"level": "🟢 Oson (4/10)", "q": "Nyutonning 2-qonuni formulasi qaysi?", "options": [("F = m * g", "opt1"), ("F = m * a", "opt2"), ("F = k * x", "opt3")], "correct": "opt2"},
        {"level": "🟡 O'rta (5/10)", "q": "Zichlik formulasi qaysi?", "options": [("rho = m / V", "opt1"), ("rho = F / s", "opt2"), ("rho = a * t", "opt3")], "correct": "opt1"},
        {"level": "🟡 O'rta (6/10)", "q": "Bosimni aniqlash formulasi qaysi?", "options": [("p = m * g", "opt1"), ("p = F / S", "opt2"), ("p = v * t", "opt3")], "correct": "opt2"},
        {"level": "🟡 O'rta (7/10)", "q": "Jism 4 s ichida 20 m/s tezlikka erishdi. Uning tezlanishi qanday?", "options": [("5 m/s²", "opt1"), ("80 m/s²", "opt2"), ("0.2 m/s²", "opt3")], "correct": "opt1"},
        {"level": "🟡 O'rta (8/10)", "q": "Arximed kuchining formulasi qaysi?", "options": [("F = m * g", "opt1"), ("F = rho * g * V", "opt2"), ("F = k * x^2 / 2", "opt3")], "correct": "opt2"},
        {"level": "🔴 Qiyin (9/10)", "q": "Kinetik energiya formulasi qaysi?", "options": [("E = m * g * h", "opt1"), ("E = m * v^2 / 2", "opt2"), ("E = F * s", "opt3")], "correct": "opt2"},
        {"level": "🔴 Qiyin (10/10)", "q": "O'zgarmas tok kuchi uchun Om qonuni formulasi qaysi?", "options": [("I = U / R", "opt1"), ("I = q / t", "opt2"), ("I = P / U", "opt3")], "correct": "opt1"}
    ]
}

# ==========================================
# 1. SINF TUGMALARI
# ==========================================
def get_grades_keyboard():
    buttons = []
    row = []
    for i in range(1, 12):
        row.append(InlineKeyboardButton(text=f"{i}-sinf", callback_data=f"grade_{i}"))
        if len(row) == 3:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# ==========================================
# 2. FANLAR MENYUSI
# ==========================================
def get_subjects_keyboard(grade: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📐 Matematika", callback_data=f"sub_{grade}_math_0"),
                InlineKeyboardButton(text="🇺🇿 Ona tili", callback_data=f"sub_{grade}_uzb_0")
            ],
            [
                InlineKeyboardButton(text="🇬🇧 Ingliz tili", callback_data=f"sub_{grade}_eng_0"),
                InlineKeyboardButton(text="⚡️ Fizika", callback_data=f"sub_{grade}_fiz_0")
            ],
            [
                InlineKeyboardButton(text="⬅️ Sinfni o'zgartirish", callback_data="back_to_grades")
            ]
        ]
    )

# ==========================================
# 3. /START BUYRUG'I
# ==========================================
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        f"Assalomu alaykum, **{message.from_user.first_name}**! 👋\n\n"
        "📚 1-11-sinf o'quvchilari uchun 10 bosqichli qiyinlashib boruvchi test botiga xush kelibsiz.\n"
        "Bilimingizni sinovdan o'tkazish uchun **o'zingizga kerakli sinfni tanlang**:",
        reply_markup=get_grades_keyboard(),
        parse_mode="Markdown"
    )

# ==========================================
# 4. SINF TANLANGANDA
# ==========================================
@dp.callback_query(F.data.startswith("grade_"))
async def grade_chosen(callback: types.CallbackQuery):
    await callback.answer()  # Birinchi navbatda tugma aylanishini to'xtatish
    grade = callback.data.split("_")[1]
    await callback.message.edit_text(
        f"🎯 Siz **{grade}-sinf**ni tanladingiz.\n\n"
        "Bilimingizni sinash uchun **fanni tanlang**:",
        reply_markup=get_subjects_keyboard(grade),
        parse_mode="Markdown"
    )

# ==========================================
# 5. ORQAGA QAYTISH
# ==========================================
@dp.callback_query(F.data == "back_to_grades")
async def back_to_grades(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "📚 Qaytadan sinfni tanlang:",
        reply_markup=get_grades_keyboard()
    )

# ==========================================
# 6. SAVOLNI CHIQARISH
# ==========================================
@dp.callback_query(F.data.startswith("sub_"))
async def subject_chosen(callback: types.CallbackQuery):
    await callback.answer()
    _, grade, subject, step_str = callback.data.split("_")
    step = int(step_str)
    
    subject_names = {
        "math": "Matematika",
        "uzb": "Ona tili",
        "eng": "Ingliz tili",
        "fiz": "Fizika"
    }
    sub_name = subject_names.get(subject, "Fan")
    q_data = QUESTIONS[subject][step]
    
    buttons = []
    for text, cdata in q_data["options"]:
        buttons.append([InlineKeyboardButton(text=text, callback_data=f"ans_{grade}_{subject}_{step}_{cdata}")])
    
    buttons.append([InlineKeyboardButton(text="🔄 Asosiy menyu", callback_data="back_to_grades")])
    
    await callback.message.edit_text(
        f"📖 **{grade}-sinf | {sub_name}**\n"
        f"🔸 **Daraja:** {q_data['level']}\n\n"
        f"❓ **Savol:** {q_data['q']}",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
        parse_mode="Markdown"
    )

# ==========================================
# 7. JAVOBNI TEKSHIRISH
# ==========================================
@dp.callback_query(F.data.startswith("ans_"))
async def check_answer(callback: types.CallbackQuery):
    await callback.answer()  # Tugma qotib qolmasligi uchun darhol to'xtatiladi
    _, grade, subject, step_str, chosen_opt = callback.data.split("_")
    step = int(step_str)
    
    q_data = QUESTIONS[subject][step]
    
    if chosen_opt == q_data["correct"]:
        next_step = step + 1
        if next_step < len(QUESTIONS[subject]):
            await callback.message.edit_text(
                f"✅ **To'g'ri javob!** 🎉\n\n"
                f"Keyingi savolga o'tish uchun pastdagi tugmani bosing:",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="➡️ Keyingi savol", callback_data=f"sub_{grade}_{subject}_{next_step}")],
                    [InlineKeyboardButton(text="🔄 Asosiy menyu", callback_data="back_to_grades")]
                ]),
                parse_mode="Markdown"
            )
        else:
            await callback.message.edit_text(
                f"🏆 **Tabriklayman!** Siz ushbu fanning barcha 10 ta qiyinlik bosqichini muvaffaqiyatli yakunladingiz! 🚀",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="🔄 Asosiy menyu", callback_data="back_to_grades")]
                ]),
                parse_mode="Markdown"
            )
    else:
        await callback.message.edit_text(
            f"❌ **Noto'g'ri javob!** 😢\n\n"
            f"Afsuski, bu savolda xato qildingiz. Qaytadan urinib ko'rasizmi?",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔄 Qaytadan urinish", callback_data=f"sub_{grade}_{subject}_{step}")],
                [InlineKeyboardButton(text="🔄 Asosiy menyu", callback_data="back_to_grades")]
            ]),
            parse_mode="Markdown"
        )

# ==========================================
# 8. BOTNI ISHGA TUSHIRISH
# ==========================================
async def main():
    logging.basicConfig(level=logging.INFO)
    print("Bot muvaffaqiyatli ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())