import threading
import time

import schedule

from app.bot import bot
from app.price_fetcher import fetch_price

CHAT_ID_THREAD_DICT = {}
DEFAULT_MAILING_TIME = 3


def user_should_be_subscribed(func):
    def wrapper(chat_id, *args, **kwargs):
        if chat_id in CHAT_ID_THREAD_DICT:
            func(chat_id, *args, **kwargs)
            return True
        else:
            return False

    return wrapper


def user_should_not_be_subscribed(func):
    def wrapper(chat_id, *args, **kwargs):
        if chat_id not in CHAT_ID_THREAD_DICT:
            func(chat_id, *args, **kwargs)
            return True
        else:
            return False

    return wrapper


@user_should_not_be_subscribed
def subscribe(chat_id, mailing_time=DEFAULT_MAILING_TIME):
    thread = threading.Thread(target=_schedule_sending, args=(chat_id, mailing_time))
    CHAT_ID_THREAD_DICT[chat_id] = thread
    thread.start()


@user_should_be_subscribed
def unsubscribe(chat_id):
    thread = CHAT_ID_THREAD_DICT.pop(chat_id)
    thread._stop()


@user_should_be_subscribed
def change_mailing_time(chat_id, new_mailing_time):
    unsubscribe(chat_id)
    subscribe(chat_id, new_mailing_time)


def _send_price(chat_id):
    current_price = fetch_price()
    bot.send_message(chat_id, f'Sup! Current price {chat_id} {time.time()}')


def _schedule_sending(chat_id, mailing_time):
    schedule.every(mailing_time).seconds.do(_send_price, chat_id)
    while True:
        schedule.run_pending()
        time.sleep(1)
