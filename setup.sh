#!/bin/bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

pip install -r "$DIR/requirements.txt"
sudo python -m nltk.downloader -d /usr/local/share/nltk_data all
cd server && npm install
