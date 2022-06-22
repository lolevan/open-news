# open-news

Это сайт для свободного размещения Новостей 

+ Проект реализован на **Python** с использованием фреймворка **Django**.
+ Реализовал выдачу постов и также разбивку этих постов на категории благодаря **языку шаблонов Django** и **классам**
+ Сделал создание новостей и также сделал валидацию по контенту на нецензурную лексику с помощью **форм в Django**
+ Осуществил обратную связь с разработчиками благодаря пониманию **SMTP** и **форм в Django**
+ Реализовал регистрацию и авторизацию благодаря **системам аутентификации** и **формам в Django**
+ Сделал оптимизацию **SQL** запросов с помощью **Django ORM** и **Django Debug toolbar**
+ Реализовал ограничение доступа у неавторизованных пользователей с помощью миксин **LoginRequired**
+ Создал удобную админку благодаря **функционалу Django** и **CKEdior**


## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/lolevan/open-news.git
```

```
cd open-news
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv/Scripts/activate
```

или

```
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Сделать и выполнить миграции:

```
python manage.py makemigrations
```

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```

Перейти по ссылке:

```
http://127.0.0.1:8000/
```
