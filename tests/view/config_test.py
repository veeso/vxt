from vxt.misc.track_fmt import TrackFmt
from vxt.speech2text.google import GoogleSpeech2TextEngine
from vxt.view.config import Config

from locale import getdefaultlocale


def test_new_config():
    locale = getdefaultlocale()[0]
    if locale is None:
        locale = "en_US"
    config = Config()
    assert isinstance(config.engine, GoogleSpeech2TextEngine)
    assert locale == config.language
    assert 500 == config.min_silence_len
    assert -16 == config.silence_threshold
    assert 500 == config.keep_silence
    assert str(TrackFmt("%t-%s.64")) == str(config.output_fmt)
    assert config.output_dir is None


def test_set_config():
    config = Config()
    config.language = "it_IT"
    assert "it_IT" == config.language
    config.min_silence_len = 100
    assert 100 == config.min_silence_len
    config.silence_threshold = -30
    assert -30 == config.silence_threshold
    config.keep_silence = 300
    assert 300 == config.keep_silence
    config.output_fmt = "%s.32"
    assert str(TrackFmt("%s.32")) == str(config.output_fmt)
    config.output_dir = "/tmp/output"
    assert "/tmp/output" == config.output_dir
