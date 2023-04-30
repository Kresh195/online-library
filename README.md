# Парсер книг с сайта [tululu.org](https://tululu.org)
Накачать сотни и тысячи книг о научной фантастике и сделать сайт,
который будет работать локально, без интернета.

# Как установить
1.Python3 должен быть уже установлен. Затем используйте `pip` (или `pip3`, если 
есть конфликт с Python2) для установки зависимостей:
```sh
pip install -r requirements.txt
```

# Аргументы
`--start_page` отвечает за номер страницы на сайте [tululu.org](https://tululu.org/l55/),
с которой мы начинаем скачивать нужные нам книги (требует после себя натуральное число).

`--end_page` отвечает за последний номер страницы, на которой программа скачает книги 
(требует после себя натуральное число).

`--dest_folder` отвечает за путь к каталогу, в который попадут книги, картинки и JSON
файл с описанием книг (требует после себя путь к папке в одиночных кавычках `'...'`).

`--json_path` отвечает за путь к каталогу, в который попадёт JSON файл с описанием книг
(требует после себя путь к папке в одиночных кавычках `'...'`).

`--skip_imgs` пропускает скачивание картинок (ничего после себя не требует).

`--skip_txt` пропускает скачивание книг (ничего после себя не требует).


# Запуск
Чтобы запустить код, следующую команду в терминале:  
- Скачать книги со страниц 1-4:
```sh
python main.py
```
Также можно использовать и комбинировать данные выше аргументы, например скачать книги со страницы 3 и 4 без обложек:
```sh
python main.py --start_page 3 --end_page 4 --skip_imgs
```

Для запуска сайта необходимо ввести в терминал:
```sh
python render_website.py
```
Если вы указывали свой путь к JSON файлу:
```sh
python render_website.py --json_path 'ваш путь'
```
Адрес вашего локального сайта: http://127.0.0.1:5500

[Пример полученного сайта](https://kresh195.github.io/online-library)


# Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков
[dvmn.org](https://dvmn.org).
 
