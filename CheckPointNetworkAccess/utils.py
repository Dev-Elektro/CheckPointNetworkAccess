import os.path
import pathlib
import sys
from typing import List

from cryptography.fernet import Fernet


def encrypt(login: str, password: str) -> List[bytes]:
    k = Fernet.generate_key()
    f = Fernet(k)
    return [k, f.encrypt(login.encode()), f.encrypt(password.encode())]


def decrypt(data1: bytes, data2: bytes, data3: bytes) -> List[str]:
    f = Fernet(data1)
    return [f.decrypt(data2).decode(), f.decrypt(data3).decode()]


def get_data_dir() -> str:
    """
    Возвращает путь к родительскому каталогу
    где могут храниться постоянные данные приложения.

    # linux: ~/.local/share
    # macOS: ~/Library/Application Support
    # windows: C:/Users/<USER>/AppData/Roaming
    """

    home = pathlib.Path.home()

    if sys.platform.startswith("win32"):
        return os.path.join(home, "AppData/Roaming")
    elif sys.platform.startswith("linux"):
        return os.path.join(home, ".local/share")
    elif sys.platform == "darwin":
        return os.path.join(home, "Library/Application Support")
