# Stops all training VM's.

#!/bin/bash -e

DEPLOYMENT_ID=$1
cfy executions start -d $DEPLOYMENT_ID -w execute_operation -p '{"operation": "cloudify.interfaces.lifecycle.stop", "type_names": ["cloudify.nodes.Compute"]}' -l