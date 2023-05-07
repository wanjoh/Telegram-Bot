import os
from telegram.ext import ApplicationBuilder, CommandHandler

from handlers import *

from dotenv import load_dotenv
load_dotenv()


def main() -> None:

    # timeouts added because of TimedOut errors
    app = ApplicationBuilder()\
        .token(os.environ['TOKEN'])\
        .read_timeout(30)\
        .write_timeout(30)\
        .build()

    app.add_handlers([
        CommandHandler('hello', greeting), 
        CommandHandler('image', generate_image),
        CommandHandler('video', generate_video)
        ])

    app.run_polling()


if __name__ == '__main__':
    main()
