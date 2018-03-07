#!/usr/bin/env python

import argparse
from prettytable import PrettyTable
from cloudify_cli.cli import cfy


@cfy.pass_client()
def recreate_vms(client, deployment_id, vm_type):
    node_id = {
        'cli': 'cli_vm',
        'mgr': 'manager_vm',
        'mgr-img': 'cm_vm',
        'app': 'app_vm'
    }[vm_type]
    node_instances = client.node_instances.list(deployment_id=deployment_id,
                                                node_id=node_id)
    for ni in node_instances:
        print 'Recreating VM: {}'.format(ni.id)
        client.executions.start(deployment_id, 'heal', {'node_instance_id': ni.id},
                                force=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('deployment_id',
                        help='ID of the deployment')
    parser.add_argument('vm_type',
                        help='the VM type to heal',
                        choices=['cli', 'mgr', 'app'])

    args = parser.parse_args()

    recreate_vms(deployment_id=args.deployment_id,
                 vm_type=args.vm_type)