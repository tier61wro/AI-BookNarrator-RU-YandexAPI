import os
from shutil import rmtree

from utilities import (create_session, extract_number,
                       join_wav_files, replace_names,
                       synthesize_wav_audio, text_to_blocks)

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
            # synthesize_audio(session, pcm_file_name, blocks[i], 'ermil', 'lpcm', '16000')
            # pcm_to_wav(pcm_file_name, wav_file_name)

            synthesize_wav_audio(session, wav_file_name, blocks[i])

        print('Going to join .wav files to common output file')
        join_wav_files(output_filepath, *wav_files)
        break


if __name__ == '__main__':
    main()
