# meetings

### Настройка проекта
Создайте `.env` файл в папке config
```bash
cp .env.exampe .env
```

Примените миграции
```bash
python manage.py migrate
```

Загрузите фикстуры
```bash
python manage.py loaddata fixtures.json
```
Создадутся таблицы комнат, несколько пользователей и несколько записей. В основном за 17.10.2023
Суперпользователь admin admin

Запустите проект
```bash
python manage.py runserver 127.0.0.1:8000
```
