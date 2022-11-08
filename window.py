import configparser
import logging
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from ttkwidgets.autocomplete import AutocompleteCombobox
from tkinter import *
from validation import *
from proxy import *
from sms_activate_service import *
from simsms_service import *

S1_front_colour = '#80f100'
S1_back_colour = '#333333'

S2_front_colour = '#206f1a'
S2_back_colour = '#333333'

S3_front_colour = '#a8c99f'
S3_back_colour = '#333333'


class MainWindow:
    def __init__(self):
        super().__init__()

        self.confirm_success = False

        # Логгер
        is_exist = os.path.exists(LOG_DIR)
        if not is_exist:
            os.makedirs(LOG_DIR)
        logging.basicConfig(
            filename=LOG_FILE,
            level=logging.INFO,
            filemode='w',
            datefmt='%Y-%m-%d %H:%M:%S',
            format='[%(asctime)-2s] [%(levelname)-2s]: %(message)s'
        )
        logging.info(START_INFO_MESSAGE)

        # Остальные папки
        is_exist = os.path.exists(SESSIONS_DIR)
        if not is_exist:
            os.makedirs(SESSIONS_DIR)
            logging.info(SESSIONS_INFO_MESSAGE)

        is_exist = os.path.exists(UTILS_DIR)
        if not is_exist:
            messagebox.showerror(ERROR_TITLE, UTILS_CRITICAL_MESSAGE)
            logging.critical(UTILS_CRITICAL_MESSAGE)
            exit(1)

        # Информация для Telethon (api_id, api_hash)
        self.api_id = None
        self.api_hash = None

        # Информация об API ключах
        try:
            config = configparser.ConfigParser()
            config.read(API_KEYS_INI_FILE)
            self.sms_activate_api_key = config.get('api_keys', 'sms_activate_api_key')
            self.simsms_api_key = config.get('api_keys', 'simsim_api_key')
            if len(self.sms_activate_api_key) == 0 or len(self.simsms_api_key) == 0:
                raise ValueError(API_KEY_CRITICAL_MESSAGE)
            logging.info(API_KEY_INFO_MESSAGE)
        except Exception as e:
            messagebox.showerror(ERROR_TITLE, str(e))
            logging.critical(API_KEY_CRITICAL_MESSAGE)
            exit(1)

        # Объекты классов для работы с сайтами
        self.sms_activate_api = SmsActivateService(api_key=self.sms_activate_api_key)
        logging.info(SMS_ACTIVATE_CREATE_INFO_MESSAGE)
        self.simsms_api = SimSmsService(api_key=self.simsms_api_key)
        logging.info(SIMSMS_CREATE_INFO_MESSAGE)

        # Прокси
        try:
            if os.stat(PROXY_TXT_FILE).st_size == 0:
                raise ValueError(PROXY_CRITICAL_MESSAGE)
            self.socks5 = read_socks5(PROXY_TXT_FILE)
            logging.info(PROXY_INFO_MESSAGE)
        except Exception as e:
            messagebox.showerror(ERROR_TITLE, str(e))
            logging.critical(PROXY_CRITICAL_MESSAGE)
            exit(1)

        self.failed_sessions = []
        self.new_sessions = 0
        self.sessions = 0
        self.inputs_list = []
        self.labels_list = []
        self.info_labels_list = []
        self.message_base = ["", "", "", "", "", "", "", ""]
        self.message_list = []
        self.buttons_list = []

        self.window = tk.Tk()
        self.window.title(WINDOW_TITLE)
        self.window.resizable(width=False, height=False)
        self.window.iconbitmap(ICO_FILE)
        backplane = image(900)
        self.panel = tk.Label(self.window, image=backplane)
        self.panel.pack(side="top", fill="both", expand=False)

        self.front_colour = S1_front_colour
        self.back_colour = S1_back_colour
        self.create_style()

        self.site = HANDLE_LEFT_TEXT
        new_site = self.new_site(self.site)

        self.api_random = BooleanVar()
        self.api_random.set(False)
        self.manual_reg = BooleanVar()
        self.manual_reg.set(False)

        INPUT_CONFIG = [(API_ID_TEXT, 14, 20, 100, "Entry", 27, [], 130, 100, ""),
                        (API_HASH_TEXT, 14, 20, 130, "Entry", 27, [], 130, 130, ""),
                        (INPUT_SESSION_COUNT_TEXT, 14, 20, 210, "Spinbox", 25, [MIN_BOT_COUNT, MAX_BOT_COUNT], 130, 210, ""),
                        (INPUT_COUNTRY_TEXT, 14, 20, 240, "AutocompleteCombobox", 25, [], 130, 240, ""),
                        ("Время ожидания", 14, 20, 270, "Entry", 27, [], 130, 270, ""),
                        ("Таймаут", 14, 20, 300, "Entry", 27, [], 130, 300, ""),
                        ("Попытки", 14, 20, 330, "Spinbox", 25, [MIN_TRIES_COUNT, MAX_TRIES_COUNT], 130, 330, ""),
                        ("Номер телефона", 14, 20, 410, "Entry", 27, [], 130, 410, ""),
                        ("Пароль 2FA", 14, 20, 440, "Entry", 27, [], 130, 440, "")]

        self.api_random_checkbutton = tk.Checkbutton(self.window, variable=self.api_random, onvalue=True,
                                                     offvalue=False, text=RANDOM_API_ID_HASH_TEXT, width=35, bg=self.front_colour,
                                                     command=self.random_api_id_hash)
        self.api_random_checkbutton.place(x=20, y=170)
        self.inputs_list.append(self.api_random_checkbutton)

        self.manual_reg_checkbutton = tk.Checkbutton(self.window, variable=self.manual_reg, onvalue=True,
                                                     offvalue=False, text=MANUAL_REG_TEXT, width=35,
                                                     background=self.front_colour,
                                                     command=self.enable_manual_registration)
        self.manual_reg_checkbutton.place(x=20, y=370)
        self.inputs_list.append(self.manual_reg_checkbutton)

        self.inputs_list = []
        for label_text, label_width, label_x, label_y, input_type, input_width, input_values, input_x, input_y, input_insert in INPUT_CONFIG:
            label = ttk.Label(self.window, text=label_text, width=label_width)
            label.place(x=label_x, y=label_y)
            self.labels_list.append(label)
            if input_type == "Combobox":
                input_box = ttk.Combobox(self.window, width=input_width, values=input_values,
                                         background=self.back_colour, foreground=self.front_colour)
            elif input_type == "AutocompleteCombobox":
                input_box = AutocompleteCombobox(self.window, width=input_width, state='readonly',
                                                 background=self.back_colour, foreground=self.front_colour)
            elif input_type == "Spinbox":
                input_box = ttk.Spinbox(self.window, from_=input_values[0], to=input_values[1], width=input_width,
                                        background=self.back_colour, foreground=self.front_colour)
            elif input_type == 'Entry':
                input_box = tk.Entry(self.window, width=input_width,
                                     background=self.back_colour, foreground=self.front_colour)
            input_box.place(x=input_x, y=input_y)
            input_box.insert(0, input_insert)
            self.inputs_list.append(input_box)

        self.inputs_list[3].configure(completevalues=sms_activate_countries_list)
        self.inputs_list[7].config(state='disabled')
        self.labels_list[7].config(background='gray')
        self.inputs_list[7].configure(disabledbackground=self.back_colour)
        self.inputs_list[8].config(state='disabled')
        self.labels_list[8].config(background='gray')
        self.inputs_list[8].configure(disabledbackground=self.back_colour)

        INFO_CONFIG = [(self.site, 15, 360, 90),
                       (BALANCE_TEXT + START_BALANCE, 15, 360, 130),
                       (None, 15, 480, 90),
                       (None, 15, 480, 130),
                       (None, 15, 600, 90),
                       (None, 15, 600, 130),
                       (None, 15, 720, 90),
                       ("Состояние: ВЫКЛ", 15, 720, 130),
                       (None, 64, 370, 180),
                       (None, 64, 370, 221),
                       (None, 64, 370, 262),
                       (None, 64, 370, 303),
                       (None, 64, 370, 344),
                       (None, 64, 370, 385)]

        for text, width, x, y in INFO_CONFIG:
            label = ttk.Label(self.window, text=text, width=width, background='#000000', foreground=self.front_colour,
                              anchor='w')
            label.place(x=x, y=y)
            self.info_labels_list.append(label)

        BTNS_CONFIG = [(lambda: (self.update(), self.real_time_message(f"Нажали кнопку обновить для сайта {self.site}")),
                        "Обновить", self.front_colour, 10, 390, 480),
                       (self.start, "Запуск", self.front_colour, 10, 560, 480),
                       (lambda: self.configure_site(site=new_site), new_site, self.front_colour, 15, 730, 480),
                       (lambda: threading.Thread(target=self.sync_start_manual_registration).start(), 'Отправить код', self.front_colour, 38, 20, 470),
                       (self.display_information, 'Инфо', self.front_colour, 6, 20, 20),
                       (lambda: self.configure_style(S1_front_colour, 'style_1'), None, S1_front_colour, 4, 750, 20),
                       (lambda: self.configure_style(S2_front_colour, 'style_2'), None, S2_front_colour, 4, 800, 20),
                       (lambda: self.configure_style(S3_front_colour, 'style_3'), None, S3_front_colour, 4, 850, 20)]

        for command, text, colour, width, x, y in BTNS_CONFIG:
            button = Button(self.window, command=command, text=text, bg=colour, activebackground=colour, width=width)
            button.place(x=x, y=y)
            self.buttons_list.append(button)
        self.buttons_list[3].configure(state='disabled')
        self.buttons_list[3].configure(background='gray')

        self.real_time()
        self.window.mainloop()

    def display_information(self):
        self.real_time_message('Попытки - количество попыток создания одной сессии')
        self.real_time_message('Таймаут - время (в секундах) ожидания после успешного создания сессии')
        self.real_time_message('Время ожидания - время (в секундах) ожидания СМС при создании сессии')
        self.real_time_message('Страна - выбор страны для активации номера телефона')
        self.real_time_message('Создать (шт) - количество сессий, которое необходимо создать')
        self.real_time_message('api_id, api_hash - параметры подключения к Telegram API')

    def real_time(self):
        self.info_labels_list[6].configure(text=time.strftime("%d %B %H:%M:%S"), width=22)
        self.window.after(1, self.real_time)

    def real_time_message(self, message):
        for number in range(6):
            if number < 5:
                self.message_base[5 - number] = self.message_base[4 - number]
            else:
                self.message_base[0] = message
        for number in range(6):
            self.info_labels_list[number + 8].configure(text=self.message_base[number])

    def random_api_id_hash(self):
        if self.api_random.get() is True:
            self.inputs_list[0].config(state='readonly')
            self.inputs_list[0].configure(readonlybackground=self.back_colour)
            self.labels_list[0].configure(background='gray')
            self.inputs_list[1].config(state='readonly')
            self.inputs_list[1].configure(readonlybackground=self.back_colour)
            self.labels_list[1].configure(background='gray')
        else:
            self.inputs_list[0].config(state='normal')
            self.labels_list[0].configure(background=self.front_colour)
            self.inputs_list[1].config(state='normal')
            self.labels_list[1].configure(background=self.front_colour)

    def enable_manual_registration(self):
        if self.manual_reg.get() is True:
            self.inputs_list[2].config(state='readonly')
            self.inputs_list[3].config(state='disabled')
            self.inputs_list[4].config(state='readonly')
            self.inputs_list[4].configure(readonlybackground=self.back_colour)
            self.inputs_list[5].config(state='readonly')
            self.inputs_list[5].configure(readonlybackground=self.back_colour)
            self.inputs_list[6].config(state='readonly')

            for label in self.labels_list[2:-2]:
                label.configure(background='gray')
            for button in self.buttons_list[:3]:
                button.configure(state='disabled')
                button.configure(background='gray')

            self.buttons_list[3].configure(state='normal')
            self.buttons_list[3].configure(background=self.front_colour)
            self.inputs_list[7].config(state='normal')
            self.labels_list[7].config(background=self.front_colour)
            self.inputs_list[8].config(state='normal')
            self.labels_list[8].config(background=self.front_colour)
        else:
            self.api_random_checkbutton.configure(state='normal')
            self.inputs_list[2].config(state='normal')
            self.inputs_list[3].config(state='readonly')
            self.inputs_list[4].config(state='normal')
            self.inputs_list[5].config(state='normal')
            self.inputs_list[6].config(state='normal')

            for label in self.labels_list[2:-2]:
                label.configure(background=self.front_colour)
            for button in self.buttons_list[:3]:
                button.configure(state='active')
                button.configure(background=self.front_colour)

            self.buttons_list[3].configure(state='disabled')
            self.buttons_list[3].configure(background='gray')
            self.inputs_list[7].config(state='disabled')
            self.labels_list[7].config(background='gray')
            self.inputs_list[7].configure(disabledbackground=self.back_colour)
            self.inputs_list[8].config(state='disabled')
            self.labels_list[8].config(background='gray')
            self.inputs_list[8].configure(disabledbackground=self.back_colour)

    def get_random_api_id_hash(self):
        with open(API_ID_HASH_FILE, "r", encoding='utf-8') as file:
            api_id_hash_data = file.read().split("\n")
        api_id_hash_dict = {}
        for pair in api_id_hash_data:
            if ':' in pair:
                api_id, api_hash = pair.split(":")
                if api_id and api_hash:
                    api_id_hash_dict[api_id] = api_hash
        if len(api_id_hash_dict) == 0:
            raise Exception('В файле нет валидных api_id и api_hash')
        api_id, api_hash = random.choice(list(api_id_hash_dict.items()))
        if api_id is not None and api_hash is not None:
            logging.info(RANDOM_API_ID_HASH_INFO_MESSAGE)
        return api_id, api_hash

    def new_site(self, site):
        if site == HANDLE_LEFT_TEXT:
            new_site = HANDLE_RIGHT_TEXT
            if len(self.inputs_list) >= 3:
                self.inputs_list[3].set('')
                self.inputs_list[3].configure(completevalues=sms_activate_countries_list)
        else:
            new_site = HANDLE_LEFT_TEXT
            if len(self.inputs_list) >= 3:
                self.inputs_list[3].set('')
                self.inputs_list[3].configure(completevalues=simsms_countres_list)
        return new_site

    def create_style(self):
        # Сконфигурим Стиль приложения.
        STYLE_CONFIG = [(S1_front_colour, S1_back_colour, 'style_1'),
                        (S2_front_colour, S2_back_colour, 'style_2'),
                        (S3_front_colour, S3_back_colour, 'style_3')]
        self.combostyle = ttk.Style()
        for front_colour, back_colour, style_name in STYLE_CONFIG:
            self.combostyle.theme_create(style_name,
                                         parent='alt',
                                         settings={'TCombobox':
                                             {'configure':
                                                 {
                                                     'selectbackground': back_colour,
                                                     'fieldbackground': back_colour,
                                                     'foreground': front_colour,
                                                     'background': front_colour
                                                 }

                                             },
                                             'TSpinbox':
                                                 {'configure':
                                                     {
                                                         'selectbackground': back_colour,
                                                         'fieldbackground': back_colour,
                                                         'foreground': front_colour,
                                                         'background': front_colour
                                                     }

                                                 },
                                             'TEntry':
                                                 {'configure':
                                                     {
                                                         'selectbackground': back_colour,
                                                         'fieldbackground': back_colour,
                                                         'foreground': front_colour
                                                     }
                                                 },
                                             'TLabel':
                                                 {'configure':
                                                     {
                                                         'background': front_colour,
                                                         'padding': 1,
                                                         'font': ("Arial", 9)
                                                     }
                                                 },
                                             'TScrollbar':
                                                 {'configure':
                                                     {
                                                         'background': front_colour
                                                     }
                                                 }
                                         }
                                         )
        self.combostyle.theme_use('style_1')

    def configure_style(self, colour, style_name):
        self.real_time_message("Изменили стиль интерфейса")
        self.front_colour = colour

        for btn in self.buttons_list[:-3]:
            btn.configure(bg=colour, activebackground=colour)

        for label in self.info_labels_list + self.message_list:
            label.configure(foreground=colour)

        for input in self.inputs_list:
            input.configure(foreground=colour)

        self.manual_reg_checkbutton.configure(background=colour)
        self.api_random_checkbutton.configure(background=colour)

        self.combostyle.theme_use(style_name)
        self.window.update()
        logging.info(CHANGE_STYLE_BUTTON_INFO_MESSAGE)

    def configure_site(self, site):
        self.real_time_message(f"Изменили сайт на {site}")
        self.site = site
        self.info_labels_list[0].configure(text=site)
        if site == HANDLE_RIGHT_TEXT:
            site_text = HANDLE_LEFT_TEXT
        elif site == HANDLE_LEFT_TEXT:
            site_text = HANDLE_RIGHT_TEXT
        self.buttons_list[2].configure(text=site_text, command=lambda: self.configure_site(site=self.new_site(site)))
        logging.info(CHANGE_SITE_BUTTON_INFO_MESSAGE.format(self.site))
        self.update()

    def confirm_window_processing(self, client: TelegramClient, phone_number: str, password_2fa: str, proxy):
        root = tk.Tk()
        width = 300
        height = 200
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        root.geometry('%dx%d+%d+%d' % (width, height, x, y))
        root.title('Подтверждение')
        root.configure(background=self.back_colour)
        label = Label(root, text="Введите код", fg='white', width=27, background=self.back_colour)
        label.place(x=50, y=30)
        self.code_input = tk.Entry(root, width=27, background=self.back_colour, foreground=self.front_colour)
        self.code_input.place(x=70, y=70)
        button = Button(root,
                        command=lambda: self.sync_try_confirm_code(client, phone_number, password_2fa, proxy,),
                        text='Проверить код', bg=self.front_colour, activebackground=self.front_colour, width=22)
        button.place(x=70, y=110)
        self.msg_label = Label(root, fg='red', width=27, background=self.back_colour)
        self.msg_label.place(x=50, y=150)
        root.mainloop()

    def sync_try_confirm_code(self, client: TelegramClient, phone_number: str, password_2fa: str, proxy):
        logging.info(SMS_ACTIVATE_RUN_THREAD_INFO_MESSAGE)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop.run_until_complete(self.async_try_confirm_code(client, phone_number, password_2fa, proxy))
        loop.close()

    async def async_try_confirm_code(self, client: TelegramClient, phone_number: str, password_2fa: str, proxy):
        try:
            code = self.code_input.get()
            if len(code) == 0:
                self.msg_label.configure(text='Поле не должно быть пустым')
            elif not code.isdigit():
                self.msg_label.configure(text='Код должен состоять из цифр')

            with open(NAMES_TXT_FILE, "r", encoding='utf-8') as file:
                names_data = file.read().split("\n")
            firstnames_list = []
            lastnames_list = []
            for pair in names_data:
                firstname, lastname = pair.split(":")
                firstnames_list.append(firstname)
                lastnames_list.append(lastname)
            random_firstname = random.choice(firstnames_list)
            random_lastname = random.choice(lastnames_list)

            self.real_time_message('Попытка регистрации новой сессии')
            await client.sign_up(
                phone=str(phone_number),
                code=str(code),
                first_name=str(random_firstname),
                last_name=str(random_lastname)
            )
            self.real_time_message('Успешно')

            await client.edit_2fa(new_password=password_2fa)
            self.real_time_message('Успешно установлен пароль 2FA')

            js = serialization.JsonSerializer()
            js.json_serialize(self.api_id, self.api_hash, phone_number, password_2fa, random_firstname, random_lastname, proxy)
            self.real_time_message('Успешно собран JSON файл')
            self.confirm_success = True
        except Exception as e:
            self.confirm_success = False
            try:
                full_session_name = SESSIONS_DIR + '\\' + str(phone_number) + '.session'
                full_session_journal_name = SESSIONS_DIR + '\\' + str(phone_number) + '.session-journal'
                json_session_name = SESSIONS_DIR + '\\' + str(phone_number) + '.json'
                if os.path.exists(full_session_name):
                    os.remove(full_session_name)
                if os.path.exists(json_session_name):
                    os.remove(json_session_name)
                if os.path.exists(full_session_journal_name):
                    os.remove(full_session_journal_name)
                logging.info(DELETED_FAILED_SESSIONS_INFO_MESSAGE)
            except:
                pass
            logging.error('Вызвано исключение во время регистрации сессии: {}'.format(e))
            raise RuntimeError('Вызвано исключение во время регистрации сессии')

    def sync_start_manual_registration(self):
        logging.info(SMS_ACTIVATE_RUN_THREAD_INFO_MESSAGE)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop.run_until_complete(self.async_start_manual_registration())
        loop.close()

    async def async_start_manual_registration(self):
        try:
            if self.api_random.get() is False:
                self.api_id = validate_api_id(self.inputs_list[0].get())
                logging.info(API_ID_INFO_MESSAGE)
                self.api_hash = validate_api_hash(self.inputs_list[1].get())
                logging.info(API_HASH_INFO_MESSAGE)
            else:
                self.api_id, self.api_hash = self.get_random_api_id_hash()
            phone_number = validate_phone_number(self.inputs_list[7].get())
            password_2fa = validate_2fa(self.inputs_list[8].get())
            self.real_time_message('Получены номер телефона и пароль 2FA')
            logging.info('Получены номер телефона и пароль 2FA')
        except Exception as e:
            self.real_time_message('Ошибка при проверке входных параметров')
            logging.error('Ошибка при проверке входных параметров: {}'.format(e))
            return

        try:
            self.confirm_success = False
            proxy = random_proxy(self.socks5)
            self.real_time_message('Получен прокси для запроса')
            logging.info(PROXY_RANDOM_INFO_MESSAGE.format(proxy))
            session_name = SESSIONS_DIR + '\\' + str(phone_number)
            client = TelegramClient(session_name, self.api_id, self.api_hash, proxy=proxy)
            await client.connect()
            await client.send_code_request(phone=phone_number)
            self.confirm_window_processing(client, phone_number, password_2fa, proxy)
            if self.confirm_success is True:
                self.real_time_message('Сессия успешно зарегистрирована на номер {}'.format(phone_number))
            else:
                self.real_time_message('Не получилось создать сессию вручную')
        except Exception as e:
            try:
                full_session_name = SESSIONS_DIR + '\\' + str(phone_number) + '.session'
                full_session_journal_name = SESSIONS_DIR + '\\' + str(phone_number) + '.session-journal'
                json_session_name = SESSIONS_DIR + '\\' + str(phone_number) + '.json'
                if os.path.exists(full_session_name):
                    os.remove(full_session_name)
                if os.path.exists(json_session_name):
                    os.remove(json_session_name)
                if os.path.exists(full_session_journal_name):
                    os.remove(full_session_journal_name)
                logging.info(DELETED_FAILED_SESSIONS_INFO_MESSAGE)
            except:
                pass
            self.real_time_message('Ошибка при создании сессии вручную')
            logging.error('Ошибка при создании сессии вручную: {}'.format(e))

    async def async_create_single_session_left(self, api_id, api_hash, country, duration, timeout, max_tries):
        session_api = SmsActivateService(api_key=self.sms_activate_api_key)
        session_phone = None
        logging.info(SMS_ACTIVATE_CREATE_INFO_MESSAGE)
        current_try = 0
        while True:
            try:
                self.real_time_message('Попытка создания сессии...')
                if current_try == max_tries:
                    self.real_time_message(ACTIVATION_TRIES_LIMIT_WARNING_MESSAGE)
                    logging.warning(ACTIVATION_TRIES_LIMIT_WARNING_MESSAGE)
                    break
                session_phone = session_api.activate_phone_number(country=country)
                self.real_time_message('Получен номер телефона: {}'.format(session_phone['phone']))
                logging.info(SMS_ACTIVATE_GET_NUMBER_MESSAGE.format(session_phone))
                self.failed_sessions.append(session_phone)
                self.update()
                proxy = random_proxy(self.socks5)
                self.real_time_message('Получен прокси для запроса')
                logging.info(PROXY_RANDOM_INFO_MESSAGE.format(proxy))
                if api_id is None and api_hash is None:
                    api_id, api_hash = self.get_random_api_id_hash()

                self.real_time_message('Попытка получения кода для номера {}'.format(session_phone['phone']))
                code = await session_api.create_new_session(
                    phone=session_phone,
                    api_id=api_id,
                    api_hash=api_hash,
                    timeout=duration,
                    proxy=proxy,
                )
                if code != 0 and code is not None:
                    self.real_time_message('Пришел код подтверждения: {}'.format(code))
                    self.new_sessions += 1
                    if session_phone in self.failed_sessions:
                        self.failed_sessions.remove(session_phone)
                    self.real_time_message('Таймаут после успешного создания сессии ({} секунд)'.format(timeout))
                    await asyncio.sleep(timeout)
                    self.real_time_message('Таймаут истёк')
                    break
                self.real_time_message('Код не пришел на номер {}'.format(session_phone['phone']))

            except Exception as e:
                logging.warning(SMS_ACTIVATE_SINGLE_SESSION_WARNING_MESSAGE.format(session_phone, e))
                session_api.deactivate_phone_number(phone=session_phone)
                self.update()
            current_try += 1
        logging.info(SMS_ACTIVATE_SINGLE_SESSION_INFO_MESSAGE.format(session_phone))

    async def async_create_sessions_left(self):
        try:
            self.api_id, self.api_hash = None, None
            if self.api_random.get() is False:
                self.api_id = validate_api_id(self.inputs_list[0].get())
                logging.info(API_ID_INFO_MESSAGE)
                self.api_hash = validate_api_hash(self.inputs_list[1].get())
                logging.info(API_HASH_INFO_MESSAGE)
            count = validate_bots_count(self.inputs_list[2].get())
            logging.info(BOTS_COUNT_INFO_MESSAGE)
            country = sms_activate_countries_dict[self.inputs_list[3].get().split(' ')[0]][0]
            logging.info(SMS_ACTIVATE_AUTO_COUNTRY_INFO_MESSAGE.format(self.inputs_list[3].get().split(' ')[0]))
            duration = validate_timeout(self.inputs_list[4].get())
            logging.info(DURATION_INFO_MESSAGE)
            timeout = validate_timeout(self.inputs_list[5].get())
            logging.info(TIMEOUT_INFO_MESSAGE)
            max_tries = validate_tries(self.inputs_list[6].get())
            logging.info(MAX_TRIES_INFO_MESSAGE)
        except Exception as e:
            self.real_time_message("Неверные данные: {}".format(e))
            logging.error("Неверные данные: {}".format(e))
            return

        self.info_labels_list[7].configure(text="Состояние: ВКЛ")
        self.new_sessions = 0
        self.failed_sessions = []
        logging.info(SMS_ACTIVATE_TASKS_INFO_MESSAGE)
        if timeout == 0:
            tasks = [self.async_create_single_session_left(self.api_id, self.api_hash,
                                                           country, duration, timeout, max_tries) for _ in range(count)]
            await asyncio.wait(tasks)
        else:
            for _ in range(count):
                await self.async_create_single_session_left(self.api_id, self.api_hash,
                                                            country, duration, timeout, max_tries)

        self.sessions += self.new_sessions
        if self.new_sessions == 0:
            self.real_time_message('Не удалось создать сессии на сайту sms-activate.org')
        else:
            self.real_time_message("Создано {} сессий на сайте sms-activate.org. Всего - {} сессий".format(self.new_sessions, self.sessions))

        for phone in self.failed_sessions:
            try:
                full_session_name = SESSIONS_DIR + '\\' + str(phone['phone']) + '.session'
                full_session_journal_name = SESSIONS_DIR + '\\' + str(phone['phone']) + '.session-journal'
                json_session_name = SESSIONS_DIR + '\\' + str(phone['phone']) + '.json'
                if os.path.exists(full_session_name):
                    os.remove(full_session_name)
                if os.path.exists(json_session_name):
                    os.remove(json_session_name)
                if os.path.exists(full_session_journal_name):
                    os.remove(full_session_journal_name)
                # self.sms_activate_api.deactivate_phone_number(phone)
            except:
                pass
        logging.info(DELETED_FAILED_SESSIONS_INFO_MESSAGE)
        self.info_labels_list[7].configure(text="Состояние: ВЫКЛ")

    def sync_create_sessions_left(self):
        logging.info(SMS_ACTIVATE_RUN_THREAD_INFO_MESSAGE)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop.run_until_complete(self.async_create_sessions_left())
        loop.close()

    async def async_create_single_session_right(self, api_id, api_hash, country, duration, timeout, max_tries):
        session_api = SimSmsService(api_key=self.simsms_api_key)
        session_phone = None
        logging.info(SIMSMS_CREATE_INFO_MESSAGE)
        current_try = 0
        while True:
            try:
                self.real_time_message('Попытка создания сессии...')
                if current_try == max_tries:
                    self.real_time_message(ACTIVATION_TRIES_LIMIT_WARNING_MESSAGE)
                    logging.warning(ACTIVATION_TRIES_LIMIT_WARNING_MESSAGE)
                    break
                session_phone = session_api.activate_phone_number(country=country)
                self.real_time_message('Получен номер телефона: {}'.format(session_phone['number']))
                logging.info(SIMSMS_GET_NUMBER_MESSAGE.format(str(session_phone)))
                self.failed_sessions.append(session_phone)
                self.update()
                proxy = random_proxy(self.socks5)
                self.real_time_message('Получен прокси для запроса')
                logging.info(PROXY_RANDOM_INFO_MESSAGE.format(proxy))

                if api_id is None and api_hash is None:
                    api_id, api_hash = self.get_random_api_id_hash()

                self.real_time_message('Попытка получения кода для номера {}'.format(session_phone['number']))
                code = await session_api.create_new_session(
                    country=country,
                    phone=session_phone,
                    api_id=api_id,
                    api_hash=api_hash,
                    timeout=duration,
                    proxy=proxy
                )
                if code != 0 and code is not None:
                    self.real_time_message('Пришел код подтверждения: {}'.format(code))
                    self.new_sessions += 1
                    if session_phone in self.failed_sessions:
                        self.failed_sessions.remove(session_phone)
                    self.real_time_message('Таймаут после успешного создания сессии ({} секунд)'.format(timeout))
                    await asyncio.sleep(timeout)
                    self.real_time_message('Таймаут истёк')
                    break
                self.real_time_message('Код не пришел на номер {}'.format(session_phone['number']))

            except Exception as e:
                logging.warning(SIMSMS_SINGLE_SESSION_WARNING_MESSAGE.format(session_phone, e))
                session_api.deactivate_phone_number(country=country['country'], phone=session_phone)
                self.update()
            current_try += 1
        logging.info(SIMSMS_SINGLE_SESSION_INFO_MESSAGE.format(session_phone))

    async def async_create_sessions_right(self):
        try:
            self.api_id, self.api_hash = None, None
            if self.api_random.get() is False:
                self.api_id = validate_api_id(self.inputs_list[0].get())
                logging.info(API_ID_INFO_MESSAGE)
                self.api_hash = validate_api_hash(self.inputs_list[1].get())
                logging.info(API_HASH_INFO_MESSAGE)
            count = validate_bots_count(self.inputs_list[2].get())
            logging.info(BOTS_COUNT_INFO_MESSAGE)
            country = simsms_countres_dict[self.inputs_list[3].get().split(' ')[0]][0]
            logging.info(SIMSMS_COUNTRY_INFO_MESSAGE.format(country))
            duration = validate_timeout(self.inputs_list[4].get())
            logging.info(DURATION_INFO_MESSAGE)
            timeout = validate_timeout(self.inputs_list[5].get())
            logging.info(TIMEOUT_INFO_MESSAGE)
            max_tries = validate_tries(self.inputs_list[6].get())
            logging.info(MAX_TRIES_INFO_MESSAGE)
        except Exception as e:
            self.real_time_message("Неверные данные: {}".format(e))
            logging.error("Неверные данные: {}".format(e))
            return

        self.info_labels_list[7].configure(text="Состояние: ВКЛ")
        self.new_sessions = 0
        self.failed_sessions = []
        logging.info(SIMSMS_TASKS_INFO_MESSAGE)
        if timeout == 0:
            tasks = [self.async_create_single_session_right(self.api_id, self.api_hash,
                                                            country, duration, timeout, max_tries) for _ in
                     range(count)]
            await asyncio.wait(tasks)
        else:
            for _ in range(count):
                await self.async_create_single_session_right(self.api_id, self.api_hash,
                                                             country, duration, timeout, max_tries)

        self.sessions += self.new_sessions
        if self.new_sessions == 0:
            self.real_time_message('Не удалось создать сессии на сайту simsms.org')
        else:
            self.real_time_message("Создано {} сессий на сайтe simsms.org. Всего - {} сессий".format(self.new_sessions, self.sessions))

        for phone in self.failed_sessions:
            try:
                full_session_name = SESSIONS_DIR + '\\' + str(phone['number']) + '.session'
                full_session_journal_name = SESSIONS_DIR + '\\' + str(phone['number']) + '.session-journal'
                json_session_name = SESSIONS_DIR + '\\' + str(phone['number']) + '.json'
                if os.path.exists(full_session_name):
                    os.remove(full_session_name)
                if os.path.exists(json_session_name):
                    os.remove(json_session_name)
                if os.path.exists(full_session_journal_name):
                    os.remove(full_session_journal_name)
            except:
                pass
        logging.info(DELETED_FAILED_SESSIONS_INFO_MESSAGE)
        self.info_labels_list[7].configure(text="Состояние: ВЫКЛ")

    def sync_create_sessions_right(self):
        logging.info(SIMSMS_RUN_THREAD_INFO_MESSAGE)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop.run_until_complete(self.async_create_sessions_right())
        loop.close()

    def start(self):
        self.real_time_message(f"Нажали кнопку запустить для сайта {self.site}")
        if self.site == HANDLE_LEFT_TEXT:
            logging.info(SMS_ACTIVATE_RUN_INFO_MESSAGE)
            self.real_time_message('Создание сессий на сайте sms-activate.org...')
            thread = threading.Thread(target=self.sync_create_sessions_left)
            thread.start()
        elif self.site == HANDLE_RIGHT_TEXT:
            logging.info(SIMSMS_RUN_INFO_MESSAGE)
            self.real_time_message('Создание сессий на сайте simsms.org...')
            thread = threading.Thread(target=self.sync_create_sessions_right)
            thread.start()

    def update_sms_activate(self):
        try:
            balance = self.sms_activate_api.get_balance()
            self.info_labels_list[1].configure(text=(BALANCE_TEXT + str(balance) + POSTFIX_RUB_TEXT))
            logging.info(SMS_ACTIVATE_BALANCE_INFO_MESSAGE)
        except Exception as e:
            self.real_time_message(SMS_ACTIVATE_BALANCE_ERROR_MESSAGE.format(e))
            logging.error(SMS_ACTIVATE_BALANCE_ERROR_MESSAGE.format(e))

        try:
            if len(self.inputs_list) >= 3:
                self.inputs_list[3].configure(completevalues=sms_activate_countries_list)
                top_countries_dict = self.sms_activate_api.get_countries()
                for key, value in sms_activate_countries_dict.items():
                    value[1] = top_countries_dict[value[0]]['count']
                update_sms_activate_countries_list \
                    = [key + ' ({})'.format(value[1]) for key, value in sms_activate_countries_dict.items()]
                self.inputs_list[3].set_completion_list(update_sms_activate_countries_list)
        except Exception as e:
            self.real_time_message(SMS_ACTIVATE_COUNT_ERROR_MESSAGE.format(e))
            logging.error(SMS_ACTIVATE_COUNT_ERROR_MESSAGE.format(e))

    def update_simsms(self):
        try:
            balance = self.simsms_api.get_balance()['balance']
            self.info_labels_list[1].configure(text=(BALANCE_TEXT + str(balance) + POSTFIX_RUB_TEXT))
            logging.info(SIMSMS_BALANCE_INFO_MESSAGE)
        except Exception as e:
            self.real_time_message(SIMSMS_BALANCE_ERROR_MESSAGE.format(e))
            logging.error(SIMSMS_BALANCE_ERROR_MESSAGE.format(e))

        try:
            if len(self.inputs_list) >= 3:
                self.inputs_list[3].configure(completevalues=simsms_countres_list)
                top_countries_dict = self.simsms_api.get_countries()
                count = 0
                for key, value in simsms_countres_dict.items():
                    value[1] = top_countries_dict[count]['online']
                    count += 1
                update_simsms_countries_list = [key + ' ({})'.format(value[1]) for key, value in simsms_countres_dict.items()]
                self.inputs_list[3].set_completion_list(update_simsms_countries_list)
        except Exception as e:
            self.real_time_message(SIMSMS_COUNT_ERROR_MESSAGE.format(e))
            logging.error(SIMSMS_COUNT_ERROR_MESSAGE.format(e))

    def update(self):
        # self.real_time_message(f"Нажали кнопку обновить для сайта {self.site}")
        if self.site == HANDLE_LEFT_TEXT:
            thread = threading.Thread(target=self.update_sms_activate)
            thread.start()
        elif self.site == HANDLE_RIGHT_TEXT:
            thread = threading.Thread(target=self.update_simsms)
            thread.start()
