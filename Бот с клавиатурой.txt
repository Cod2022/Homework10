import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler

reply_keyboard = [['/address', '/phone'],
                  ['/site', '/work_time'],
                  ['/picture', '/close']]

markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

TOKEN = ''


def start(update, context):
    update.message.reply_text(
        "Я бот-справочник. Какая информация вам нужна?",
        reply_markup=markup
    )

def close_keyboard(update, context):
    update.message.reply_text(
        "Ok",
        reply_markup=ReplyKeyboardRemove()
    )

def help(update, context):
    update.message.reply_text(
        "Я бот справочник.")


def address(update, context):
    update.message.reply_text(
        "Адрес: 125167, г. Москва, Ленинградский проспект, д.39, стр.79 этаж 23, помещение XXXIV")


def phone(update, context):
    update.message.reply_text("Телефон: 8 (800) 555-15-40")


def picture(update, context):
    context.bot.send_photo(update.effective_chat.id, photo=open('gb.png', 'rb'))


def site(update, context):
    update.message.reply_text(
        "Сайт: https://gb.ru")


def work_time(update, context):
    update.message.reply_text(
        "Время работы: круглосуточно.")


def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("address", address))
    dp.add_handler(CommandHandler("phone", phone))
    dp.add_handler(CommandHandler("site", site))
    dp.add_handler(CommandHandler("work_time", work_time))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("close", close_keyboard))
    dp.add_handler(CommandHandler("picture", picture))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
