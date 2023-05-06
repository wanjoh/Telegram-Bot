import validators

from telegram import Update
from telegram.ext import ContextTypes

whitelist = ['jpg', 'png']

async def greeting(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}, what can I do for you today?')

async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) != 1:
        await send_error_mesage(update, 'Usage /image URL.')
        return
    
    url = context.args[0]
    if not validators.url(url) or url[-3:] not in whitelist:
        await send_error_mesage(update, 'URL is not valid. Supported extensions are {}'.format(', '.join(whitelist)))
        return

    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=url)

async def send_error_mesage(update: Update, msg: str) -> None:
    await update.message.reply_text('Hmm, something is wrong with that command. ' + msg)
