import argparse

from settings import NARRATION_COST_PER_THOUSAND, NARRATION_PRICE_URL
from utilities import (calculate_book_narration_price, create_default_session,
                       find_foreign_words_in_folder, find_top_names_in_folder,
                       replace_names, synthesize_wav_audio)

folder_path = '1_text_in'

parser = argparse.ArgumentParser(description="Find names in text and generate audio samples.")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--find_names", action="store_true", help="Find and print names from the text.")
group.add_argument("--generate_sample", action="store_true", help="Generate an audio file with names.")
group.add_argument("--calculate_price", action="store_true", help="Calculate price of book narration")

args = parser.parse_args()


if args.find_names:
    name_list = []
    top_names = find_top_names_in_folder(folder_path)

    name_list = list(top_names.keys())
    print(name_list)

    foreign_text = find_foreign_words_in_folder(folder_path)

    if foreign_text:
        print(f'ALARM: foreign_language_text {foreign_text}')


if args.generate_sample:
    # на основе первого запуска скрипта формируем массив из имен собственных которые могут звучать неправильно
    possible_wrong_names = [
        'Лукаш',
    ]

    wrong_names_string = ' sil<[500]>'.join(possible_wrong_names)

    corrected_names = list(map(replace_names, possible_wrong_names))
    corrected_names_string = ' sil<[500]>'.join(corrected_names)

    print(wrong_names_string)
    print(corrected_names_string)

    session = create_default_session()

    synthesize_wav_audio(session, 'names_wrong.wav', wrong_names_string)
    synthesize_wav_audio(session, 'names_ok.wav', corrected_names_string)

if args.calculate_price:
    price, total_symbols = calculate_book_narration_price(folder_path)
    print(f"The approximate cost of narrating your book is: {round(price, 2)} rubles")
    print(f"Your book contains {total_symbols} characters.")
    print(f"The calculation is based on the price of {NARRATION_COST_PER_THOUSAND} rubles per thousand characters.")
    print(f"Find the current price here: {NARRATION_PRICE_URL}.")

print('Script work is over')
