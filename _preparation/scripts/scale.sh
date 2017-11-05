# Starts all training VM's.

#!/bin/bash -e

DEPLOYMENT_ID=$1
DELTA=$2

cfy executions start -d $1 -p '{"scalable_entity_name": "trainee", "delta": '"$DELTA"'}' scale
