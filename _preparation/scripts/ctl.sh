#!/bin/bash -e

DEPLOYMENT_ID=$1
KIND=$2
OP=$3

case "$KIND" in
    cli )
        filter='node_ids'
        criteria='["cli_vm"]'
        ;;
    mgr )
        filter='node_ids'
        criteria='["manager_vm"]'
        ;;
    app )
        filter='node_ids'
        criteria='["nodejs_vm","mongodb_vm"]'
        ;;
    all )
        filter='type_names'
        criteria='["cloudify.nodes.Compute"]'
        ;;
    * )
        echo "Invalid option; should be either 'cli', 'mgr' or 'app'"
        exit 1
esac

cfy executions start -d $DEPLOYMENT_ID -w execute_operation -p '{"operation": "cloudify.interfaces.lifecycle.'$OP'", "'$filter'": '${criteria}'}' -l