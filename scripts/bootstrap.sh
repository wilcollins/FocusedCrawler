#!/bin/bash
set -u
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd )"
source "$DIR/conf"

pip uninstall docker-py; pip uninstall docker; pip install docker

cd .. && git submodule update --init --recursive

$DIR/git/enablePreCommitHook.sh

cd $DIR/../server && npm install
