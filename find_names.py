import os
import re
from collections import Counter

from utilities import (create_session, find_foreign_words_in_folder, replace_names, synthesize_wav_audio)


def find_top_names_in_folder(folder_path, top_n=200):
    # Регулярное выражение для поиска имен собственных (слов, начинающихся с заглавной буквы)
    name_min_len = 4
    name_pattern = re.compile(r'(?<=[а-я]\s)\b[А-Я][а-я]{' + str(name_min_len - 1) + r',}\b')

    # Counter для подсчёта вхождений каждого имени собственного во всех файлах
    name_counts = Counter()

    # Перебор всех файлов в папке
    for file_name in sorted(os.listdir(folder_path)):
        file_path = os.path.join(folder_path, file_name)

        # Чтение текста из файла
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        # Поиск имен собственных в тексте с помощью регулярного выражения
        names = name_pattern.findall(text)

        # Обновление счетчика имен собственных для этого файла
        name_counts.update(names)

    # Получение top_n самых частых имен собственных
    top_names = name_counts.most_common(top_n)

    # Формирование результата в желаемом формате
    # result = {name: count for name, count in top_names}
    result = dict(top_names)

    return result



folder_path = '1_text_in'
top_names = find_top_names_in_folder(folder_path)

print(top_names)

name_list = []
for k in top_names.keys():
    name_list.append(f"{k}")

print(name_list)

foreign_text = find_foreign_words_in_folder(folder_path)

if foreign_text:
    print(f'ALARM: foreign_language_text {foreign_text}')

possible_wrong_names = [
                        'Лукаш',
                        ]


wrong_names_string = ' sil<[500]>'.join(possible_wrong_names)
print(wrong_names_string)

corrected_names = list(map(replace_names, possible_wrong_names))
corrected_names_string = ' sil<[500]>'.join(corrected_names)
print(corrected_names_string)


oauth_token = os.getenv("OAUTH_TOKEN")
catalog_id = os.getenv("CATALOG_ID")

session = create_session(oauth_token, catalog_id)

# pcm_file_wrong = 'names_wrong.pcm'
# wav_file_wrong = 'names_wrong.wav'
# pcm_file_ok = 'names_ok.pcm'
# wav_file_ok = 'names_ok.wav'


# synthesize_audio(session, pcm_file_wrong, wrong_names_string, 'ermil', 'lpcm', '16000')
# pcm_to_wav(pcm_file_wrong, wav_file_wrong)
#
# synthesize_audio(session, pcm_file_ok, corrected_names_string, 'ermil', 'lpcm', '16000')
# pcm_to_wav(pcm_file_ok, wav_file_ok)

synthesize_wav_audio(session, 'names_wrong.wav', wrong_names_string)
synthesize_wav_audio(session, 'names_ok.wav', corrected_names_string)

print('script work is over')
