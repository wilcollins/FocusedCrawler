#!/bin/bash
# ecs-deploy : https://github.com/silinternational/ecs-deploy

set -u
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd )"
source "$DIR/../conf"

$ECS_DEPLOY -p $AWS_PROFILE -r $REGION -t $PUSH_TIMEOUT -c $CLUSTER -n $SERVICE -i $IMAGE_HUB_URL --max-definitions 10 --enable-rollback
