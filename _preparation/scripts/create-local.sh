#!/bin/bash -e
SCRIPTPATH=$(cd $(dirname $0) ; pwd -P)
cfy local install -p $SCRIPTPATH/../blueprint/blueprint.yaml -i $1 --task-retries 30