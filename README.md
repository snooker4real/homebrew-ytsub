# ytsub

CLI pour afficher ou telecharger la transcription (sous-titres) d'une video ou d'une playlist YouTube.

## Installation (Homebrew)

```
brew tap snooker4real/ytsub
brew install ytsub
```

Alternative sans Homebrew: `pipx install git+https://github.com/snooker4real/homebrew-ytsub`

## Utilisation

```
ytsub https://youtu.be/bqMBqcwR8vg              # affiche le texte
ytsub <url> -o transcript.txt                   # enregistre dans un fichier
ytsub <url> -j                                  # texte en paragraphes
ytsub <url> -f srt -l fr,en                     # format srt, langues preferees fr puis en
ytsub --langs <url>                             # langues disponibles
ytsub <url-playlist> -o transcripts/ --limit 10 # une playlist -> un fichier par video
```

Formats: `text` (defaut), `json`, `srt`, `vtt`. Si aucune langue demandee n'existe, la premiere disponible est utilisee.

## Publier une nouvelle version

```
./release.sh 0.1.1
```

Le script met a jour la version, cree le tag, calcule le sha256 du tarball GitHub et met a jour `Formula/ytsub.rb`.

## Developpement

```
python3 -m venv .venv && .venv/bin/pip install -e . pytest
.venv/bin/pytest
```
