from app import validator, scheduler

from app.bot import bot
from app.price_fetcher import fetch_price


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Yoooooooo wazzzzzuuup')


@bot.message_handler(commands=['check'])
def check(message):
    current_price = fetch_price()
    bot.send_message(message.chat.id, f'Current price {current_price} ₴')


@bot.message_handler(commands=['subscribe'])
def subscribe(message):
    chat_id = message.chat.id
    result = scheduler.subscribe(chat_id)

    if result:
        bot.send_message(chat_id, 'You subscribed <3')
    else:
        bot.send_message(chat_id, 'You already subscribed')


@bot.message_handler(commands=['unsubscribe'])
def unsubscribe(message):
    chat_id = message.chat.id
    result = scheduler.unsubscribe(chat_id)

    if result:
        bot.send_message(chat_id, 'You unsubscribed')
    else:
        bot.send_message(chat_id, 'You not subscribed yet')


@bot.message_handler(commands=['changemailingtime'])
def change_sending_time(message):
    chat_id = message.chat.id

    if chat_id in scheduler.SUBSCRIBED_CHAT_IDS:
        bot.send_message(chat_id, 'When do you want to get mailing ? (Example -> 15:45)')
        bot.register_next_step_handler(message, handle_new_mailing_time)
    else:
        bot.send_message(chat_id, 'You have to subscribe first. Use /startsending')


def handle_new_mailing_time(message):
    chat_id = message.chat.id
    new_mailing_time = message.text

    if validator.is_valid_time(new_mailing_time):
        result = scheduler.change_mailing_time(chat_id, new_mailing_time)

        if result:
            bot.send_message(chat_id, f'Done! New mailing time set {new_mailing_time}')
        else:
            bot.send_message(chat_id, 'You have to subscribe first. Use /startsending')
    else:
        bot.send_message(chat_id, 'You dummy... Date invalid')
