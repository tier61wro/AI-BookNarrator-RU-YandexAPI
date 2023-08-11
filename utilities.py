import os
import re
import wave
from speechkit import Session, SpeechSynthesis
import nltk
from nltk.tokenize import sent_tokenize
from settings import RUSSIAN_WORDS_REGEX, IGNORED_WORDS, CHANNELS, SAMPLE_WIDTH, FRAME_RATE
from typing import List, Optional
from settings import REPLACEMENTS

# ... [Все общие функции из book_narrator.py и find_names.py]

def create_session(oauth_token: str, catalog_id: str) -> Session:
    """Создание сессии"""
    session = Session.from_yandex_passport_oauth_token(oauth_token, catalog_id)
    if session:
        print("Session created successfully")
    return session


def synthesize_audio(session: Session, output_file: str, text: str, voice: str, format: str, sample_rate: str):
    """Синтезирование аудио"""
    synthesize_audio_obj = SpeechSynthesis(session)
    print(f'Creating audio for  {len(text)} symbols block')
    synthesize_audio_obj.synthesize(
        output_file, text=text,
        voice=voice, format=format, sampleRateHertz=sample_rate
    )


def pcm_to_wav(input_file: str, output_file: str):
    """Конвертация PCM в WAV"""
    with open(input_file, 'rb') as raw_file:
        raw_audio_data = raw_file.read()
    with wave.open(output_file, 'wb') as wav_file:
        wav_file.setnchannels(CHANNELS)
        wav_file.setsampwidth(SAMPLE_WIDTH)
        wav_file.setframerate(FRAME_RATE)
        wav_file.writeframes(raw_audio_data)


def join_wav_files(output_file: str, *input_files: str):
    """Объединение WAV файлов"""
    data = []
    for input_file in input_files:
        with wave.open(input_file, 'rb') as wav_file:
            data.append(wav_file.readframes(wav_file.getnframes()))
    with wave.open(output_file, 'wb') as output_wav:
        output_wav.setnchannels(CHANNELS)  # Моно
        output_wav.setsampwidth(SAMPLE_WIDTH)  # 2 байта (16 бит) на сэмпл
        output_wav.setframerate(FRAME_RATE)  # Частота дискретизации 16000 Гц
        for d in data:
            output_wav.writeframes(d)


def split_large_block(text_block, max_length=800):
    sentences = sent_tokenize(text_block)
    blocks = []
    current_block = ''

    for sentence in sentences:
        if len(current_block) + len(sentence) > max_length:
            blocks.append(current_block.strip())
            current_block = sentence
        else:
            current_block += ' ' + sentence

    if current_block:
        blocks.append(current_block.strip())

    return blocks


def text_to_blocks(file_in):
    with open(file_in, 'r', encoding='utf-8') as file:
        file_text = file.read()
        blocks = file_text.split('\n')
        blocks_final = []
        current_block = ''

        for bl in blocks:
            if len(current_block) + len(bl) > 1000:
                if len(current_block) > 1000:
                    sub_blocks = split_large_block(current_block)
                    blocks_final.extend(sub_blocks)
                else:
                    blocks_final.append(current_block)
                current_block = bl
            else:
                current_block = current_block + ' ' + bl

        if current_block:
            if len(current_block) > 1000:
                sub_blocks = split_large_block(current_block)
                blocks_final.extend(sub_blocks)
            else:
                blocks_final.append(current_block)

        return blocks_final


def find_non_russian_words_in_folder(folder_path: str) -> Optional[List[str]]:
    non_russian_words = ['adc']
    for file_name in sorted(os.listdir(folder_path)):
        file_path = os.path.join(folder_path, file_name)
        # print(f'{file_path}')

        # Чтение текста из файла
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()


        """Поиск слов, которые не состоят только из русских букв"""
        words = re.findall(r'\b\w+\b', text)
        non_russian_words.extend([word for word in words if not re.match(RUSSIAN_WORDS_REGEX, word) and word not in IGNORED_WORDS])

    return non_russian_words if non_russian_words else None


def replace_names(text: str) -> str:
    """Замена слов по заданному словарю"""
    for old, new in REPLACEMENTS.items():
        text = text.replace(old, new)
    return text


def extract_number(filename: str) -> int:
    """Извлечение номера из имени файла"""
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else 0  # Если номер не найден, возвращаем 0