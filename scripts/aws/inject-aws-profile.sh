#!/bin/bash

PROFILE=${1:-default}
PROFILE_CREDS=$(grep -A 2 $PROFILE ~/.aws/credentials)

scrape_field () {
  FIELD=$1
  VALUE=$( echo `echo "$PROFILE_CREDS" | grep $FIELD` | sed s/$FIELD.*=[[:space:]]*//g )
  echo $VALUE
}

AWS_ACCESS_KEY_ID=$(scrape_field aws_access_key_id)
AWS_SECRET_ACCESS_KEY=$(scrape_field aws_secret_access_key)

export AWS_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY

echo $AWS_ACCESS_KEY_ID
echo $AWS_SECRET_ACCESS_KEY
