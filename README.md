# Веб сайт онлайн бибилиотеки

Веб сайт онлайн библиотеки, отображает информацию о книгах, скачанных с сайта tululu.org.

[Демо версия сайта](https://sanchos2.github.io/dvmn_layout_4/pages/)

### Как установить

Устанавливаем Python:
```
sudo apt install python3
sudo apt install python3-pip
```
Клонируем проект:
```
git clone https://github.com/sanchos2/dvmn_layout_4
cd dvmn_layout_4
```
Создаем виртуальное окружение, активируем его и  устанавливаем зависимости:

```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Аргументы

Параметры запуска скрипта для скачивания книг:
```
--start_page START_PAGE    Начальная страница
--end_page END_PAGE        Конечная страница
--dest_folder DEST_FOLDER  Путь к каталогу с результатами парсинга
--skip_imgs                Не скачивать картинки
--skip_txt                 Не скачивать книги
--json_path JSON_PATH      Путь к json файлу с результатами парсинга
```
В корне проекта можно создать файл .env в котором имеется возможность переопределить имя json файла
с помощью переменной JSON_FILE_NAME. Пример:
```
JSON_FILE_NAME=my_file.json
```

Конфигурация логгера содержится в файле logging.yaml и подключается в файле .env переменной LOG_CONFIG. Пример:
```
LOG_CONFIG=logging.yaml
```

Последняя страница сайта задается в .env файле
```
END_PAGE=702
```

Обязательный параметр `--start_page`, остальные опциональные.

Пример:
Будут скачаны все книги начиная с 234 страницы:
```
parse_tululu_category.py --start_page 234
```

Пример:
Будут скачаны все книги начиная с 234 страницы и заканчивая 236ой включительно:
```
parse_tululu_category.py --start_page 234 --end_page 237
```

Пример:
Будут скачаны все книги начиная с 234 страницы и заканчивая 236ой включительно, файл с описанием сохранится в /home/user/documents/library.json:
```
parse_tululu_category.py --start_page 234 --end_page 237 --json_path /home/user/documents/library.json
```

### Генерация html страниц

Для генерации html страниц необходимо запустить скрипт `render_website.py`. Страницы будут сгенерированы в директории `pages`.

Пагинация задается в файле .env следующим параметром:
```
BOOK_PER_PAGE=10
```

### Запуск бибилиотеки в оффлайн режиме

Открыть в браузере файл /pages/index.html

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).