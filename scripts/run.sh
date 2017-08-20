#!/bin/bash
set -u
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd )"
source "$DIR/conf"

KILL_SCRIPT="$DIR/kill.sh"
BUILD_SCRIPT="$DIR/build.sh"

# kills currently running servers unless `-s|--safe` is provided
FORCE=true
BUILD=false

# ----- arg parsing -----

show_help(){
  cat <<EOF
Usage: [options]

-h| --help           show this help text
-s|--safe            safe mode (will not kill currently running server)
-b|--build           build the server before running
EOF
}

# Transform long options to short ones
for arg in "$@"; do
  shift
  case "$arg" in
    "--help") set -- "$@" "-h" ;;
    "--safe") set -- "$@" "-s" ;;
    "--build") set -- "$@" "-b" ;;
    *)        set -- "$@" "$arg"
  esac
done

INTERACTIVE_OR_DETACHED_DEFAULT="-d"
INTERACTIVE_OR_DETACHED=$INTERACTIVE_OR_DETACHED_DEFAULT
WAIT=false
CMD=""
# Parse short options
OPTIND=1
while getopts "hsbc:iw" opt
do
  case "$opt" in
    "h") show_help; exit 0 ;;
    "s") FORCE=false; ;;
    "b") BUILD=true; ;;
    "c") CMD="${OPTARG}" ; echo $CMD;;
    "i") INTERACTIVE_OR_DETACHED="" ;;
    "w") WAIT="true" ;;
    "?") show_help >&2; exit 1 ;;
  esac
done
shift $(expr $OPTIND - 1) # remove options from positional parameters
# end arg parsing

if [ $FORCE = "true" ]; then
  $KILL_SCRIPT 2>/dev/null
fi

if [ $BUILD = "true" ]; then
  $BUILD_SCRIPT
fi

# run container
RUN_CONTAINER_CMD="docker-compose run $INTERACTIVE_OR_DETACHED --service-ports $DOCKER_SERVICE $CMD"
if [ "$INTERACTIVE_OR_DETACHED" = "$INTERACTIVE_OR_DETACHED_DEFAULT" ]; then
  CONTAINER_ID=$($RUN_CONTAINER_CMD)

  # cache container id
  echo "caching"
  mkdir $PROJECT_TMP_DIR 2>/dev/null
  echo $CONTAINER_ID > "$CONTAINER_ID_FILE"

  # show container logs
  docker logs -f $CONTAINER_ID &

  if [ "$WAIT" = "true" ]; then
    EXIT_CODE=$(docker wait $CONTAINER_ID)
    exit $EXIT_CODE
  fi
else
  /bin/bash -c "$RUN_CONTAINER_CMD"
fi

EXIT_CODE=$?
exit $EXIT_CODE
