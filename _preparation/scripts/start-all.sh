# Starts all training VM's.

#!/bin/bash -e
cfy executions start -d prep -w execute_operation -p '{"operation": "cloudify.interfaces.lifecycle.start", "type_names": ["cloudify.nodes.Compute"]}' -l