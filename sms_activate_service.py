from smsactivate.api import SMSActivateAPI
from smsactivateru import SmsTypes
from telethon.sync import TelegramClient
import random
import asyncio
import time
from config import *
from serialization import JsonSerializer


class SmsActivateService:
    def __init__(self, api_key: str):
        self._api = SMSActivateAPI(api_key)
        self._api.debug_mode = False

    def get_countries(self):
        return self._api.getTopCountriesByService('tg')

    def get_balance(self):
        return float(self._api.getBalance()['balance'])

    def activate_phone_number(self, country: int = 11):
        phone = None
        balance = self.get_balance()
        best_country = self._api.getPrices(
            service='tg',
            country=country
        )
        if best_country and balance >= best_country[str(country)]['tg']['cost']:
            phone = self._api.getNumber(
                service='tg',
                country=country,
            )
            self._api.setStatus(
                id=phone['activation_id'],
                status=SmsTypes.Status.SmsSent
            )
        return phone

    async def create_new_session(self, phone: dict, api_id: int, api_hash: str, proxy=None, timeout=120):
        session_name = SESSIONS_DIR + '\\' + str(phone['phone'])
        client = TelegramClient(session_name, api_id, api_hash, proxy=proxy)
        try:
            await client.connect()
            await client.send_code_request(phone['phone'])
            start_time = time.time()

            while True:
                if time.time() - start_time >= timeout:
                    await client.log_out()
                    full_session_name = SESSIONS_DIR + '\\' + str(phone['phone']) + '.session'
                    full_session_journal_name = SESSIONS_DIR + '\\' + str(phone['phone']) + '.session-journal'
                    json_session_name = SESSIONS_DIR + '\\' + str(phone['phone']) + '.json'
                    if os.path.exists(full_session_name):
                        os.remove(full_session_name)
                    if os.path.exists(json_session_name):
                        os.remove(json_session_name)
                    if os.path.exists(full_session_journal_name):
                        os.remove(full_session_journal_name)
                    self._api.setStatus(
                        id=phone['activation_id'],
                        status=SmsTypes.Status.AlreadyUsed
                    )
                    return 0

                status = self._api.getStatus(id=phone['activation_id'])
                response = self._api.activationStatus(status)
                if response['status'].split(':')[0].strip() == 'STATUS_OK':
                    code = response['status'].split(':')[1].strip()

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

                    await client.sign_up(
                        phone=str(phone['phone']),
                        code=str(code),
                        first_name=str(random_firstname),
                        last_name=str(random_lastname),
                    )

                    with open(PASSWORD_TXT_FILE, "r", encoding='utf-8') as file:
                        password_list = file.read().split("\n")
                        password_list = [i for i in password_list if i]
                    random_password = random.choice(password_list)
                    await client.edit_2fa(new_password=random_password)

                    js = JsonSerializer()
                    js.json_serialize(api_id, api_hash, phone['phone'], random_password, random_firstname, random_lastname, proxy)

                    self._api.setStatus(
                        id=phone['activation_id'],
                        status=SmsTypes.Status.End
                    )
                    return code
                await asyncio.sleep(1)
        except Exception as e:
            await client.log_out()
            full_session_name = SESSIONS_DIR + '\\' + str(phone['phone']) + '.session'
            full_session_journal_name = SESSIONS_DIR + '\\' + str(phone['phone']) + '.session-journal'
            json_session_name = SESSIONS_DIR + '\\' + str(phone['phone']) + '.json'
            if os.path.exists(full_session_name):
                os.remove(full_session_name)
            if os.path.exists(json_session_name):
                os.remove(json_session_name)
            if os.path.exists(full_session_journal_name):
                os.remove(full_session_journal_name)
            return 0

    def deactivate_phone_number(self, phone: dict):
        if phone is not None:
            self._api.setStatus(
                id=phone['activation_id'],
                status=SmsTypes.Status.AlreadyUsed
            )
