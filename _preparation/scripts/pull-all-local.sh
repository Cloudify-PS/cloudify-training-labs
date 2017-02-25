# "cfy local" equivalent of pull-all.sh.
# Use this if you don't think you'll need to scale the topology (the "scale" workflow,
# as of 3.4.x, doesn't run in local mode).

#!/bin/bash -e
cfy local execute -w execute_operation -p '{"operation": "labs.pull", "node_ids": ["cli_configuration"]}'