# This script installs the training topology in local mode.
# Use this if you don't think you'll need to scale the topology (the "scale" workflow,
# as of 3.4.x, doesn't run in local mode).

#!/bin/bash -e

SCRIPTPATH=$(cd $(dirname $0) ; pwd -P)
cfy local install -p $SCRIPTPATH/../blueprint/blueprint.yaml -i $1 --task-retries 30