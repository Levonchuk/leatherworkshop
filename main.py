import telebot
from telebot import types

API_TOKEN = "YOUR_API_TOKEN"

bot = telebot.TeleBot(API_TOKEN)

# Основное меню
main_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(types.KeyboardButton('📜 Каталог'))
main_menu.add(types.KeyboardButton('🛒 Оформить заказ'))
main_menu.add(types.KeyboardButton('📞 Связаться с оператором'))
main_menu.add(types.KeyboardButton('❓ Помощь'))

# Меню каталога
catalog_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
catalog_menu.add(types.KeyboardButton('Кожаные сумки'))
catalog_menu.add(types.KeyboardButton('Кошельки'))
catalog_menu.add(types.KeyboardButton('Ремни'))
catalog_menu.add(types.KeyboardButton('Браслеты'))
catalog_menu.add(types.KeyboardButton('🔙 Назад'))

# Описание товаров
items = {
    'Кожаные сумки': {
        'Шоппер': 'Описание: Высококачественная кожаная сумка для повседневной жизни.',
        'Поясная сумка': 'Описание: Стильная и удобная кожаная сумка для прогулок и отдыха.'
    },
    'Кошельки': {
        'Зиппер': 'Описание: Кожаный кошелек на молнии с множеством отделений.',
        'Бифолд с монетницей': 'Описание: Компактный и стильный кожаный кошелек.'
    },
    'Ремни': {
        'Брючный ремень': 'Описание: Прочный кожаный ремень с классической пряжкой.',
        'Джинсовый ремень': 'Описание: Стильный кожаный ремень для повседневного использования.'
    },
    'Браслеты': {
        'Мужской браслет': 'Описание: Кожаный брутальный браслет с металлическими вставками.',
        'Женский браслет': 'Описание: Стильный кожаный браслет для модных образов.'
    }
}

# Флаги для отслеживания текущего состояния
is_ordering = False
is_contacting_operator = False
current_level = 'main'
selected_item = None
selected_subitem = None


# Команда /start
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    global is_ordering, is_contacting_operator, current_level, selected_item, selected_subitem
    is_ordering = False
    is_contacting_operator = False
    current_level = 'main'
    selected_item = None
    selected_subitem = None
    bot.send_message(message.chat.id, "Добро пожаловать в наш магазин изделий из кожи!", reply_markup=main_menu)


# Обработка текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global is_ordering, is_contacting_operator, current_level, selected_item, selected_subitem

    if message.text == '📜 Каталог':
        current_level = 'catalog'
        bot.send_message(message.chat.id, "Выберите категорию:", reply_markup=catalog_menu)
        selected_item = None
        selected_subitem = None

    elif message.text in items and current_level == 'catalog':
        selected_item = message.text
        current_level = 'subitems'
        subitems_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for subitem in items[selected_item]:
            subitems_menu.add(types.KeyboardButton(subitem))
        subitems_menu.add(types.KeyboardButton('🔙 Назад'))
        bot.send_message(message.chat.id, f"Категория: {selected_item}. Выберите товар:", reply_markup=subitems_menu)

    elif selected_item and message.text in items[selected_item] and current_level == 'subitems':
        selected_subitem = message.text
        current_level = 'item'
        item_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_menu.add(types.KeyboardButton('🛒 Заказать'))
        item_menu.add(types.KeyboardButton('🔙 Назад'))
        bot.send_message(message.chat.id, items[selected_item][selected_subitem], reply_markup=item_menu)

    elif message.text == '🛒 Заказать':
        if selected_item and selected_subitem:
            bot.send_message(message.chat.id, f"Заказ {selected_subitem} принят. Ждите звонка!", reply_markup=main_menu)
            current_level = 'main'
        else:
            bot.send_message(message.chat.id, "Пожалуйста, выберите товар из каталога.")

    elif message.text == '📞 Связаться с оператором':
        is_contacting_operator = True
        bot.send_message(message.chat.id, "Ваш запрос в обработке. Ждите звонка!", reply_markup=main_menu)
        current_level = 'main'

    elif message.text == '🛒 Оформить заказ':
        is_ordering = True
        bot.send_message(message.chat.id, "Пожалуйста, напишите, что хотите заказать.", reply_markup=main_menu)
        current_level = 'main'

    elif message.text == '❓ Помощь':
        bot.send_message(message.chat.id, "Как мы можем вам помочь?", reply_markup=main_menu)

    elif message.text == '🔙 Назад':
        if current_level == 'item':
            current_level = 'subitems'
            subitems_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
            for subitem in items[selected_item]:
                subitems_menu.add(types.KeyboardButton(subitem))
            subitems_menu.add(types.KeyboardButton('🔙 Назад'))
            bot.send_message(message.chat.id, "Вы вернулись к выбору товаров.", reply_markup=subitems_menu)
        elif current_level == 'subitems':
            current_level = 'catalog'
            bot.send_message(message.chat.id, "Вы вернулись к выбору категорий.", reply_markup=catalog_menu)
        elif current_level == 'catalog':
            current_level = 'main'
            bot.send_message(message.chat.id, "Вы вернулись в главное меню.", reply_markup=main_menu)
        else:
            bot.send_message(message.chat.id, "Вы уже в главном меню.", reply_markup=main_menu)
            current_level = 'main'

    else:
        if is_ordering or is_contacting_operator:
            bot.send_message(message.chat.id, "Ваш запрос в обработке. Ждите звонка!")
        else:
            bot.send_message(message.chat.id, "Неизвестная команда. Используйте кнопки меню.", reply_markup=main_menu)


def save_order(order_details):
    with open("orders.txt", "a") as file:
        file.write(order_details + "\n")

def notify_operator(order_details):
    bot.send_message(OPERATOR_CHAT_ID, "Новый заказ:\n" + order_details)
    

bot.polling(none_stop=True)
