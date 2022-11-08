import json
import random
from telethon.sync import TelegramClient
import requests
import asyncio
import serialization
import time
from config import *


class SimSmsCountry:
   RU = "RU",
   CA = "CA",
   UA = "UA",
   DE = "DE",
   IT = "IT",
   KZ = "KZ",
   HT = "HT",
   RO = "RO",
   UK = "UK",
   AR = "AR",
   BE = "BE",
   BA = "BA",
   BR = "BR",
   VN = "VN",
   HK = "HK",
   DO = "DO",
   EG = "EG",
   IL = "IL",
   IN = "IN",
   ID = "ID",
   IE = "IE",
   ES = "ES",
   KH = "KH",
   CA_V = "CA_V",
   KE = "KE",
   CY = "CY",
   KG = "KG",
   CN = "CN",
   LA = "LA",
   LV = "LV",
   LT = "LT",
   MY = "MY",
   MA = "MA",
   MX = "MX",
   MD = "MD",
   NG = "NG",
   NL = "NL",
   NZ = "NZ",
   PL = "PL",
   PT = "PT",
   US = "US",
   TH = "TH",
   PH = "PH",
   FI = "FI",
   FR = "FR",
   HR = "HR",
   CZ = "CZ",
   CL = "CL",
   SE = "SE",
   EE = "EE",
   ZA = "ZA",


class SimSmsService:
    def __init__(self, api_key: str):
        self._api_key = api_key
        self._service = 'opt29'
        self._address = 'http://simsms.org/priemnik.php'

    @staticmethod
    def __request(method: str, address: str, params: dict):
        request = requests.request(method=method, url=address, params=params)
        return json.loads(request.text)

    def __get_count_new(self, country: str = None):
        if country is None:
            params = {
                'method': 'get_count_new',
                'service': self._service,
                'apikey': self._api_key,
            }
        else:
            params = {
                'method': 'get_count_new',
                'service': self._service,
                'apikey': self._api_key,
                'country': country
            }
        get_count_new_request = self.__request(
            method='GET',
            address=self._address,
            params=params
        )
        return get_count_new_request

    def __get_service_price(self, country: str):
        params = {
            'metod': 'get_service_price',
            'country': country,
            'service': self._service,
            'apikey': self._api_key,
        }
        get_service_price_request = self.__request(
            method='GET',
            address=self._address,
            params=params
        )
        return get_service_price_request

    def __get_number(self, country: str):
        params = {
            'method': 'get_number',
            'country': country,
            'service': self._service,
            'apikey': self._api_key
        }
        get_number_request = self.__request(
            method='GET',
            address=self._address,
            params=params
        )
        return get_number_request

    def __get_sms(self, country: str, order_id: int):
        params = {
            'method': 'get_sms',
            'country': country,
            'service': self._service,
            'id': order_id,
            'apikey': self._api_key
        }
        get_sms_request = self.__request(
            method='GET',
            address=self._address,
            params=params
        )
        return get_sms_request

    def __denial(self, country: str, order_id: int):
        params = {
            'method': 'denial',
            'country': country,
            'service': self._service,
            'id': order_id,
            'apikey': self._api_key
        }
        denial_request = self.__request(
            method='POST',
            address=self._address,
            params=params
        )
        return denial_request

    def get_countries(self):
        countries = [attr for attr in dir(SimSmsCountry) if not callable(getattr(SimSmsCountry, attr)) and not attr.startswith("__")]
        top_countries = []
        for country in countries:
            try:
                res = self.__get_count_new(country=country)
                top_countries.append(res)
            except:
                pass
        return top_countries

    def get_balance(self):
        params = {
            'method': 'get_balance',
            'service': self._service,
            'apikey': self._api_key
        }
        balance_request_dict = self.__request(
            method='GET',
            address=self._address,
            params=params
        )
        return balance_request_dict

    def activate_phone_number(self, country: str = 'RU'):
        available_numbers_request = self.__get_count_new(country=country)
        available_numbers = available_numbers_request['total']

        phone_request = None
        if available_numbers > 0:
            number_price_request = self.__get_service_price(country=country)
            number_price = float(number_price_request['price'])

            balance_request = self.get_balance()
            balance = float(balance_request['balance'])

            if balance > number_price:
                phone_request = self.__get_number(country=country)
        return phone_request

    async def create_new_session(self, country: str, phone: dict, api_id: int, api_hash: str, proxy=None, timeout=120):
        phone_number = phone['CountryCode'] + phone['number']
        session_name = SESSIONS_DIR + '\\' + str(phone_number)
        client = TelegramClient(session_name, api_id, api_hash, proxy=proxy)
        try:
            await client.connect()
            await client.send_code_request(phone_number)
            start_time = time.time()
            while True:
                if time.time() - start_time >= timeout:
                    await client.log_out()
                    full_session_name = SESSIONS_DIR + '\\' + str(phone['number']) + '.session'
                    full_session_journal_name = SESSIONS_DIR + '\\' + str(phone['number']) + '.session-journal'
                    json_session_name = SESSIONS_DIR + '\\' + str(phone['number']) + '.json'
                    if os.path.exists(full_session_name):
                        os.remove(full_session_name)
                    if os.path.exists(json_session_name):
                        os.remove(json_session_name)
                    if os.path.exists(full_session_journal_name):
                        os.remove(full_session_journal_name)
                    self.__denial(
                        country=country,
                        order_id=phone['id']
                    )
                    return 0

                sms_request = self.__get_sms(
                    country=country,
                    order_id=phone['id']
                )
                if int(sms_request['response']) == 1:
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

                    code = sms_request['sms']
                    await client.sign_up(
                        phone=str(phone_number),
                        code=str(code),
                        first_name=str(random_firstname),
                        last_name=str(random_lastname)
                    )

                    with open(PASSWORD_TXT_FILE, "r", encoding='utf-8') as file:
                        password_list = file.read().split("\n")
                        password_list = [i for i in password_list if i]
                    random_password = random.choice(password_list)
                    await client.edit_2fa(new_password=random_password)

                    js = serialization.JsonSerializer()
                    js.json_serialize(api_id, api_hash, phone_number, random_password, random_firstname, random_lastname, proxy)

                    return code
                await asyncio.sleep(1)
        except Exception as e:
            await client.log_out()
            full_session_name = SESSIONS_DIR + '\\' + str(phone['number']) + '.session'
            full_session_journal_name = SESSIONS_DIR + '\\' + str(phone['number']) + '.session-journal'
            json_session_name = SESSIONS_DIR + '\\' + str(phone['number']) + '.json'
            if os.path.exists(full_session_name):
                os.remove(full_session_name)
            if os.path.exists(json_session_name):
                os.remove(json_session_name)
            if os.path.exists(full_session_journal_name):
                os.remove(full_session_journal_name)
            return 0

    def deactivate_phone_number(self, country: str, phone: dict):
        if phone is not None:
            self.__denial(
                country=country,
                order_id=phone['id']
            )
