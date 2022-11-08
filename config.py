import os
from PIL import ImageTk, Image

# region Window constants
WINDOW_TITLE = "Telegram Activator"
STATUS_LIST = ["OFF", "ON", "CONNECT", "DISCONNECT", "ERROR", "WARNING", "COMPLETE", "EXCEPTION"]
# endregion


# region Dir management constants
LOCAL_DIR = os.getcwd()
UTILS_DIR = f'{LOCAL_DIR}\\utils'
SESSIONS_DIR = f'{LOCAL_DIR}\\sessions'
LOG_DIR = f'{LOCAL_DIR}\\log'
IMG_DIR = f'{LOCAL_DIR}\\img'
PHOTOS_DIR = f'{UTILS_DIR}\\avatars'
# endregion


# region File management constants
BACKPLANE_FILE = f'{IMG_DIR}\\logo2.jpg'
ICO_FILE = f'{IMG_DIR}\\icn.ico'
API_KEYS_INI_FILE = f'{UTILS_DIR}\\api_keys.ini'
PROXY_TXT_FILE = f'{UTILS_DIR}\\socks5.txt'
LOG_FILE = f'{LOG_DIR}\\logfile.log'
API_ID_HASH_FILE = f'{UTILS_DIR}\\api_id_hash.txt'
NAMES_TXT_FILE = f'{UTILS_DIR}\\names.txt'
PASSWORD_TXT_FILE = f'{UTILS_DIR}\\password.txt'
SDK_TXT_FILE = f'{UTILS_DIR}\\sdk.txt'
APP_VERSION_TXT_FILE = f'{UTILS_DIR}\\app_version.txt'
DEVICE_TXT_FILE = f'{UTILS_DIR}\\device.txt'
LANG_PACK_TXT_FILE = f'{UTILS_DIR}\\lang_pack.txt'
# endregion


# region Color constants
COLOR_GRAY = '#B0C4DE'
COLOR_BLUE = '#003153'
# endregion


# region Bot constants
MIN_BOT_COUNT = 1
MAX_BOT_COUNT = 30
MAX_ACTIVATION_TRIES = 3
# endregion


# region Tries
MIN_TRIES_COUNT = 1
MAX_TRIES_COUNT = 90
# endregion


# region Text constants
API_ID_TEXT = 'api_id'
API_HASH_TEXT = 'api_hash'
HANDLE_LEFT_TEXT = 'sms-activate.org'
HANDLE_RIGHT_TEXT = 'simsms.org'
BALANCE_TEXT = '⭕️ Balance : '
STATUS_TEXT = '⭕️ Status : '
INFO_MESSAGE_TEXT = '⭕️ Information message ⭕️'
INPUT_SESSION_COUNT_TEXT = 'Создать (шт)'
INPUT_COUNTRY_TEXT = 'Страна'
BUTTON_CREATE_TEXT = 'Создать сессии'
BUTTON_UPDATE_TEXT = 'Обновить'
START_BALANCE = '00.00'
POSTFIX_RUB_TEXT = 'RUB'
CRITICAL_TITLE = 'Критическая ошибка'
ERROR_TITLE = 'Ошибка'
WARNING_TITLE = 'Предупреждение'
INFO_TITLE = 'Сообщение'
RANDOM_API_ID_HASH_TEXT = "Случайный api_id и api_hash"
MANUAL_REG_TEXT='Регистрация сессии вручную'
# endregion


# region API constants
API_ID = 226539
API_HASH = 'f0ff3e06e48258b5158132f8599fe34b'
# endregion


# region Logger messages constants
# Critical
UTILS_CRITICAL_MESSAGE = 'Отсутствует папка utils.'
API_KEY_CRITICAL_MESSAGE = 'Ошибка в файле с API ключами сайтов, либо файл отсутствует ({}).'.format(API_KEYS_INI_FILE)
PROXY_CRITICAL_MESSAGE = 'Ошибка в файле с Proxy, либо файл отсутствует ({}).'.format(PROXY_TXT_FILE)

# Error
SMS_ACTIVATE_BALANCE_ERROR_MESSAGE = 'Ошибка при получени баланса с сайта sms-activate.org ({}).'
SMS_ACTIVATE_COUNT_ERROR_MESSAGE = 'Ошибка при получени количества свободных номеров с сайта sms-activate.org ({}).'
SIMSMS_COUNT_ERROR_MESSAGE = 'Ошибка при получени количества свободных номеров с сайта simsms.org ({}).'
SIMSMS_BALANCE_ERROR_MESSAGE = 'Ошибка при получени баланса с сайта simsms.org ({}).'
API_ID_HASH_ERROR_MESSAGE = 'Ошибка при получении api_id и api_hash.'

# Warning
SMS_ACTIVATE_SINGLE_SESSION_WARNING_MESSAGE = '{} - возникла ошибка при создании сессии на сайте sms-activate.org ({}).'
SIMSMS_SINGLE_SESSION_WARNING_MESSAGE = '{} - возникла ошибка при создании сессии на сайте simsms.org ({}).'
ACTIVATION_TRIES_LIMIT_WARNING_MESSAGE = 'Использованы все попытки для активации номера.'

# Info
START_INFO_MESSAGE = 'Папка для лог-файла и лог-файл созданы ({}).'.format(LOG_FILE)
SESSIONS_INFO_MESSAGE = 'Папка для сессий создана ({}).'.format(SESSIONS_DIR)
SMS_ACTIVATE_CREATE_INFO_MESSAGE = 'Объект класса для работы с сайтом sms-activate.org создан.'
SIMSMS_CREATE_INFO_MESSAGE = 'Объект класса для работы с сайтом simsms.org создан.'
API_KEY_INFO_MESSAGE = 'Ключи успешно получены из файла ({}).'.format(API_KEYS_INI_FILE)
PROXY_INFO_MESSAGE = 'Proxy успешно получены из файла ({}).'.format(PROXY_TXT_FILE)
SMS_ACTIVATE_BALANCE_INFO_MESSAGE = 'Баланс с сайта sms-activate.org успешно получен.'
SIMSMS_BALANCE_INFO_MESSAGE = 'Баланс с сайта simsms.org успешно получен.'
SMS_ACTIVATE_GET_NUMBER_MESSAGE = '{} - номер успешно активирован на сервисе sms-activate.org.'
SIMSMS_GET_NUMBER_MESSAGE = '{} - номер успешно активирован на сервисе simsms.org.'
PROXY_RANDOM_INFO_MESSAGE = '{} - получен случайный Proxy.'
SMS_ACTIVATE_SINGLE_SESSION_INFO_MESSAGE = '{}.session - создана новая сессия на сайте sms-activate.org.'
SIMSMS_SINGLE_SESSION_INFO_MESSAGE = '{}.session - создана новая сессия на сайте simsms.org.'
API_ID_INFO_MESSAGE = 'Значение api_id успешно получено.'
API_HASH_INFO_MESSAGE = 'Значение api_hash успешно получено.'
SMS_ACTIVATE_AUTO_COUNTRY_INFO_MESSAGE = '{} - определена страна для покупки номера на сайте sms-activate.org.'
SIMSMS_COUNTRY_INFO_MESSAGE = '{} - определена страна для покупки номера на сайте simsms.org.'
SMS_ACTIVATE_TASKS_INFO_MESSAGE = 'Успешно запущен процесс покупки номеров на сайте sms-activate.org.'
SIMSMS_TASKS_INFO_MESSAGE = 'Успешно запущен процесс покупки номеров на сайте simsms.org.'
SMS_ACTIVATE_RUN_THREAD_INFO_MESSAGE = 'Успешно запущен поток для покупки номеров на сайте sms-activate.org.'
SIMSMS_RUN_THREAD_INFO_MESSAGE = 'Успешно запущен поток для покупки номеров на сайте simsms.org.'
SMS_ACTIVATE_RUN_INFO_MESSAGE = 'Успешно запущен процесс покупки номеров на сайте sms-activate.org.'
SIMSMS_RUN_INFO_MESSAGE = 'Успешно запущен процесс покупки номеров на сайте simsms.org.'
BOTS_COUNT_INFO_MESSAGE = 'Успешно получено количество сессий.'
DURATION_INFO_MESSAGE = 'Успешно получено значение длительности создания одной сессии.'
TIMEOUT_INFO_MESSAGE = 'Успешно получено значение таймаута после попытки создания сессии.'
MAX_TRIES_INFO_MESSAGE = 'Успешно получено значение максимального количества попыток создания сессии.'
DELETED_FAILED_SESSIONS_INFO_MESSAGE = 'Успешно удалены неудачные сессии.'
RANDOM_API_ID_HASH_INFO_MESSAGE = 'Успешно получены случайные значения для api_id и api_hash'
CHANGE_SITE_BUTTON_INFO_MESSAGE = 'Сменили сайт на {}.'
CHANGE_STYLE_BUTTON_INFO_MESSAGE = 'Сменили стиль.'

# endregion


def image(width):
    img = Image.open(BACKPLANE_FILE)
    ratio = (width / float(img.size[0]))
    height = int((float(img.size[1]) * float(ratio)))
    imag = img.resize((width, height), Image.ANTIALIAS)
    return ImageTk.PhotoImage(imag)


# region Countries
sms_activate_countries_dict = {
    "Россия": [0, 0],
    "Украина": [1, 0],
    "Казахстан": [2, 0],
    "Китай": [3, 0],
    "Филиппины": [4, 0],
    "Мьянма": [5, 0],
    "Индонезия": [6, 0],
    "Малайзия": [7, 0],
    "Кения": [8, 0],
    "Танзания": [9, 0],
    "Вьетнам": [10, 0],
    "Кыргызстан": [11, 0],
    "США (виртуальные)": [12, 0],
    "Израиль": [13, 0],
    "Гонконг": [14, 0],
    "Польша": [15, 0],
    "Англия": [16, 0],
    "Мадагаскар": [17, 0],
    "Дем. Конго": [18, 0],
    "Нигерия": [19, 0],
    "Макао": [20, 0],
    "Египет": [21, 0],
    "Индия": [22, 0],
    "Ирландия": [23, 0],
    "Камбоджа": [24, 0],
    "Лаос": [25, 0],
    "Гаити": [26, 0],
    "Кот д'Ивуар": [27, 0],
    "Гамбия": [28, 0],
    "Сербия": [29, 0],
    "Йемен": [30, 0],
    "ЮАР": [31, 0],
    "Румыния": [32, 0],
    "Колумбия": [33, 0],
    "Эстония": [34, 0],
    "Канада": [35, 0],
    "Марокко": [36, 0],
    "Гана": [37, 0],
    "Аргентина": [38, 0],
    "Узбекистан": [39, 0],
    "Камерун": [40, 0],
    "Чад": [41, 0],
    "Германия": [42, 0],
    "Литва": [43, 0],
    "Хорватия": [44, 0],
    "Швеция": [45, 0],
    "Ирак": [46, 0],
    "Нидерланды": [47, 0],
    "Латвия": [48, 0],
    "Австрия": [49, 0],
    "Беларусь": [50, 0],
    "Таиланд": [51, 0],
    "Сауд. Аравия": [52, 0],
    "Мексика": [53, 0],
    "Тайвань": [54, 0],
    "Испания": [55, 0],
    "Алжир": [56, 0],
    "Словения": [57, 0],
    "Бангладеш": [58, 0],
    "Сенегал": [59, 0],
    "Турция": [60, 0],
    "Чехия": [61, 0],
    "Шри-Ланка": [62, 0],
    "Перу": [63, 0],
    "Пакистан": [64, 0],
    "Новая Зеландия": [65, 0],
    "Гвинея": [66, 0],
    "Мали": [67, 0],
    "Венесуэла": [68, 0],
    "Эфиопия": [69, 0],
    "Монголия": [70, 0],
    "Бразилия": [71, 0],
    "Афганистан": [72, 0],
    "Уганда": [73, 0],
    "Ангола": [74, 0],
    "Кипр": [75, 0],
    "Франция": [76, 0],
    "Папуа-Новая Гвинея": [77, 0],
    "Мозамбик": [78, 0],
    "Непал": [79, 0],
    "Бельгия": [80, 0],
    "Болгария": [81, 0],
    "Венгрия": [82, 0],
    "Молдова": [83, 0],
    "Италия": [84, 0],
    "Парагвай": [85, 0],
    "Гондурас": [86, 0],
    "Тунис": [87, 0],
    "Никарагуа": [88, 0],
    "Тимор-Лесте": [89, 0],
    "Боливия": [90, 0],
    "Коста Рика": [91, 0],
    "Гватемала": [92, 0],
    "ОАЭ": [93, 0],
    "Зимбабве": [94, 0],
    "Пуэрто-Рико": [95, 0],
    "Того": [96, 0],
    "Кувейт": [97, 0],
    "Сальвадор": [98, 0],
    "Ливия": [99, 0],
    "Ямайка": [100, 0],
    "Тринидад и Тобаго": [101, 0],
    "Эквадор": [102, 0],
    "Свазиленд": [103, 0],
    "Оман": [104, 0],
    "Босния и Герцеговина": [105, 0],
    "Доминиканская Республика": [106, 0],
    "Катар": [107, 0],
    "Панама": [108, 0],
    "Мавритания": [109, 0],
    "Сьерра-Леоне": [110, 0],
    "Иордания": [111, 0],
    "Португалия": [112, 0],
    "Барбадос": [113, 0],
    "Бурунди": [114, 0],
    "Бенин": [115, 0],
    "Бруней": [116, 0],
    "Багамы": [117, 0],
    "Ботсвана": [118, 0],
    "Белиз": [119, 0],
    "ЦАР": [120, 0],
    "Доминика": [121, 0],
    "Гренада": [122, 0],
    "Грузия": [123, 0],
    "Греция": [124, 0],
    "Гвинея-Бисау": [125, 0],
    "Гайана": [126, 0],
    "Исландия": [127, 0],
    "Коморы": [128, 0],
    "Сент-Китс и Невис": [129, 0],
    "Либерия": [130, 0],
    "Лесото": [131, 0],
    "Малави": [132, 0],
    "Намибия": [133, 0],
    "Нигер": [134, 0],
    "Руанда": [135, 0],
    "Словакия": [136, 0],
    "Суринам": [137, 0],
    "Таджикистан": [138, 0],
    "Монако": [139, 0],
    "Бахрейн": [140, 0],
    "Реюньон": [141, 0],
    "Замбия": [142, 0],
    "Армения": [143, 0],
    "Сомали": [144, 0],
    "Конго": [145, 0],
    "Чили": [146, 0],
    "Буркина-Фасо": [147, 0],
    "Ливан": [148, 0],
    "Габон": [149, 0],
    "Албания": [150, 0],
    "Уругвай": [151, 0],
    "Маврикий": [152, 0],
    "Бутан": [153, 0],
    "Мальдивы": [154, 0],
    "Гваделупа": [155, 0],
    "Туркменистан": [156, 0],
    "Французская Гвиана": [157, 0],
    "Финляндия": [158, 0],
    "Сент-Люсия": [159, 0],
    "Люксембург": [160, 0],
    "Сент-Винсент и Гренадин": [161, 0],
    "Экваториальная Гвинея": [162, 0],
    "Джибути": [163, 0],
    "Антигуа и Барбуда": [164, 0],
    "Острова Кайман": [165, 0],
    "Черногория": [166, 0],
    "Дания": [167, 0],
    "Швейцария": [168, 0],
    "Норвегия": [169, 0],
    "Австралия": [170, 0],
    "Эритрея": [171, 0],
    "Южный Судан": [172, 0],
    "Сан-Томе и Принсипи": [173, 0],
    "Аруба": [174, 0],
    "Монтсеррат": [175, 0],
    "Ангилья": [176, 0],
    "Северная Македония": [177, 0],
    "Республика Сейшелы": [178, 0],
    "Новая Каледония": [179, 0],
    "Кабо-Верде": [180, 0],
    "США": [181, 0]
}
sms_activate_countries_list = [key + ' ({})'.format(value[1]) for key, value in sms_activate_countries_dict.items()]

simsms_countres_dict = {
    "Россия": ["RU", 0],
    "Канада": ["CA", 0],
    "Украина": ["UA", 0],
    "Германия": ["DE", 0],
    "Италия": ["IT", 0],
    "Казахстан": ["KZ", 0],
    "Гаити": ["HT", 0],
    "Румыния": ["RO", 0],
    "Англия": ["UK", 0],
    "Аргентина": ["AR", 0],
    "Бельгия": ["BE", 0],
    "Бос. и Герц.": ["BA", 0],
    "Бразилия": ["BR", 0],
    "Вьетнам": ["VN", 0],
    "Гонконг": ["HK", 0],
    "Доминикана": ["DO", 0],
    "Египет (Virtual)": ["EG", 0],
    "Израиль": ["IL", 0],
    "Индия": ["IN", 0],
    "Индонезия": ["ID", 0],
    "Ирландия": ["IE", 0],
    "Испания": ["ES", 0],
    "Камбоджа": ["KH", 0],
    # "Канада (Virtual)": ["CA_V", 0],
    "Кения": ["KE", 0],
    "Кипр": ["CY", 0],
    "Киргизия": ["KG", 0],
    "Китай": ["CN", 0],
    "Лаос": ["LA", 0],
    "Латвия": ["LV", 0],
    "Литва": ["LT", 0],
    "Малайзия": ["MY", 0],
    "Марокко": ["MA", 0],
    "Мексика": ["MX", 0],
    "Молдова": ["MD", 0],
    "Нигерия": ["NG", 0],
    "Нидерланды": ["NL", 0],
    "Новая Зеландия": ["NZ", 0],
    "Польша": ["PL", 0],
    "Португалия": ["PT", 0],
    "США": ["US", 0],
    "Таиланд": ["TH", 0],
    "Филиппины": ["PH", 0],
    "Финляндия": ["FI", 0],
    "Франция": ["FR", 0],
    "Хорватия": ["HR", 0],
    "Чехия": ["CZ", 0],
    "Чили": ["CL", 0],
    "Швеция": ["SE", 0],
    "Эстония": ["EE", 0],
    "ЮАР": ["ZA", 0]
}
simsms_countres_list = [key + ' ({})'.format(value[1]) for key, value in simsms_countres_dict.items()]
# endregion
