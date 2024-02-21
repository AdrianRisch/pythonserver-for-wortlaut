# Flask Audio Transcription Service

Dieses Projekt bietet einen Web-Service zur Transkription von Audiodateien unter Verwendung des Faster Whisper-Modells. Es unterstützt auch die semantische Analyse und detaillierte Wort-für-Wort-Vergleiche zwischen erwartetem und transkribiertem Text.

## Verwandte Projekte

- Für das dazugehörige Frontend oder weitere Informationen, besuche [dieses Repository](https://github.com/AdrianRisch/wortlaut-flutterapp).


## Features

- Transkription von Audiodateien mit dem Faster Whisper-Modell.
- Semantische Ähnlichkeitsberechnung zwischen Texten.
- Detaillierter Wort-für-Wort-Vergleich zwischen erwartetem und transkribiertem Text.


## Voraussetzungen

- Python 3.11.5 (nur damit getestet)
- Flask
- Flask-CORS
- Spacy und ein deutsches Spacy-Modell [(`de_core_news_md`)](https://spacy.io/models/de)
- Torch
- [Faster Whisper](https://github.com/SYSTRAN/faster-whisper)
- FFmpeg: Für die Verarbeitung von Audiodateien ist FFmpeg notwendig. Die Installation von FFmpeg kann je nach Betriebssystem variieren. Besuche [FFmpeg.org](https://ffmpeg.org//) für Installationsanweisungen.

## Installation

1. Klone dieses Repository.
2. Installiere die erforderlichen Python-Pakete mit `pip install -r requirements.txt`.
3. Lade das Spacy-Modell mit `python -m spacy download de_core_news_md` herunter.
4. Erstelle den Ordner **temp_audio**.
5. Starte den Server mit: ```python <server_fasterWhisper>.py```

## Konfiguration

Die Standardkonfiguration kann direkt im Code geändert werden. Das Upload-Verzeichnis und das Whisper-Modell (Größe) können in der Datei angepasst werden.
Zur Auswahl stehen: "tiny","small","base","medium","large"
Es empfiehlt sich vor dem 1. Nutzen alle benötigten Modelle mindestens einmal geladen zu haben.

## Ausführung

Starte den Server mit:

```bash
python <server_fasterWhisper>.py
```
## API-Endpunkte

 -   POST /transcribe: Transkribiert die hochgeladene Audiodatei. Optionale Parameter für die Analyse können übermittelt werden (model_size, analysis_type, expected_text).
 -   GET /ping: Überprüft die Erreichbarkeit des Servers.
