# VoiceXTractor

<p align="center">~ A python CLI tool to extract voice sentences from audio files with speech recognition ~</p>
<p align="center">
  <a href="https://ko-fi.com/veeso" target="_blank">Ko-fi</a>
  ·
  <a href="#get-started" target="_blank">Installation</a>
  ·
  <a href="/docs/en_EN/man.md" target="_blank">User manual</a>
</p>

<p align="center">Developed by <a href="https://veeso.github.io/" target="_blank">@veeso</a></p>
<p align="center">Current version: 0.1.0 (09/01/2022)</p>

<p align="center">
  <a href="https://opensource.org/licenses/MIT"
    ><img
      src="https://img.shields.io/badge/License-MIT-teal.svg"
      alt="License-MIT"
  /></a>
  <a href="https://github.com/veeso/vxt/stargazers"
    ><img
      src="https://img.shields.io/github/stars/veeso/vxt.svg"
      alt="Repo stars"
  /></a>
  <a href="https://pepy.tech/project/vxt"
    ><img
      src="https://pepy.tech/badge/vxt"
      alt="Downloads counter"
  /></a>
  <a href="https://pypi.org/project/vxt/"
    ><img
      src="https://badge.fury.io/py/vxt.svg"
      alt="Latest version"
  /></a>
  <a href="https://ko-fi.com/veeso">
    <img
      src="https://img.shields.io/badge/donate-ko--fi-red"
      alt="Ko-fi"
  /></a>
</p>
<p align="center">
  <a href="https://github.com/veeso/vxt/actions"
    ><img
      src="https://github.com/veeso/vxt/workflows/Ci/badge.svg"
      alt="CI"
  /></a>
  <a href="https://coveralls.io/github/veeso/vxt"
    ><img
      src="https://coveralls.io/repos/github/veeso/vxt/badge.svg"
      alt="Coveralls"
  /></a>
</p>

---

## About VXT 🚜

VXT, which stands for VoiceXTractor is a Python command-line utility to extract voice tracks from audio.

How it works:

1. You provide VXT with an audio file
2. The audio file is split by silence
3. for each "track" chunked by the audio file, it gets the speech for it using a customisable speech-to-text engine
4. you can at this point work on tracks (amplify, normalize, split, remove...)
5. export the tracks to files with the format you prefer

---

## Get started 🚀

You can install VXT with pip:

```sh
pip3 install vxt
```

then you can run VXT with the following arguments:

```sh
vxt -l it_IT -o ./output/ ./hackerino.mp3
```

this will split the `hackerino.mp3` audio file into tracks by voice into `output/`, the `-l` option specifies the audio language is Italian.

vxt supports these options:

```txt
  -e, --engine TEXT            Specify speech2text engine [bing, google,
                               google-cloud, houndify, ibm, sphinx] (default:
                               google)

  -l, --language TEXT          Specify audio language (e.g. it_IT), system
                               language will be used otherwise

  -f, --output-fmt TEXT        Specify output format (See readme)
  -o, --output-dir TEXT        Specify output directory
  -A, --api-key TEXT           Specify api key (required for: bing, google
  -J, --json-credentials TEXT  Specify json credentials (required for: google-
                               cloud)

  -C, --client-id TEXT         Specify client id (required for: houndify)
  -K, --client-key TEXT        Specify client key (required for: houndify)
  -U, --username TEXT          Specify username (required for: ibm)
  -P, --password TEXT          Specify user password (required for: ibm)
  --keyword-entries TEXT       Specify keyword entries (required for: sphinx)
  --grammar-file TEXT          Specify grammar file (required for: sphinx)
  --help                       Show this message and exit.
```

by default the `google` engine will be used for speech-to-text.

### Output format

Track filename fmt.
The syntax use parameters which must be preceeded by `%`, everything in between will be kept the same.
The following parameters are supported.

- `%%`: print percentage symbol
- `%d`: current day
- `%H`: current hours
- `%I`: current timestamp ISO8601 syntax
- `%M`: current minutes
- `%m`: current month
- `%S`: current seconds
- `%s`: track speech
- `%s`.NUMBER track speech cut at length (e.g. `%s.24`)
- `%t`: track number in track list (from 1 to n)
- `%y`: current year with 2 digits
- `%Y`: current year with 4 digits

---

## Support the developer ☕

If you like VXT and you're grateful for the work I've done, please consider a little donation 🥳

You can make a donation with one of these platforms:

[![ko-fi](https://img.shields.io/badge/Ko--fi-F16061?style=for-the-badge&logo=ko-fi&logoColor=white)](https://ko-fi.com/veeso)
[![PayPal](https://img.shields.io/badge/PayPal-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://www.paypal.me/chrisintin)

---

## Contributing and issues 🤝🏻

Contributions, bug reports, new features and questions are welcome! 😉
If you have any question or concern, or you want to suggest a new feature, or you want just want to improve VXT, feel free to open an issue or a PR.

Please follow [our contributing guidelines](CONTRIBUTING.md)

---

## Changelog ⏳

View VXT's changelog [HERE](CHANGELOG.md)

---

## Powered by 💪

VXT is powered by these awesome projects:

- [PyInquirer](https://github.com/CITGuru/PyInquirer)
- [pydub](http://pydub.com/)
- [speech_recognition](https://github.com/Uberi/speech_recognition)
- [yaspin](https://pypi.org/project/yaspin/)

---

## License 📃

VXT is licensed under the MIT license.

You can read the entire license [HERE](LICENSE)
