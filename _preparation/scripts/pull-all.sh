#!/bin/bash -e

cfy executions start -d prep -w execute_operation -p '{"operation": "labs.pull", "node_ids": ["cli_configuration"]}' -l