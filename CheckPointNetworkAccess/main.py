import asyncio
import configparser
import os.path
import sys
from getpass import getpass

from pyppeteer import launch
from pyppeteer.errors import TimeoutError
from loguru import logger
import argparse

from .utils import get_data_dir, encrypt, decrypt


async def authorization(url: str, login: str, password: str):
    logger.info("Start authorization Check Point")
    try:
        browser = await launch()
        page = await browser.newPage()
        await page.goto(url)
        js = """(data) => {
            document.querySelector('#LoginUserPassword_auth_username').value = data.login;
            document.querySelector('#LoginUserPassword_auth_password').value = data.password;
            }"""
        try:
            await page.waitForSelector('#LoginUserPassword_auth_password', {'visible': True})
        except TimeoutError:
            logger.error("Waiting for load page. Timeout 30000ms exceeds.")
            await browser.close()
            return False
        await page.evaluate(js, {'login': login, 'password': password})
        elem = await page.querySelector("#UserCheck_Login_Button")
        await elem.click()
        try:
            await page.waitForSelector('#nac_expiration_time > p', {'visible': True, 'timeout': 5000})
        except TimeoutError:
            obj_error_msg = await page.querySelector("#LoginUserPassword_error_message")
            logger.error(await page.evaluate('(obj) => {return obj.innerText}', obj_error_msg))
            await browser.close()
            return False
        elem = await page.querySelector("#nac_expiration_time > p")
        logger.info(await page.evaluate('(elem) => {return elem.innerText}', elem))
        await browser.close()
        return True
    except Exception as e:
        logger.error(e)


def runAuthorization(url: str, login: str, password: str):
    loop = asyncio.get_event_loop()
    for i in range(3):
        if loop.run_until_complete(authorization(url, login, password)):
            break


def create_config():
    url = input("Введите адрес страницы авторизации на Check Point: ")
    login = input("Логин: ")
    password = getpass('Пароль: ')
    password2 = getpass('Повторите пароль: ')
    if password != password2:
        return print("Пароли не совпадают.")
    patch = os.path.join(get_data_dir(), '')
    try:
        os.mkdir(patch)
    except FileExistsError:
        pass
    account = encrypt(login, password)
    config = configparser.ConfigParser()
    config['ACCOUNT'] = {
        'url': url,
        'data1': account[0].decode(),
        'data2': account[1].decode(),
        'data3': account[2].decode()
    }
    with open(os.path.join(patch, 'config.ini'), 'w') as configfile:
        config.write(configfile)
        print(f"Файл конфигурации авторизации сохранен в: {patch}")
        print(f"Для подключения вызовите {sys.argv[0]} без параметров.")


def authorization_from_config(patch: str):
    config = configparser.ConfigParser()
    config.read(patch)
    account = decrypt(config['ACCOUNT']['data1'].encode(), config['ACCOUNT']['data2'].encode(), config['ACCOUNT']['data3'].encode())
    runAuthorization(config['ACCOUNT']['url'], account[0], account[1])


def main():
    logger.remove()
    logger.add(sys.stderr, level="INFO", format="{time:YYYY-MM-DD HH:mm:ss} - {level} - {message}")
    parser = argparse.ArgumentParser(description="Check Point Network Access авторизация через web интерфейс.")

    subparsers = parser.add_subparsers()

    create_parser = subparsers.add_parser('authorization', help='Авторизация на Check Point')
    create_parser.add_argument('url', help='Адрес страницы авторизации Check Point')
    create_parser.add_argument('login', help='Логин')
    create_parser.add_argument('password', help='Пароль')
    create_parser.set_defaults(authorization=runAuthorization)

    create_parser2 = subparsers.add_parser('create_config', help='Создание конфига подключения.')
    create_parser2.set_defaults(config=create_config)

    args = parser.parse_args()

    if hasattr(args, 'authorization'):
        args.authorization(args.url, args.login, args.password)
        sys.exit(0)
    if hasattr(args, 'config'):
        args.config()
        sys.exit(0)

    path = os.path.join(os.path.join(get_data_dir(), ''), 'config.ini')
    if os.path.exists(path):
        authorization_from_config(path)
    else:
        print("Файл конфигурации подключения отсутствует.\n")
        parser.print_help()


if __name__ == '__main__':
    main()
