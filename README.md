# Check Point Network Access
Авторизация в сети через WEB страницу Check Point

## Установка

Windows `pip install git+https://github.com/Dev-Elektro/CheckPointNetworkAccess.git#egg=CheckPointNetworkAccess`

Linux, Mac `sudo pip install git+https://github.com/Dev-Elektro/CheckPointNetworkAccess.git#egg=CheckPointNetworkAccess`

## Использование

### Ручная авторизация

`check_point_network_access authorization https://checkpointserver/connect login password`

### Создание конфигурации авторизации

`check_point_network_access create_config`
