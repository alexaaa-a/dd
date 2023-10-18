import telebot
from telebot import custom_filters
from telebot import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State

state_storage = StateMemoryStorage()
# Вставить свой токет или оставить как есть, тогда мы создадим его сами
bot = telebot.TeleBot("6413962426:AAFSYqey5j0qzKdj-Yxk4IWmSZuPjgYv4zs",
                      state_storage=state_storage, parse_mode='Markdown')


class PollState(StatesGroup):
    name = State()
    age = State()


class HelpState(StatesGroup):
    wait_text = State()


text_poll = "Регистрация для географов"  # Можно менять текст
text_button_1 = "Информация про *реки*"  # Можно менять текст
text_button_2 = "Информация про *горы*"  # Можно менять текст
text_button_3 = "Список городов-*миллиоников* РФ"  # Можно менять текст
text_button_4 = "Ссылочка на автора бота)"  # Можно менять текст

menu_keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_poll,
    )
)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_1,
    )
)

menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_2,
    ),
    telebot.types.KeyboardButton(
        text_button_3,
    )
)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_4,
    )
)


@bot.message_handler(state="*", commands=['start'])
def start_ex(message):
    bot.send_message(
        message.chat.id,
        'Ку, географ! Давай быстренько пройдем регистрацию-опрос?)',  # Можно менять текст
        reply_markup=menu_keyboard)


@bot.message_handler(func=lambda message: text_poll == message.text)
def first(message):
    bot.send_message(message.chat.id, 'Как *тебя* зовут?')  # Можно менять текст
    bot.set_state(message.from_user.id, PollState.name, message.chat.id)


@bot.message_handler(state=PollState.name)
def name(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text
    bot.send_message(message.chat.id,
                     ' Сколько _лет_ ты замаешься [географией](https://ru.wikipedia.org/wiki/%D0%93%D0%B5%D0%BE%D0%B3%D1%80%D0%B0%D1%84%D0%B8%D1%8F) ?')  # Можно менять текст
    bot.set_state(message.from_user.id, PollState.age, message.chat.id)


@bot.message_handler(state=PollState.age)
def age(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['age'] = message.text
    bot.send_message(message.chat.id, 'Опрос закончен!', reply_markup=menu_keyboard)  # Можно менять текст
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(func=lambda message: text_button_1 == message.text)
def help_command(message):
    bot.send_message(message.chat.id,
                     "Исток — место, где река берёт своё начало. Русло — естественное углубление, выработанное рекой. Устье — место впадения реки в другую реку, озеро, море или океан",
                     reply_markup=menu_keyboard)  # Можно менять текст


@bot.message_handler(func=lambda message: text_button_2 == message.text)
def help_command(message):
    bot.send_message(message.chat.id,
                     "Вершина – высшая точка горы или массива; Пик — остроконечная вершина; Купол — вершина с круглыми формами; Маршрут – путь выхода на вершину и спуска.",
                     reply_markup=menu_keyboard)  # Можно менять текст


@bot.message_handler(func=lambda message: text_button_3 == message.text)
def help_command(message):
    bot.send_message(message.chat.id,
                     "Москва; Санкт-Петербург; Новосибирск; Екатеринбург; Казань; Нижний Новгород; Челябинск; Самара; Уфа; Ростов-на-Дону; Омск; Воронеж; Пермь; Волгоград; С недавнего времени Краснодар.",
                     reply_markup=menu_keyboard)  # Можно менять текст


@bot.message_handler(func=lambda message: text_button_4 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "Можешь звать меня _Ульяной_, лови мой [ВК] (https://vk.com/voolco)",
                     reply_markup=menu_keyboard)  # Можно менять текст


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.TextMatchFilter())

bot.infinity_polling()