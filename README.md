# AI-BookNarrator-RU-YandexAPI

## Описание
AI-BookNarrator-RU-YandexAPI - это проект, который использует Yandex SpeechKit для автоматического озвучивания текста книг на русском языке.
Озвучивание книги на русском языке, на примере книги Карла Ванека "Приключения бравого солдата Швейка в русском плену"
Код, представленный в этом репозитории, предназначен для чтения текста книги, разбивки его на блоки и преобразования текста в аудио, которое затем сохраняется в формате wav.

## Начало работы
Прежде всего, вам необходимо клонировать репозиторий и установить необходимые библиотеки. Для этого выполните следующие команды в терминале:

git clone [ссылка на ваш репозиторий]
cd AI-BookNarrator-RU-YandexAPI
pip install -r requirements.txt

## Использование

Перед запуском убедитесь, что вы правильно настроили файл .env, указав там свой oauth_token и catalog_id.

Чтобы начать озвучивание книги, поместите текстовые файлы с книгой в папку `1_text_in` и запустите основной скрипт:

python yandex_book.py

Аудиофайлы будут сохранены в формате .wav в папке `3_audio_out`.

Для преобразования файлов из .wav в .mp3 используйте следующий скрипт:

python convert_wav_mp3.py

## Лицензия
MIT

## Контакты
https://github.com/tier61wro
