# Тикет бот для дискорд + управление с помощью реакций
## Как бот работает:
1. Вы отправляете !help и бот в данную категории отсылает панель и создает канал log:

/путь/к/изображению.jpg "Подсказка"


## Шаги для запуска:
1. Загрузите python с https://www.python.org/downloads/
2. Запустите установщик.
3. Войдите в командную строку и введите следующик команды:
```
        pip
        pip install discord.py
        pip install asyncio
```
4. Перейдите на https://discordapp.com/developers/applications и создайте свое приложение, перейдите в раздел ботов и скопируйте свой токен. Поместите его в кавычки вместо TOKEN в config.py. Там же замените все желаемые смайлики(узнать информацию о смайлике можно, написав в чат \смайлик, вы получите <:emoji:emoji_id>)
5.Вернитесь в командную строку и cd (перейдите) в каталог, в который вы загрузили этот проект. Как только вы окажетесь в каталоге в командной строке, выполните следующую команд?
```
     py main.py
```
6. Успех! Если вы видите, что бот говорит, что он работает с отображением смайликами и идентификатора пользователя, вы успешно настроили бота.
