#!/bin/bash
set -u
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd )"
source "$DIR/conf"

show_help(){
  cat <<EOF
Usage: [options]

-h| --help           show this help text
EOF
}

LOCAL=false
# Parse short options
OPTIND=1
while getopts "hl" opt
do
  case "$opt" in
    "l") LOCAL=true ;;
    "h") show_help; exit 0 ;;
    "?") show_help >&2; exit 1 ;;
  esac
done
shift $(expr $OPTIND - 1) # remove options from positional parameters
# end arg parsing

test () {
  if [ $LOCAL = 'true' ]; then
    npm start &
    sleep 5
    npm test
  else
    # Builds before running test inside container (not against it)
    $DIR/run.sh -b -w -c "./scripts/test.sh -l"
  fi

  EXIT_CODE=$?
  return $EXIT_CODE
}

if test ; then
  echo "pass"
fi
exit $EXIT_CODE
