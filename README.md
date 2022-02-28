# Получение средней зарплаты для программистов в Москве

### Описание

Программа обращается к ресурсам для поиска работы [headhunter](https://hh.ru/) и [superjob](https://www.superjob.ru/). Анализ вакансий происходт по Москве для десяти самых популярных языков программирования. На выходе вы получите таблицу в следующем формате:

Superjob
|    Язык программирования | Найдено вакансий   |  Обработано вакансий |
| ------------------------ |:------------------:|----------------------|
|            python        |        1000        |           2300       |
|            java          |        700         |           2000       |

### Установка

Python должен быть установлен. Затем используйте pip (или pip3 если есть конфликт с Python2) для установки зависимостей. Затем создайте виртуальное окружение и в терминале выполните команду по установке зависимостей:

```
pip install -r requirements.txt
```

### Переменные окружения

Для доступа к ресурсе superjob необходимо получить токен авторизации, затем добавьте его в файл .env в формате

`SUPERJOB_TOKEN=ваш_токен`


