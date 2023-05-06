import os
from telegram.ext import ApplicationBuilder, CommandHandler

from handlers import *

from dotenv import load_dotenv
load_dotenv()


def main() -> None:

    app = ApplicationBuilder().token(os.environ['TOKEN']).build()

    app.add_handlers([
        CommandHandler('hello', greeting), 
        CommandHandler('image', generate_image)
        ])

    app.run_polling()


if __name__ == '__main__':
    main()