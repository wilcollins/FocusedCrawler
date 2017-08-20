#!/bin/bash
set -u
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd )"
source "$DIR/conf"

$DIR/push.sh

echo ""

source $DIR/aws/inject-aws-profile.sh $AWS_PROFILE

echo ""

# show start time
echo "$(date +%r)"
time $DIR/aws/ecs-deploy.sh 2>&1 &
