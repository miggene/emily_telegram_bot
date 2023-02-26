import os
import re
import openai
import telebot
from dotenv import load_dotenv


def create_response(txt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f'The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: My name is Emily. I am an AI created by OpenAI. How can I help you today?\nHuman: {txt}\nAI:',
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
    )

    return response


if __name__ == '__main__':
    print('start bot')
    load_dotenv()
    BOT_TOKEN = os.environ.get('BOT_TOKEN')
    openai.api_key = os.environ.get('OPENAI_KEY')
    bot = telebot.TeleBot(BOT_TOKEN)

    # @bot.message_handler(commands=['start', 'help'])
    # def send_welcome(message):
    #     print(message)
    #     print(message.text)
    #     bot.reply_to(message, "Howdy, how are you doing?")

    @bot.message_handler(func=lambda message: True)
    def echo_all(message):
        # pattern = re.compile('@emily (\S+)')
        text = message.text
        print(f'text: {text}')
        try:
            resp = create_response(text)
            print(resp)
            ans = resp.choices[0].text
            bot.reply_to(message, ans)
        except openai.APIError as e:
            print(f'error: {e}')
            bot.reply_to(
                message, 'Please tell me something you want to know')

        # m = pattern.search(text)
        # if m is None:
        #     bot.reply_to(message, 'Please tell me something you want to know')
        # else:
        #     try:
        #         resp = create_response(text)
        #         print(resp)
        #         ans = resp.choices[0].text
        #         bot.reply_to(message, ans)
        #     except openai.APIError as e:
        #         print(f'error: {e}')
        #         bot.reply_to(
        #             message, 'Please tell me something you want to know')

    bot.infinity_polling()
