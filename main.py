from app.bot import bot
from app import commands_handler


def main():
    print("bot started")
    bot.polling()


if __name__ == '__main__':
    main()
