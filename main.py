import telebot
from telebot import types

API_TOKEN = "7250988138:AAFq8mJZWpHvR_C_k2Tkgq4XFmo2P6XfJ24"

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

# Описание товаров и пути к изображениям
items = {
    'Кожаные сумки': {
        'Шоппер': {
            'description': 'Описание: Высококачественная кожаная сумка для повседневного использования.',
            'image_path': '/Users/natalyalevoncuk/Desktop/images/sumka1.jpeg'
        },
        'Поясная сумка': {
            'description': 'Описание: Стильная и удобная кожаная сумка для прогулок и отдыха.',
            'image_path': '/Users/natalyalevoncuk/Desktop/images/sumka2.jpeg'
        }
    },
    'Кошельки': {
        'Зиппер': {
            'description': 'Описание: Кожаный кошелек с множеством отделений на молнии.',
            'image_path': '/Users/natalyalevoncuk/Desktop/images/koshelek1.jpeg'
        },
        'Бифолд': {
            'description': 'Описание: Компактный и стильный кожаный кошелек.',
            'image_path': '/Users/natalyalevoncuk/Desktop/images/koshelek2.jpeg'
        }
    },
    'Ремни': {
        'Брючный ремень': {
            'description': 'Описание: Прочный кожаный ремень с классической пряжкой.',
            'image_path': '/Users/natalyalevoncuk/Desktop/images/remni1.jpg'
        },
        'Ремень для джинс': {
            'description': 'Описание: Стильный кожаный ремень для повседневного использования.',
            'image_path': '/Users/natalyalevoncuk/Desktop/images/remni2.jpeg'
        }
    },
    'Браслеты': {
        'Мужской браслет': {
            'description': 'Описание: Кожаный браслет с металлическими вставками.',
            'image_path': '/Users/natalyalevoncuk/Desktop/images/braslet1.jpeg'
        },
        'Женский браслет': {
            'description': 'Описание: Стильный кожаный браслет для модных образов.',
            'image_path': '/Users/natalyalevoncuk/Desktop/images/braslet2.jpeg'
        }
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
    bot.send_message(
        message.chat.id,
        "Добро пожаловать в наш магазин изделий из кожи ручной работы!",
        reply_markup=main_menu
    )


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
        bot.send_message(
            message.chat.id,
            f"Вы выбрали категорию: {selected_item}. Выберите товар:",
            reply_markup=subitems_menu
        )

    elif selected_item and message.text in items[selected_item] and current_level == 'subitems':
        selected_subitem = message.text
        current_level = 'item'
        item_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_menu.add(types.KeyboardButton('🛒 Заказать'))
        item_menu.add(types.KeyboardButton('🔙 Назад'))
        with open(items[selected_item][selected_subitem]['image_path'], 'rb') as image:
            bot.send_photo(
                message.chat.id,
                image,
                caption=items[selected_item][selected_subitem]['description'],
                reply_markup=item_menu
            )

    elif message.text == '🛒 Заказать':
        if selected_item and selected_subitem:
            bot.send_message(
                message.chat.id,
                f"Ваш заказ на {selected_subitem.lower()} принят в обработку. "
                "Дождитесь ответа оператора для согласования заказа."
            )
            current_level = 'item'
        else:
            bot.send_message(message.chat.id, "Пожалуйста, выберите товар из каталога.")

    elif message.text == '🔙 Назад':
        if current_level == 'item':
            current_level = 'subitems'
            subitems_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
            for subitem in items[selected_item]:
                subitems_menu.add(types.KeyboardButton(subitem))
            subitems_menu.add(types.KeyboardButton('🔙 Назад'))
            bot.send_message(message.chat.id, "Выберите товар:", reply_markup=subitems_menu)
        elif current_level == 'subitems':
            current_level = 'catalog'
            bot.send_message(message.chat.id, "Выберите категорию:", reply_markup=catalog_menu)
        elif current_level == 'catalog':
            current_level = 'main'
            bot.send_message(message.chat.id, "Вы в главном меню.", reply_markup=main_menu)

    elif message.text == '📞 Связаться с оператором' and not is_contacting_operator:
        is_contacting_operator = True
        bot.send_message(
            message.chat.id,
            "Ваш запрос в обработке. Первый освободившийся оператор с вами свяжется.",
            reply_markup=main_menu
        )

    elif message.text == '🛒 Оформить заказ' and not is_ordering:
        is_ordering = True
        bot.send_message(
            message.chat.id,
            "Пожалуйста, напишите, что вы хотите заказать.",
            reply_markup=main_menu
        )

    else:
        if is_ordering or is_contacting_operator:
            bot.send_message(
                message.chat.id,
                "Ваш запрос в обработке. Дождитесь ответа оператора для согласования заказа.",
                reply_markup=main_menu
            )
        else:
            bot.send_message(
                message.chat.id,
                "Неизвестная команда. Пожалуйста, выберите опцию из меню.",
                reply_markup=main_menu
            )


# Запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True)
