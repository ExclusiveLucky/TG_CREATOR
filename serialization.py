import json
import random
from config import *


class JsonSerializer:
    @staticmethod
    def __random_name():
        with open(NAMES_TXT_FILE, "r", encoding='utf-8') as file:
            names_data = file.read().split("\n")
        firstnames_list = []
        lastnames_list = []
        for pair in names_data:
            firstname, lastname = pair.split(":")
            firstnames_list.append(firstname)
            lastnames_list.append(lastname)
        firstnames_list = [i for i in firstnames_list if i]
        lastnames_list = [i for i in lastnames_list if i]
        random_firstname = random.choice(firstnames_list)
        random_lastname = random.choice(lastnames_list)
        return random_firstname, random_lastname

    @staticmethod
    def __random_password():
        with open(PASSWORD_TXT_FILE, "r", encoding='utf-8') as file:
            password_list = file.read().split("\n")
            password_list = [i for i in password_list if i]
        random_password = random.choice(password_list)
        return random_password

    @staticmethod
    def __random_sdk():
        with open(SDK_TXT_FILE, "r", encoding='utf-8') as file:
            sdk_list = file.read().split("\n")
            sdk_list = [i for i in sdk_list if i]
        random_sdk = random.choice(sdk_list)
        return random_sdk

    @staticmethod
    def __random_app_version():
        with open(APP_VERSION_TXT_FILE, "r", encoding='utf-8') as file:
            app_version_list = file.read().split("\n")
            app_version_list = [i for i in app_version_list if i]
        random_app_version = random.choice(app_version_list)
        return random_app_version

    @staticmethod
    def __random_lang_pack():
        with open(LANG_PACK_TXT_FILE, "r", encoding='utf-8') as file:
            lang_pack_list = file.read().split("\n")
            lang_pack_list = [i for i in lang_pack_list if i]
        random_lang_pack = random.choice(lang_pack_list)
        return random_lang_pack

    @staticmethod
    def __random_device():
        with open(DEVICE_TXT_FILE, "r", encoding='utf-8') as file:
            device_list = file.read().split("\n")
            device_list = [i for i in device_list if i]
        random_device = random.choice(device_list)
        return random_device

    def json_serialize(self, api_id, api_hash, phone, password_2fa, firstname, lastname, proxy):
        json_session_name = SESSIONS_DIR + '\\' + str(phone) + '.json'
        with open(json_session_name, 'w', encoding='utf-8') as file:
            file.write('{\n')
            file.write("\t\"session_file\": \"{}\",\n".format(phone))
            file.write("\t\"phone\": \"{}\",\n".format(phone))
            file.write("\t\"register_time\": {},\n".format(0))
            file.write("\t\"app_id\": {},\n".format(api_id))
            file.write("\t\"app_hash\": \"{}\",\n".format(api_hash))
            file.write("\t\"sdk\": \"{}\",\n".format(self.__random_sdk()))
            file.write("\t\"app_version\": \"{}\",\n".format(self.__random_app_version()))
            file.write("\t\"device\": \"{}\",\n".format(self.__random_device()))
            file.write("\t\"lang_pack\": \"{}\",\n".format(self.__random_lang_pack()))
            file.write("\t\"proxy\": {},\n".format(json.dumps(proxy)))
            file.write("\t\"first_name\": \"{}\",\n".format(firstname))
            file.write("\t\"last_name\": \"{}\",\n".format(lastname))
            file.write("\t\"password_str\": \"{}\",\n".format(password_2fa))
            file.write("\t\"avatar\": {}\n".format('null'))
            file.write('}')