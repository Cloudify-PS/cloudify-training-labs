# For all CLI VM's, pull the latest training labs material from Git.
# This is useful if a fix is being pushed to the training labs repo, while a training course
# is still ongoing.

#!/bin/bash -e

DEPLOYMENT_ID=$1
cfy executions start -d $DEPLOYMENT_ID -p '{"operation": "custom.install_cli", "node_ids": ["cli_configuration"]}' execute_operation
