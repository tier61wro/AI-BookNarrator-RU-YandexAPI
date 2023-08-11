import os
import re
import wave
from shutil import rmtree
from typing import List, Optional

# import nltk
# from dotenv import load_dotenv
# from nltk.tokenize import sent_tokenize
# from speechkit import Session, SpeechSynthesis

# nltk.download('punkt')
#
# load_dotenv()

from utilities import (create_session, pcm_to_wav, replace_names, synthesize_audio,
                       split_large_block, text_to_blocks, find_non_russian_words,
                       join_wav_files, extract_number)

from settings import RUSSIAN_WORDS_REGEX, IGNORED_WORDS


# Объявляем глобальные переменные буква
# поправляем ударения для имен собственных
REPLACEMENTS = {
    'Лукаш': 'Л+укаш',
}

RUSSIAN_WORDS_REGEX = "^[а-яА-ЯёЁ0-9]+$"
IGNORED_WORDS = ['sil']

# Параметры озвучивания
CHANNELS = 1
SAMPLE_WIDTH = 2
FRAME_RATE = 16000

#
# def create_session(oauth_token: str, catalog_id: str) -> Session:
#     """Создание сессии"""
#     session = Session.from_yandex_passport_oauth_token(oauth_token, catalog_id)
#     if session:
#         print("Session created successfully")
#     return session
#
#
# def synthesize_audio(session: Session, output_file: str, text: str, voice: str, format: str, sample_rate: str):
#     """Синтезирование аудио"""
#     synthesize_audio_obj = SpeechSynthesis(session)
#     print(f'Creating audio for  {len(text)} symbols block')
#     synthesize_audio_obj.synthesize(
#         output_file, text=text,
#         voice=voice, format=format, sampleRateHertz=sample_rate
#     )
#
#
# def pcm_to_wav(input_file: str, output_file: str):
#     """Конвертация PCM в WAV"""
#     with open(input_file, 'rb') as raw_file:
#         raw_audio_data = raw_file.read()
#     with wave.open(output_file, 'wb') as wav_file:
#         wav_file.setnchannels(CHANNELS)
#         wav_file.setsampwidth(SAMPLE_WIDTH)
#         wav_file.setframerate(FRAME_RATE)
#         wav_file.writeframes(raw_audio_data)
#
#
# def join_wav_files(output_file: str, *input_files: str):
#     """Объединение WAV файлов"""
#     data = []
#     for input_file in input_files:
#         with wave.open(input_file, 'rb') as wav_file:
#             data.append(wav_file.readframes(wav_file.getnframes()))
#     with wave.open(output_file, 'wb') as output_wav:
#         output_wav.setnchannels(CHANNELS)  # Моно
#         output_wav.setsampwidth(SAMPLE_WIDTH)  # 2 байта (16 бит) на сэмпл
#         output_wav.setframerate(FRAME_RATE)  # Частота дискретизации 16000 Гц
#         for d in data:
#             output_wav.writeframes(d)
#
#
# def split_large_block(text_block, max_length=800):
#     sentences = sent_tokenize(text_block)
#     blocks = []
#     current_block = ''
#
#     for sentence in sentences:
#         if len(current_block) + len(sentence) > max_length:
#             blocks.append(current_block.strip())
#             current_block = sentence
#         else:
#             current_block += ' ' + sentence
#
#     if current_block:
#         blocks.append(current_block.strip())
#
#     return blocks
#
#
# def text_to_blocks(file_in):
#     with open(file_in, 'r', encoding='utf-8') as file:
#         file_text = file.read()
#         blocks = file_text.split('\n')
#         blocks_final = []
#         current_block = ''
#
#         for bl in blocks:
#             if len(current_block) + len(bl) > 1000:
#                 if len(current_block) > 1000:
#                     sub_blocks = split_large_block(current_block)
#                     blocks_final.extend(sub_blocks)
#                 else:
#                     blocks_final.append(current_block)
#                 current_block = bl
#             else:
#                 current_block = current_block + ' ' + bl
#
#         if current_block:
#             if len(current_block) > 1000:
#                 sub_blocks = split_large_block(current_block)
#                 blocks_final.extend(sub_blocks)
#             else:
#                 blocks_final.append(current_block)
#
#         return blocks_final
#
#
# def find_non_russian_words(text: str) -> Optional[List[str]]:
#     """Поиск слов, которые не состоят только из русских букв"""
#     words = re.findall(r'\b\w+\b', text)
#     non_russian_words = [word for word in words if not re.match(RUSSIAN_WORDS_REGEX, word) and word not in IGNORED_WORDS]
#     return non_russian_words if non_russian_words else None
#
#
# def replace_names(text: str) -> str:
#     """Замена слов по заданному словарю"""
#     for old, new in REPLACEMENTS.items():
#         text = text.replace(old, new)
#     return text
#
#
# def extract_number(filename: str) -> int:
#     """Извлечение номера из имени файла"""
#     match = re.search(r'\d+', filename)
#     return int(match.group()) if match else 0  # Если номер не найден, возвращаем 0


def main():
    """Основная функция"""

    # tokens for yandex api
    oauth_token = os.getenv("OAUTH_TOKEN")
    catalog_id = os.getenv("CATALOG_ID")

    session = create_session(oauth_token, catalog_id)

    # input and output folders creation
    # text_folder = '1_text_in'
    text_folder = 'test_in'

    audio_tmp_folder = '2_audio_tmp'
    if os.path.exists(audio_tmp_folder) and os.path.isdir(audio_tmp_folder):
        rmtree(audio_tmp_folder)
    os.makedirs(audio_tmp_folder)

    audio_out_folder = '3_audio_out'
    if not os.path.exists(audio_out_folder):
        os.makedirs(audio_out_folder)

    files = os.listdir(text_folder)
    files_sorted = sorted(files, key=extract_number)

    print(files_sorted)

    for chapter_file in files_sorted:
        output_filename = f'{chapter_file}.wav'
        output_filepath = os.path.join(audio_out_folder, output_filename)
        print(f'Working with file {chapter_file}, output will be saved here: {output_filepath}')

        blocks = text_to_blocks(os.path.join(text_folder, chapter_file))

        # Заменяем слова где надо поменять ударения
        blocks = list(map(replace_names, blocks))


        # continue  # TODO delete me
        # break

        wav_files = []
        # for i in range(len(blocks)):
        for i in (0, 1):
            wav_files.append(wav_file_name := os.path.join(audio_tmp_folder, f'out{i}.wav'))
            pcm_file_name = os.path.join(audio_tmp_folder, f'out{i}_raw.pcm')
            synthesize_audio(session, pcm_file_name, blocks[i], 'ermil', 'lpcm', '16000')
            pcm_to_wav(pcm_file_name, wav_file_name)

        print('Going to join .wav files to common output file')
        join_wav_files(output_filepath, *wav_files)
        break


if __name__ == '__main__':
    main()
