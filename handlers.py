import validators
import re

from telegram import Update
from telegram.ext import ContextTypes
from type_enum import RequestType

import yt_dlp
import json

image_whitelist = ['jpg', 'png']

MAX_DURATION = 360


async def greeting(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}, what can I do for you today?')


async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url: str | None = await check_request(update, context, RequestType.IMAGE)
    if url:
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=url)


async def generate_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url: str | None = await check_request(update, context, RequestType.VIDEO)
    if url:
        ydl_opts = {
            'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4'
            }],
            'outtmpl': {'default': './video.mp4'},
            'overwrites': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # save video information
            info = ydl.extract_info(url, download=False)
            with open('options.json', 'w') as f:
                f.write(json.dumps(ydl.sanitize_info(info)))

            # check if video is longer than MAX_DURATION
            duration = info.get('duration')
            if duration and duration > MAX_DURATION:
                await update.message.reply_text(
                    'That video is too long, only videos shorter than 5 minutes can be sent')
                return

            # download video
            error_code = ydl.download_with_info_file('options.json')

            if error_code:
                msg = 'Video failed to download'
                print(msg)
                await send_error(update, msg)
                return
            else:
                print('Video successfully downloaded')

                await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
                await context.bot.send_video(chat_id=update.effective_chat.id, video=open('video.mp4', 'rb'),
                                             supports_streaming=True)


async def check_request(update: Update, context: ContextTypes.DEFAULT_TYPE, type: RequestType) -> str | None:
    url: str | None = None
    msg: str | None = None
    if len(context.args) != 1:
        msg = "Usage: '/image URL'."
    else:
        url = context.args[0]
        match type:
            case RequestType.IMAGE:
                if not validators.url(url) or url[-3:] not in image_whitelist:
                    msg = 'URL is not valid. Supported extensions are {}'.format(', '.join(image_whitelist))
            case RequestType.VIDEO:
                if not await validate_youtube_url(url):
                    msg = 'Not a valid youtube link.'
    if msg:
        await send_error(update, msg)
        return None
    else:
        return url


async def validate_youtube_url(url) -> bool:
    regex = re.compile(r'(https?://)?(www\.)?'
                       '(youtube|youtu|youtube-nocookie)\.(com|be)/' 
                       '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
    return re.fullmatch(regex, url) is not None


async def send_error(update: Update, msg: str) -> None:
    await update.message.reply_text('Hmm, something is wrong with that command. ' + msg)
