import telebot

# token бота
bot = telebot.TeleBot('5657144119:AAHwe90vP3dPGPPikpUgC1AQsjfAp_Mgfrc')

mass_dict = dict() # Словарь, в котором храняться тексты команд (ключ - название команды)
with open('base_text.txt', 'r', encoding='utf-8') as file:
    # Если flag == True, строка файла явлеется названием команды (ключем)
    flag = True 
    # Если flag == False, строка файла является текстом команды
    command_text = ""
    for stroke in file.readlines():
        if flag == True:
            key_n = stroke.strip()
            flag = False
        elif "**" in stroke.strip(): # строка с '**' означает конец текста команды
            # Добавление нового элемента в словарь, ключ - название команды
            mass_dict[key_n] = command_text
            flag = True
            command_text = ""
        else:
            command_text += stroke
    # Последняя команда не добавляется в цикле
    mass_dict[key_n] = command_text
    # Последняя команда должна обратываться отдельно, у нее 3 части разделенные "##"
    mass_dict["/category"] = mass_dict["/category"].split("##")


# Создание базовых меток для ответа
reply_base = telebot.types.ReplyKeyboardMarkup(row_width=3)
for mark in mass_dict.keys():
    reply_base.add(telebot.types.KeyboardButton(mark))

# Обработка InlineKeyboardButton
def category_inline(info, chat_id):
    reply_category = telebot.types.InlineKeyboardMarkup()
    catrep_list = ["Ежемесячно", "Раз в семестр", "Одноразово"]
    reply_category.add(telebot.types.InlineKeyboardButton("Назад", callback_data=f"{chat_id}^get^Назад"))
    for mark in catrep_list:
        if info != mark: # Строка нужна для того, чтобы бот не предлагал выбрать одну категорию 2 раза
            reply_category.add(telebot.types.InlineKeyboardButton(mark, callback_data=f"{chat_id}^get^{mark}"))
    # Ответ на query
    if info == "Назад":
        bot.send_message(chat_id, "Выберите комманду: ", reply_markup=reply_base)
    else:
        bot.send_message(chat_id, mass_dict["/category"][catrep_list.index(info)])
        bot.send_message(chat_id, "Хотите узнать о другой категории?", reply_markup=reply_category)


# Забирает callback_data из любого query
@bot.callback_query_handler(func=lambda call: True)
def rep_callback(query):
    # query.data хранит в себе строку формата f"{1}^get^{2}"
    # {1} это info[0], хранит id чата
    # {2} это info[2], хранит нужную команду
    info = query.data.split('^')
    if info[1] == "get":
        category_inline(info[2], info[0])

# Забирает комманды из перечня, ответ выводится из словаря
@bot.message_handler(commands=['start', 'mat_help', 'mat_forms', 'for_who', 'application', 'where'])
def bot_base(mess):
    bot.send_message(mess.chat.id, mass_dict[mess.text], reply_markup=reply_base)

# Забирает только команду /category
@bot.message_handler(commands=['category'])
def category(mess):
    # inline клавиатура с возможными вариантами ответа:
    reply_category = telebot.types.InlineKeyboardMarkup()
    catrep_list = ["Ежемесячно", "Раз в семестр", "Одноразово"]
    reply_category.add(telebot.types.InlineKeyboardButton("Назад", callback_data=f"{mess.chat.id}^get^Назад"))
    for mark in catrep_list:
        reply_category.add(telebot.types.InlineKeyboardButton(mark, callback_data=f"{mess.chat.id}^get^{mark}"))
    # Ответ
    bot.send_message(mess.chat.id , "Выберите интересующую категорию:", reply_markup=reply_category)


bot.polling(non_stop=True)