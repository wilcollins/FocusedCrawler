#!/bin/bash
set -u
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd )"
source "$DIR/../conf"

if [[ $# -eq 0 ]] ; then
    echo 'At least one image tag must be provided'
    exit 0
fi

$DIR/ecr-create-repo.sh 2>/dev/null

push(){
  IMAGE_TAG=$1
  echo "pushing $DOCKER_IMAGE:$IMAGE_TAG"
  docker tag $DOCKER_IMAGE:$IMAGE_TAG $AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$DOCKER_IMAGE:$IMAGE_TAG
  docker push $AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$DOCKER_IMAGE:$IMAGE_TAG
}

# login to ECR so the image can be pushed
$DIR/ecr-login.sh

for tag in "$@"
do
    push $tag
done
