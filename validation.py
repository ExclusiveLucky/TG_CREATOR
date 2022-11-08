from config import MIN_BOT_COUNT, MAX_BOT_COUNT, MIN_TRIES_COUNT, MAX_TRIES_COUNT


def validate_api_id(api_id: str):
    if not api_id.isdigit():
        raise ValueError('Неверное значение api_id')
    return int(api_id)


def validate_api_hash(api_hash: str):
    if len(api_hash) == 0:
        raise ValueError('Неверное значение api_hash')
    return api_hash


def validate_bots_count(count: str):
    if not count.isdigit():
        raise ValueError('Неверное значение количества ботов')
    elif int(count) < MIN_BOT_COUNT or int(count) > MAX_BOT_COUNT:
        raise IndexError('Выход за пределы возможных значений количества ботов')
    return int(count)


def validate_timeout(timeout: str):
    if not timeout.isdigit():
        raise ValueError('Неверное значение таймаута')
    elif int(timeout) < 0:
        raise IndexError('Выход за пределы возможных значений таймаута')
    return int(timeout)


def validate_tries(count: str):
    if not count.isdigit():
        raise ValueError('Неверное значение количества ботов')
    elif int(count) < MIN_TRIES_COUNT or int(count) > MAX_TRIES_COUNT:
        raise IndexError('Выход за пределы возможных значений количества попыток')
    return int(count)


def validate_phone_number(phone_number: str):
    if len(phone_number) == 0:
        raise ValueError('Пустой номер телефона')

    start_index = 0
    if phone_number[0] == '+':
        start_index = 1
    if not phone_number[start_index:].isdigit():
        raise ValueError('Неверный номер телефона')
    return phone_number


def validate_2fa(password: str):
    if len(password) == 0:
        raise ValueError('Пустой пароль 2FA')
    return password
