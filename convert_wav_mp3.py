import os
import subprocess

# folder_path = '3_out_bak'
folder_path = '3_audio_out'

intro_path = '0_intro/intro.mp3'  # укажите здесь путь к вашему intro.mp3

# Получаем список всех wav файлов
files = [f for f in os.listdir(folder_path) if f.endswith('.wav')]

# Конвертируем каждый файл
for file in files:
    # Получаем полный путь к исходному файлу
    wav_file = os.path.join(folder_path, file)
    # Создаем имя для нового файла, заменяя расширение на .mp3
    mp3_file = os.path.join(folder_path, os.path.splitext(file)[0] + '.mp3')
    combined_file = os.path.join(folder_path, "shveik_vanek_" + os.path.splitext(file)[0] + '.mp3')

    # Создаем и выполняем команду для конвертации
    command = f'ffmpeg -i {wav_file} -vn -ar 44100 -ac 2 -b:a 192k {mp3_file}'
    subprocess.call(command, shell=True)

    # Создаем и выполняем команду для объединения файлов
    command = f'ffmpeg -i "concat:{intro_path}|{mp3_file}" -c copy {combined_file}'
    subprocess.call(command, shell=True)