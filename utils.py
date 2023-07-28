import os
import wave
import numpy as np
from config.global_config import (
    FAIL_KEYWORDS
)


def check_fail_keywords(string):
    for keyword in FAIL_KEYWORDS:
        if keyword in string:
            return True
    return False


def get_abs_path(path: str) -> str:
    current_path = os.path.abspath(__file__)
    dir_name, file_name = os.path.split(current_path)
    return os.path.join(dir_name, path)


def convert_to_2d(data, step=10):
    return [data[i:i + step] for i in range(0, len(data), step)]


def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes}分{seconds}秒"


def save_audio_as_wav(array_buffer, filename, sample_rate=44100):
    audio_data = np.frombuffer(array_buffer, dtype=np.int16)
    with wave.open(filename, 'wb') as wav_file:
        wav_file.setnchannels(1)  # 单声道
        wav_file.setsampwidth(2)  # 16位
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.tobytes())
