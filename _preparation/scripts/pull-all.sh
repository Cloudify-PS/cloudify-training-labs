# For all CLI VM's, pull the latest training labs material from Git.
# This is useful if a fix is being pushed to the training labs repo, while a training course
# is still ongoing.

#!/bin/bash -e
cfy executions start -d prep -w execute_operation -p '{"operation": "labs.pull", "node_ids": ["cli_configuration"]}' -l