import os

import simpleaudio as sa
from speechkit import SpeechSynthesis

from book_narrator import create_default_session

oauth_token = os.getenv("OAUTH_TOKEN")
catalog_id = os.getenv("CATALOG_ID")

session = create_default_session()
# synthesize_audio(session, pcm_file_name, blocks[i], 'ermil', 'lpcm', '16000')

text_in = 'Пошла муха на базар и купила самовар'

synthesizeAudio = SpeechSynthesis(session)
audio_data = synthesizeAudio.synthesize_stream(
    text=text_in,
    voice='ermil', format='lpcm', sampleRateHertz='16000'
)


sample_rate = 16000

play_obj = sa.play_buffer(
    audio_data,  # audio_data, полученная методом `.synthesize_stream()`
    1,  # монодорожка, один канал
    2,  # Количество байтов в секунду (16 bit = 2 bytes)
    sample_rate,  # такой же, как указали при запросе (8000, 16000, 48000)
)
play_obj.wait_done()
