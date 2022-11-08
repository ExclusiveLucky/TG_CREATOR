import requests
import socks
import random


def read_socks5(path: str):
    with open(path, "r", encoding='utf-8') as file:
        socks5_data = file.read().split("\n")
    socks5_base = []
    for point in socks5_data:
        ip, port, login, password = point.split(":")
        socks5_base.append((socks.SOCKS5, ip, int(port), False, login, password))
    return socks5_base


def proxy_is_alive(proxy_type, proxy_ip, proxy_port, proxy_login, proxy_password):
    try:
        proxy = f'{proxy_type}://{proxy_login}:{proxy_password}@{proxy_ip}:{proxy_port}'
        _ = requests.get(
            url='https://api.ipify.org?format=json',
            proxies=dict(
                http=proxy,
                https=proxy
            )
        )
        data = True
    except Exception as e:
        data = False
    return data


def random_proxy(socks5_base):
    proxy = None
    while not proxy:
        proxy = random.choice(socks5_base)
        proxy_type = "socks5"
        proxy_ip = proxy[1]
        proxy_port = proxy[2]
        proxy_login = proxy[-2]
        proxy_password = proxy[-1]
        if not proxy_is_alive(proxy_type, proxy_ip, proxy_port, proxy_login, proxy_password):
            if proxy in socks5_base:
                socks5_base.remove(proxy)
            proxy = None
    return proxy


def test_proxy(socks5_base, proxy=None):
    if proxy:
        proxy_type, proxy_ip, proxy_port, rool, proxy_login, proxy_password = proxy
        if not proxy_is_alive('socks5', proxy_ip, proxy_port, proxy_login, proxy_password):
            return random_proxy(socks5_base)
        else:
            return proxy
    else:
        return random_proxy(socks5_base)
