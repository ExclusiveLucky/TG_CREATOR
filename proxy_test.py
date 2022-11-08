import ssl
from proxy import *
from urllib3 import Retry
from requests.adapters import HTTPAdapter

URL = 'https://simsms.org/'

if __name__ == '__main__':
    socks5 = read_socks5('./utils/socks5.txt')
    random_proxy = random_proxy(socks5)
    address = f'socks5://{random_proxy[4]}:{random_proxy[5]}@{random_proxy[1]}:{random_proxy[2]}'
    proxy = {
        'http': address,
        'https': address
    }

    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    response = requests.get(
        url=URL,
        proxies=proxy,
        verify=ssl.CERT_NONE
    )
