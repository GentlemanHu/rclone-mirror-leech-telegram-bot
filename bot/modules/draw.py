import pyfirefly
from pyfirefly.utils import ImageOptions
import io
from bot import LOGGER,FIREFLY_TOKEN, Interval, QbInterval, bot, botloop, app, bot, scheduler
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

ASPECT_RATIOS = {
    'square': {
        'width': 1024,
        'height': 1024
    },
    'landscape': {
        'width': 1408,
        'height': 1024
    },
    'portrait': {
        'width': 1024,
        'height': 1408
    },
    'widescreen': {
        'width': 1792,
        'height': 1024
    }
}

token = FIREFLY_TOKEN

async def create_image(a, prompt, img_options):
    result = await a.text_to_image(prompt, **img_options)
    return result

async def handle_callback(bot, update):
    query = update
    aspect_ratio = query.data.replace('aspect_ratio_', '')  # extract ratio name
    print(aspect_ratio)
    img.set_aspect_ratio(aspect_ratio)
    result = await create_image(a, prompt, img.options)
    photo_buffer = io.BytesIO(result.image)
    photo_buffer.name = 'image.jpg'
    await bot.send_photo(
        chat_id=query.message.chat.id,
        photo=photo_buffer,
        caption=f"Generated image for prompt: {prompt}",
        reply_to_message_id=query.message.id
    )
     # delete inline keyboard
    await bot.edit_message_reply_markup(
        chat_id=query.message.chat.id,
        message_id=query.message.id,
        reply_markup=None
    )

async def draw_prompt_selection(client, message):
    if len(message.command) < 2:
        await message.reply_text('Please provide a prompt for the image.')
        return

    global prompt, a, img
    prompt = ' '.join(message.command[1:])
    a = await pyfirefly.Firefly(token)
    img = ImageOptions(image_styles=a.image_styles)
    img.add_styles(['Photo'])

    # create inline keyboard with aspect ratio options
    keyboard = [
        [InlineKeyboardButton('RatioSquare', callback_data='aspect_ratio_square')],
        [InlineKeyboardButton('Landscape', callback_data='aspect_ratio_landscape')],
        [InlineKeyboardButton('Portrait', callback_data='aspect_ratio_portrait')],
        [InlineKeyboardButton('Widescreen', callback_data='aspect_ratio_widescreen')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # ask user to select an aspect ratio
    await message.reply_text('Please select an aspect ratio:', reply_markup=reply_markup)

async def draw_image(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text('Please provide a prompt for the image.')
        return

    global prompt, a, img
    prompt = ' '.join(message.command[1:])
    a = await pyfirefly.Firefly(token)
    img = ImageOptions(image_styles=a.image_styles)
    img.add_styles(['Photo'])

    await draw_prompt_selection(client, message)

draw_handler = MessageHandler(draw_image, filters.command('draw'))
bot.add_handler(draw_handler)

callback_handler = CallbackQueryHandler(handle_callback, filters.regex(r'^aspect_ratio_'))
bot.add_handler(callback_handler)