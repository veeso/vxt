from vxt.misc.speech_engine import (
    init_speech_engine,
    BING,
    GOOGLE,
    GOOGLE_CLOUD,
    SPHINX,
    HOUNDIFY,
    IBM,
)
from vxt.view.config import Config

import pytest

CONFIG = Config()


def test_init_speech_engine_bing():
    assert (
        CONFIG.engine
        != init_speech_engine(
            CONFIG,
            BING,
            api_key="test",
            json_credentials=None,
            client_id=None,
            client_key=None,
            username=None,
            password=None,
            keyword_entries=None,
            grammar_file=None,
        ).engine
    )


def test_init_speech_engine_bing_error():
    with pytest.raises(Exception):
        init_speech_engine(
            CONFIG,
            BING,
            api_key=None,
            json_credentials=None,
            client_id=None,
            client_key=None,
            username=None,
            password=None,
            keyword_entries=None,
            grammar_file=None,
        )


def test_init_speech_engine_google():
    assert (
        CONFIG.engine
        != init_speech_engine(
            CONFIG,
            GOOGLE,
            api_key=None,
            json_credentials=None,
            client_id=None,
            client_key=None,
            username=None,
            password=None,
            keyword_entries=None,
            grammar_file=None,
        ).engine
    )


def test_init_speech_engine_google_cloud():
    assert (
        CONFIG.engine
        != init_speech_engine(
            CONFIG,
            GOOGLE_CLOUD,
            api_key=None,
            json_credentials="omar",
            client_id=None,
            client_key=None,
            username=None,
            password=None,
            keyword_entries=None,
            grammar_file=None,
        ).engine
    )


def test_init_speech_engine_google_cloud_error():
    with pytest.raises(Exception):
        init_speech_engine(
            CONFIG,
            GOOGLE_CLOUD,
            api_key=None,
            json_credentials=None,
            client_id=None,
            client_key=None,
            username=None,
            password=None,
            keyword_entries=None,
            grammar_file=None,
        )


def test_init_speech_engine_houndify():
    assert (
        CONFIG.engine
        != init_speech_engine(
            CONFIG,
            HOUNDIFY,
            api_key=None,
            json_credentials=None,
            client_id="test",
            client_key="test",
            username=None,
            password=None,
            keyword_entries=None,
            grammar_file=None,
        ).engine
    )


def test_init_speech_engine_houndify_error():
    with pytest.raises(Exception):
        init_speech_engine(
            CONFIG,
            HOUNDIFY,
            api_key=None,
            json_credentials=None,
            client_id="test",
            client_key=None,
            username=None,
            password=None,
            keyword_entries=None,
            grammar_file=None,
        )
        init_speech_engine(
            CONFIG,
            HOUNDIFY,
            api_key=None,
            json_credentials=None,
            client_id=None,
            client_key="test",
            username=None,
            password=None,
            keyword_entries=None,
            grammar_file=None,
        )


def test_init_speech_engine_ibm():
    assert (
        CONFIG.engine
        != init_speech_engine(
            CONFIG,
            IBM,
            api_key=None,
            json_credentials=None,
            client_id=None,
            client_key=None,
            username="test",
            password="test",
            keyword_entries=None,
            grammar_file=None,
        ).engine
    )


def test_init_speech_engine_ibm_error():
    with pytest.raises(Exception):
        init_speech_engine(
            CONFIG,
            IBM,
            api_key=None,
            json_credentials=None,
            client_id=None,
            client_key=None,
            username="test",
            password=None,
            keyword_entries=None,
            grammar_file=None,
        )
        init_speech_engine(
            CONFIG,
            IBM,
            api_key=None,
            json_credentials=None,
            client_id=None,
            client_key=None,
            username=None,
            password="test",
            keyword_entries=None,
            grammar_file=None,
        )

def test_init_speech_engine_sphinx():
    assert (
        CONFIG.engine
        != init_speech_engine(
            CONFIG,
            SPHINX,
            api_key=None,
            json_credentials=None,
            client_id=None,
            client_key=None,
            username=None,
            password=None,
            keyword_entries=None,
            grammar_file=None,
        ).engine
    )
