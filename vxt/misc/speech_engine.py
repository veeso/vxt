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

from ..view.config import Config

from typing import Optional

BING = "bing"
GOOGLE = "google"
GOOGLE_CLOUD = "google-cloud"
HOUNDIFY = "houndify"
IBM = "ibm"
SPHINX = "sphinx"


def init_speech_engine(
    config: Config,
    engine: str,
    api_key: Optional[str],
    json_credentials: Optional[str],
    client_id: Optional[str],
    client_key: Optional[str],
    username: Optional[str],
    password: Optional[str],
    keyword_entries: Optional[str],
    grammar_file: Optional[str],
) -> Config:
    """
    Given the option parameters, initialize the speech engine in the configuration.
    Then return the configuration with the configuration applied.
    """
    if engine == BING:
        if not api_key:
            raise Exception("%s engine requires 'api-key' argument" % BING)
        config.use_bing_speech2text(api_key)
    elif engine == GOOGLE:
        config.use_google_speech2text(api_key)
    elif engine == GOOGLE_CLOUD:
        if not json_credentials:
            raise Exception(
                "%s engine requires 'json-credentials' argument" % GOOGLE_CLOUD
            )
        config.use_google_cloud_speech2text(json_credentials)
    elif engine == HOUNDIFY:
        if not client_id:
            raise Exception("%s engine requires 'client-id' argument" % HOUNDIFY)
        if not client_key:
            raise Exception("%s engine requires 'client-id' argument" % HOUNDIFY)
        config.use_houndify_speech2text(client_id, client_key)
    elif engine == IBM:
        if not username:
            raise Exception("%s engine requires 'client-id' argument" % IBM)
        if not password:
            raise Exception("%s engine requires 'client-id' argument" % IBM)
        config.use_ibm_speech2text(username, password)
    elif engine == SPHINX:
        config.use_sphinx_speech2text(keyword_entries, grammar_file)
    else:
        raise Exception("Unknown speech2text engine: %s" % engine)
