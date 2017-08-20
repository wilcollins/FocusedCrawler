#!/bin/bash
set -u
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd )"
source "$DIR/../conf"

rm -f "$PROJECT_ROOT_DIR/.git/hooks/pre-commit"
