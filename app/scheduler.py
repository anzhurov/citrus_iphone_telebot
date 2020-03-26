import threading
import time

import schedule

from app.bot import bot
from app.price_fetcher import fetch_price

SUBSCRIBED_CHAT_IDS = []
DEFAULT_MAILING_TIME = '10:00'


def user_should_be_subscribed(func):
    def wrapper(chat_id, *args, **kwargs):
        if chat_id in SUBSCRIBED_CHAT_IDS:
            func(chat_id, *args, **kwargs)
            return True
        else:
            return False

    return wrapper


def user_should_not_be_subscribed(func):
    def wrapper(chat_id, *args, **kwargs):
        if chat_id not in SUBSCRIBED_CHAT_IDS:
            func(chat_id, *args, **kwargs)
            return True
        else:
            return False

    return wrapper


@user_should_not_be_subscribed
def subscribe(chat_id, mailing_time=DEFAULT_MAILING_TIME):
    schedule.every().day.at(mailing_time).do(_send_price, chat_id).tag(chat_id)
    SUBSCRIBED_CHAT_IDS.append(chat_id)


@user_should_be_subscribed
def unsubscribe(chat_id):
    schedule.clear(chat_id)
    SUBSCRIBED_CHAT_IDS.remove(chat_id)


@user_should_be_subscribed
def change_mailing_time(chat_id, new_mailing_time):
    unsubscribe(chat_id)
    subscribe(chat_id, new_mailing_time)


def _send_price(chat_id):
    current_price = fetch_price()
    bot.send_message(chat_id, f'Sup! Current price {current_price} ₴')


def _start_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)


thread = threading.Thread(target=_start_scheduler)
thread.start()
