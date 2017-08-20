#!/bin/bash
set -u
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd )"
source "$DIR/../conf"

aws ecr create-repository --repository-name $DOCKER_IMAGE
