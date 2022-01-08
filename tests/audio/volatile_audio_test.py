from vxt.audio.volatile_audio import VolatileAudio
from vxt.audio.file_audio_source import FileAudioSource
import os.path

TEST_AUDIO_PATH = os.path.join("assets", "audio", "benson.wav")


def test_volatile_audio():
    source = FileAudioSource(TEST_AUDIO_PATH)
    volatile_audio = VolatileAudio(source.audio)
    assert source.audio == volatile_audio.audio
    assert "" == volatile_audio.slug
