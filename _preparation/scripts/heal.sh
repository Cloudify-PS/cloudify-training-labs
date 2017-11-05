# Starts all training VM's.

#!/bin/bash -e

DEPLOYMENT_ID=$1
NODE_INSTANCE_ID=$2

cfy executions start -d $1 -p '{"node_instance_id": '"$NODE_INSTANCE_ID"'}' heal
