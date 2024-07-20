# [QRKot - Благотворительный фонд помощи котикам!=^.^=](https://github.com/elValeron/QRkot_spreadsheets.git)

## Описание: 
    - Благотворительный фонд QRKot создан для помощи котикам в столь непростое время!


## Стэк:
    - Сервис реализован на языке программирования python 3.9
    - Фреймворк - FASTApi
    - Работа с БД - SQLAlchemy
    - Миграции БД - alembic
    - Документация - Swagger
    - Генерация отчета в Google sheets - Aiogoogle

## Перед началом работы:
    - Клонировать репозиторий и перейти в него в терминале:

        ```
        - git clone https://github.com/elValeron/QRkot_spreadsheets.git
        ```

        ```
        - cd QRkot_spreadsheets
        ```

    - Cоздать и активировать виртуальное окружение:

        ```
        - python3 -m venv venv
        ```

    * Если у вас Linux/macOS

        ```
        - source venv/bin/activate
        ```

    * Если у вас windows

        ```
        - source venv/scripts/activate
        ```

    Установить зависимости из файла requirements.txt:

        ```
        - python3 -m pip install --upgrade pip
        ```

        ```
        - pip install -r requirements.txt
        ```
    В корневой директории создайте .env - файл:
        ```
        - touch .env 
        ```
        и заполните его согласно шаблону:
        ```
        APP_TITLE=<<Название приложения>>
        DATABASE_URL=<<Адрес подключения к бд>>
        SECRET=<<Секретный ключ приложения>>
        FIRST_SUPERUSER_EMAIL=<<email суперюзера>>
        FIRST_SUPERUSER_PASSWORD=<<пароль суперюзера>>
        EMAIL=<<gmail пользователя>>
        - Данные для Google cloud platform:
        TYPE=service_account
        PROJECT_ID=<<project_id>>
        PRIVATE_KEY_ID=<<private_key_id>>
        PRIVATE_KEY=<<private_key>>
        CLIENT_EMAIL=<<client_email>>
        CLIENT_ID=<<client_id>>
        AUTH_URI=<<auth_uri>>
        TOKEN_URI=<<token_uri>>
        AUTH_PROVIDER_X509_CERT_URL=<<auth_provider_x509_cert_url>>
        CLIENT_X509_CERT_URL=<<client_x509_cert_url>>
        UNIVERSE_DOMAIN=googleapis.com
        ```
    Создать базу командой: 
        ```
        - alembic upgrade head
        ```
## Работа с сервисом: 
    - Для запуска сервиса в корневой директории проекта выполните команду:
        ```
        - uvicorn app.main:app
        ```
    - После чего проект запустится и будет доступен по адресу: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

# Работа с API:
    - *Создавать благотворительные проекты может только суперюзер.
    - Для создания проекта необходимо отправить POST запрос в формате:
    ```
        {
            "name": "<Имя проекта>",
            "description": "<Описание>",
            "full_amount": <Требуемое кол-во средств>
        }
    ```
    на эндпоинт:
    ```
    - /charity_project/
    
    ```
    - после чего проект станет доступен для инвестиций. 
    - Список всех проектов можно посмотреть отправив GET запрос на эндпоинт:
    ```
    - /charity_project/
    ```
    Для создания пожертвования необходимо отправить POST запрос в формате: 
    ```
    {
        "comment": "string",
        "full_amount": 100
    }
    ```
    На эндпоинт: 
    ```
    - /donation/
    ```
    Для получения суперюзером отчета по времени закрытия проектов, необходимо отправить POST запрос на эндпоинт:
    ```
    -/google/
    ```
    После чего в аккаунте на google drive появится таблица с отчётом по закрытым проектам. 

    Подробная документация доступна по адресам:
    - Swagger:
    ```
    [http://127.0.0.1:8000/docs/](http://127.0.0.1:8000/docs/)
    ```
    - ReDoc:
    ```
    [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/)
    ```


Автор [Балашов Валерий](https://github.com/elValeron/)
