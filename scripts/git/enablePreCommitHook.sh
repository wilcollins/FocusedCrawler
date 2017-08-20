#!/bin/bash
set -u
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd )"
source "$DIR/../conf"

cp "$PROJECT_ROOT_DIR/hooks/pre-commit" "$PROJECT_ROOT_DIR/.git/hooks/pre-commit"
