# "cfy local" equivalent of pull-all.sh.

#!/bin/bash -e
cfy local execute -w execute_operation -p '{"operation": "labs.pull", "node_ids": ["cli_configuration"]}'