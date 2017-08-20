#!/bin/bash
set -u
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd )"
source "$DIR/../conf"

export KOPS_STATE_STORE=s3://clusters.dev.wilcollins.com
export MASTER_SIZE=t2.micro
export NODE_SIZE=t2.micro


# deploy pods
deploy_pods(){
  kubectl create -f $KUBE_CONFIG_FILE --save-config
}

# expose service to the internet
expose_service(){
  kubectl expose deployment $KUBE_DEPLOY_NAME --type="LoadBalancer"
}

add_ui_dashboard(){
  kubectl create -f https://raw.githubusercontent.com/kubernetes/kops/master/addons/kubernetes-dashboard/v1.6.3.yaml
}

get_ui_admin_pw() {
  kubectl config view \
    | grep password \
    | head -n 1 \
    | sed 's/password: //g' \
    | sed 's/ //g'
}


deploy(){
  DEPLOY_TAG_DEFAULT=latest
  DEPLOY_TAG_ALT=$ENV

  get_deploy_tag(){
    KUBE_CONFIG_PATH="$DIR/$KUBE_CONFIG_FILE"
    cat "$KUBE_CONFIG_PATH" | grep "$DOCKER_IMAGE" | sed s/.*$DOCKER_IMAGE://g
  }
  get_next_tag(){
    DEPLOY_TAG_CURRENT=$(get_deploy_tag)

    if [ "$DEPLOY_TAG_CURRENT" = "$DEPLOY_TAG_DEFAULT" ];then
      DEPLOY_TAG=$DEPLOY_TAG_ALT
    else
      DEPLOY_TAG=$DEPLOY_TAG_DEFAULT
    fi
    echo $DEPLOY_TAG
  }

  update_kube_config(){
    KUBE_CONFIG_PATH="$DIR/$KUBE_CONFIG_FILE"
    KUBE_CONFIG="$( cat "$KUBE_CONFIG_PATH" | sed s/$DOCKER_IMAGE:.*/$DOCKER_IMAGE:$1/g )"
    echo "$KUBE_CONFIG" > "$KUBE_CONFIG_PATH"
  }

  DEPLOY_TAG_CURRENT=$(get_deploy_tag)
  DEPLOY_TAG=$(get_next_tag)
  echo $DEPLOY_TAG_CURRENT
  echo $DEPLOY_TAG
  update_kube_config "$DEPLOY_TAG"

  update_cluster(){
    IMAGE="$DOCKER_REGISTRY/$DOCKER_IMAGE:$1"
    # kops update cluster
    kubectl set image deployment/$KUBE_DEPLOY_NAME "$IMAGE"
    #kops update cluster --yes
    echo "deploying image $IMAGE to kube $KUBE_DEPLOY_NAME"
  }
  update_cluster "$DEPLOY_TAG"

}
