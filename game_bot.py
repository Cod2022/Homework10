import logging
import random

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters

reply_keyboard = [['/play', '/info', '/close']]
stop_keyboard = [['/stop']]

markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
stop_markup = ReplyKeyboardMarkup(stop_keyboard, one_time_keyboard=False)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

TOKEN = '5544320586:AAFaJ_z5clFBK6vVeUwpR0suqBeUOj84G8g'

candy = 0

def start(update, context):
    update.message.reply_text(
        "Привет! Я игровой бот! Сыграем в игру?",
        reply_markup=markup
    )

def play(update, context):
    update.message.reply_text("Введите количество конфет, необходимое для игры: ", reply_markup = stop_markup)
    return 1




def play_get_candy(update, contex):
    global candy
    try:
        candy = int(update.message.text)
        update.message.reply_text("Сколько конфет вы возьмёте?")
        return 2
    except ValueError:
        update.message.reply_text("Ошибка ввода! Введите число!")
        return 2
    

def player_1(update, context):
    global candy
    try:
        candy -= int(update.message.text)
        update.message.reply_text(f"Осталось конфет: {candy}")
        if candy > 28:
            temp = random.randint(1, 28)
            candy -= temp
            update.message.reply_text(f"Бот взял {temp} конфет")
            update.message.reply_text(f"Осталось конфет: {candy}")
            if candy > 28:
                update.message.reply_text("Сколько конфет вы возьмёте?")
            else:
                update.message.reply_text("Вы победили!", reply_markup = markup)
                context.bot.send_photo(update.effective_chat.id, photo=open('win.jpeg', 'rb'))
                return ConversationHandler.END
            return 2
        else:
            update.message.reply_text("Победил бот!", reply_markup = markup)
            context.bot.send_photo(update.effective_chat.id, photo=open('loose.jpg', 'rb'))
            return ConversationHandler.END
    except ValueError:
        update.message.reply_text("Ошибка ввода! Введите число!")
        return 2





def stop(update, context):
    update.message.reply_text("Игра окончена! Всего доброго!", reply_markup = markup)
    return ConversationHandler.END



def close(update, context):
    update.message.reply_text(
        "Спасибо за игру!",
        reply_markup=ReplyKeyboardRemove()
    )

def info(update, context):
    update.message.reply_text("Правила игры:\nВы играете против бота. По очереди каждый из вас  берёт какое-то количество конфет.\
            \nПобеждает тот, у кого в конце игры останется  больше конфет.")

play_handler = ConversationHandler(
        
        
        entry_points=[CommandHandler('play', play)],
        states={
            1: [MessageHandler(Filters.text & ~Filters.command, play_get_candy)],
            2: [MessageHandler(Filters.text & ~Filters.command, player_1)],
        },
        fallbacks=[CommandHandler('stop', stop)]
    )


def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(play_handler)
    dp.add_handler(CommandHandler("info", info))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("close", close))
    dp.add_handler(CommandHandler("stop", stop))
    
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
