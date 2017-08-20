#!/bin/bash
set -u
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd )"
source "$DIR/conf"

if ! $DIR/test.sh; then
  echo "Failed tests. Not pushing a broken build."
  exit 1;
fi

DOCKER_TAG="${1:-$DOCKER_TAG}"
$DIR/aws/ecr-push-image.sh $ENV $DOCKER_TAG
