#!/bin/bash
set -u
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd )"
source "$DIR/conf"

cd $PROJECT_ROOT_DIR && \
  docker-compose build $DOCKER_IMAGE
