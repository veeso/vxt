# VXT
# Developed by Christian Visintin
#
# MIT License
# Copyright (c) 2021 Christian Visintin
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

from .audio.file_audio_source import FileAudioSource
from .misc.speech_engine import init_speech_engine, GOOGLE
from .view.context import Context
from .view.config import Config
from .view.view import View
from .view.helper import ViewHelper

import click
from sys import exit
from typing import Optional


@click.command()
@click.option(
    "--engine",
    "-e",
    default=GOOGLE,
    help="Specify speech2text engine [bing, google, google-cloud, houndify, ibm, sphinx] (default: %s)"
    % GOOGLE,
)
@click.option(
    "--language",
    "-l",
    default=None,
    help="Specify audio language (e.g. it_IT), system language will be used otherwise",
)
@click.option(
    "--output-fmt", "-f", default="%t-%s.24", help="Specify output format (See readme)"
)
@click.option("--output-dir", "-o", default=None, help="Specify output directory")
@click.option(
    "--api-key", "-A", default=None, help="Specify api key (required for: bing, google"
)
@click.option(
    "--json-credentials",
    "-J",
    default=None,
    help="Specify json credentials (required for: google-cloud)",
)
@click.option(
    "--client-id", "-C", default=None, help="Specify client id (required for: houndify)"
)
@click.option(
    "--client-key",
    "-K",
    default=None,
    help="Specify client key (required for: houndify)",
)
@click.option(
    "--username",
    "-U",
    default=None,
    help="Specify username (required for: ibm)",
)
@click.option(
    "--password",
    "-P",
    default=None,
    help="Specify user password (required for: ibm)",
)
@click.option(
    "--keyword-entries",
    default=None,
    help="Specify keyword entries (required for: sphinx)",
)
@click.option(
    "--grammar-file",
    default=None,
    help="Specify grammar file (required for: sphinx)",
)
@click.argument("audio_source")
def main(
    engine: str,
    language: Optional[str],
    output_fmt: str,
    output_dir: Optional[str],
    api_key: Optional[str],
    json_credentials: Optional[str],
    client_id: Optional[str],
    client_key: Optional[str],
    username: Optional[str],
    password: Optional[str],
    keyword_entries: Optional[str],
    grammar_file: Optional[str],
    audio_source: str,
) -> None:
    vh = ViewHelper()
    # init config
    config = Config()
    if language:
        config.language = language
    if output_dir:
        config.output_dir = output_dir
    if output_fmt:
        config.output_fmt = output_fmt
    # make speech engine
    try:
        config = init_speech_engine(
            config,
            engine,
            api_key,
            json_credentials,
            client_id,
            client_key,
            username,
            password,
            keyword_entries,
            grammar_file,
        )
    except Exception as e:
        vh.error(e)
        exit(255)
    # Open audio source
    try:
        audio_source = FileAudioSource(audio_source)
    except Exception as e:
        vh.error("Failed to open audio file: %s" % e)
        exit(1)
    # make context
    ctx = Context(config, audio_source)
    # make view and run
    view = View(ctx)
    try:
        view.run()
    except Exception as e:
        vh.error(e)
        exit(1)
    exit(0)


if __name__ == "__main__":
    main()
