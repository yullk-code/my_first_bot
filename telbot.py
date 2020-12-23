from pyowm import OWM
from pyowm.utils.config import get_default_config
from pyowm.commons.exceptions import NotFoundError
import telebot

config_dict = get_default_config()
config_dict['language'] = 'ru'
owm = OWM('621c489808648ff3a7ec124017144cb7', config_dict)
bot = telebot.TeleBot("1439067887:AAGv4mrLIlmWNYkrYmvRXEZTbaD9m4QO0jo")


@bot.message_handler(content_types=['text'])
def send_echo(message):
    try:
        mgr = owm.weather_manager()
        weather = mgr.weather_at_place(message.text).weather
        temp = weather.temperature('celsius')["temp"]

        answer = "В населённому пункте " + message.text + ", сейчас " + weather.detailed_status + "\n"
        answer += "Температура сейчас в районе " + str(temp) + "°C" + "\n\n"

        if temp < -30:
            answer += "Лучше не появляться на улице при такой температуре"
        elif temp < -20:
            answer += "На улице зима одевайся как можно сильнее, шарфик обязательно"
        elif temp < -15:
            answer += "На улице холодно, но одеваться можно в умеренном режиме. На всякий " \
                      "случай можно взять шарфик и перчатки :)"
        elif temp < -10:
            answer += "За окном достаточно тепло, для прогулки"
        elif temp < 0:
            answer += "При этой температуре замерзает вода"
        elif temp < 10:
            answer += "Можно уже достать осенние/весенние вещи и попробовать погулять в них. Но не забывай про шарфик"
        elif temp < 20:
            answer += "На улице средняя температура, поэтому шарфик можно оставить дома"
        elif temp < 25:
            answer += "За окном тепло, можно ходить в трусах"
        elif temp > 30:
            answer += "А не пора ли сходить покупаться в местном водоеме?"

        bot.send_message(message.chat.id, answer)
    except NotFoundError:
        bot.send_message(message.chat.id, 'Ошибка! Город не найден.')

    bot.polling(none_stop=True)

    input()
