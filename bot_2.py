import logging
import parser_2
import config
from aiogram import Bot, Dispatcher, executor, types
logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)

# url страниц которые будем парсить
url_hot = 'https://www.povarenok.ru/recipes/category/6/~'
url_soup = 'https://www.povarenok.ru/recipes/category/2/~'
url_salad = 'https://www.povarenok.ru/recipes/category/12/~'
url_snacks = 'https://www.povarenok.ru/recipes/category/15/~'
url_bake = 'https://www.povarenok.ru/recipes/category/25/~'
url_dessert = 'https://www.povarenok.ru/recipes/category/30/~'
url_last = 'https://www.povarenok.ru/recipes/category/25/~'
count = 1
pars_tab = []

keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(types.KeyboardButton('рецепты'), types.KeyboardButton('то что у вас в холодильнике'))

# Хэндлер на команду /start
@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer("Добро пожаловать, {0.first_name}!\nЯ - кулинарный бот, создан, для поиска новыx рецептов)".format(message.from_user), reply_markup=keyboard)

@dp.message_handler(content_types=['text'])
async def lalala(message):
    global pars_tab
    keyboard2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard2.add(types.KeyboardButton('🥧Выпечка'), types.KeyboardButton('🍲Бульоны и супы'),  types.KeyboardButton('🍰Десерты'))
    keyboard2.add(types.KeyboardButton('🍤Закуски'), types.KeyboardButton('🥘Горячие блюда'), types.KeyboardButton('🥗Cалаты'))
    keyboard2.add(types.KeyboardButton('назад'))
    keyboard3 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard3.add(types.KeyboardButton('Показать ещё'), types.KeyboardButton('рецепты'))
    list_pages = []
    for i in range(1,16):
        list_pages.append(str(i))
    if message.chat.type == 'private':
        global count
        if message.text == 'рецепты':
            count = 1
            await message.answer("выберите одну из котегорий",
                                 reply_markup=keyboard2)
        elif message.text == 'то что у вас в холодильнике':
            await message.answer("скоро будет доступно)")
        elif message.text == 'назад':
            await message.answer("главное меню",
                                 reply_markup=keyboard)
        elif message.text == '🍲Бульоны и супы':
            await message.answer(categories(url_soup), reply_markup=keyboard3)
            new_url(url_soup)
        elif message.text == '🥘Горячие блюда':
            await message.answer(categories(url_hot), reply_markup=keyboard3)
            new_url(url_hot)
        elif message.text == '🥗Cалаты':
            await message.answer(categories(url_salad), reply_markup=keyboard3)
            new_url(url_salad)
        elif message.text == '🍤Закуски':
            await message.answer(categories(url_snacks), reply_markup=keyboard3)
            new_url(url_snacks)
        elif message.text == '🥧Выпечка':
            await message.answer(categories(url_bake), reply_markup=keyboard3)
            new_url(url_bake)
        elif message.text == '🍰Десерты':
            await message.answer(categories(url_dessert), reply_markup=keyboard3)
            new_url(url_dessert)
        elif message.text == 'Показать ещё':
            count += 1
            list_titles, pars_tab = parser_2.parser(url_last, count)
            text_answer = 'выберите одно число: \n\n'
            for i in range(len(list_titles)):
                text_answer += str(i + 1) + ') ' + list_titles[i] + '\n'
            await message.answer(text_answer, reply_markup=keyboard3)
        elif message.text in list_pages:
            await bot.send_photo(
                message.from_user.id,
                pars_tab[int(message.text)-1]['dish_img'],
                caption='\n' +'🍳'+ pars_tab[int(message.text)-1]['caption'] + '\n' + pars_tab[int(message.text)-1]['info-item'] + '\n\n' + '📜Читать статью:' + pars_tab[int(message.text)-1]['link_product']
            )
        else:
            await message.answer('Неправильно введен запрос!!!')

# Функция, которая парсит страницу
def categories(url):
    global pars_tab
    text_answer = 'Всё что у нас есть: \n\n'
    list_titles, pars_tab = parser_2.parser(url, 1)
    for i in range(len(list_titles)):
        text_answer += str(i + 1) + ') ' + list_titles[i] + '\n'
    return text_answer

def new_url(url):
    global url_last
    url_last = url


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
