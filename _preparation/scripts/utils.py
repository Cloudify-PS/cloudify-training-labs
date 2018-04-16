#!/usr/bin/env python

import argparse
import yaml
import logging

from cloudify_rest_client.client import CloudifyClient
from cloudify_cli.cli import cfy
from cloudify_cli.execution_events_fetcher import wait_for_execution
from cloudify.logs import create_event_message_prefix

from prettytable import PrettyTable, ALL

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


def _events_logger(events):
    for event in events:
        output = create_event_message_prefix(event)
        if output is not None:
            logger.info(output)


def _wait(client, execution):
    wait_for_execution(client,
                       execution,
                       events_handler=_events_logger,
                       include_logs=True, logger=logger)


def _is_virtual_ip_node(node):
    return 'cloudify.nodes.VirtualIP' in node.type_hierarchy


@cfy.pass_client()
def add_secrets(client, deployment_id, node_id, file, password, **kwargs):
    with open(file, 'r') as input_file:
        secrets = yaml.load(input_file)

    nodes_map = {}
    node_instances_map = {}
    nodes = client.nodes.list(deployment_id=deployment_id,
                              sort='id')
    for node in nodes:
        nodes_map[node.id] = node
    all_node_instances = client.node_instances.list(deployment_id=deployment_id)
    for node_instance in all_node_instances:
        node_instances_map[node_instance.id] = node_instance

    node_instances = client.node_instances.list(deployment_id=deployment_id,
                                                node_id=node_id)
    for ni in node_instances:
        public_ip = None
        for rel in ni.relationships:
            target_node_id = rel['target_name']
            target_node = nodes_map[target_node_id]
            if _is_virtual_ip_node(target_node):
                target_node_instance = node_instances_map[rel['target_id']]
                public_ip = target_node_instance.runtime_properties['aws_resource_id']
                break
        if not public_ip:
            raise Exception()

        current_client = CloudifyClient(host=public_ip, username='admin', password=password,
                                        tenant='default_tenant')
        print "Creating on: {}".format(public_ip)

        for key, value in secrets.iteritems():
            print "\t{}...".format(key)
            current_client.secrets.create(key, value, True)


@cfy.pass_client()
def control(client, deployment_id, kind, op, **kwargs):
    d = {
        'cli': {
            'filter': 'node_ids',
            'criteria': ['cli_vm']
        },
        'mgr': {
            'filter': 'node_ids',
            'criteria': ['manager_vm']
        },
        'mgr-ami': {
            'filter': 'node_ids',
            'criteria': ['cm_vm']
        },
        'app': {
            'filter': 'node_ids',
            'criteria': ['app_vm']
        },
        'all': {
            'filter': 'type_names',
            'criteria': ['cloudify.nodes.Compute']
        }
    }
    desc = d[kind]
    filter = desc['filter']
    criteria = desc['criteria']

    execution = client.executions.start(
        deployment_id, 'execute_operation',
        {
            filter: criteria,
            'operation': 'cloudify.interfaces.lifecycle.{}'.format(op)
        })

    print('Execution ID: {}'.format(execution.id))
    _wait(client, execution)


@cfy.pass_client()
def recreate(client, deployment_id, vm_type, **kwargs):
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
        execution = client.executions.start(
            deployment_id, 'heal', {'node_instance_id': ni.id},
            force=True)
        print '\tExecution ID: {}'.format(execution.id)


@cfy.pass_client()
def install_cli(client, deployment_id, **kwargs):
    execution = client.executions.start(
        deployment_id,
        'execute_operation',
        {'operation': 'custom.install_cli',
         'node_ids': ['cli_configuration']})
    print 'Execution ID: {}'.format(execution.id)
    _wait(client, execution)


@cfy.pass_client()
def refresh_labs(client, deployment_id, **kwargs):
    execution = client.executions.start(
        deployment_id,
        'execute_operation',
        {'operation': 'cloudify.interfaces.lifecycle.create',
         'node_ids': ['cli_labs']})
    print 'Execution ID: {}'.format(execution.id)
    _wait(client, execution)


@cfy.pass_client()
def heal(client, deployment_id, node_instance_id, **kwargs):
    execution = client.executions.start(
        deployment_id,
        'heal',
        {'node_instance_id': node_instance_id})
    print 'Execution ID: {}'.format(execution.id)
    _wait(client, execution)


@cfy.pass_client()
def scale(client, deployment_id, delta, **kwargs):
    execution = client.executions.start(
        deployment_id,
        'scale',
        {'scalable_entity_name': 'trainee',
         'delta': delta})
    print 'Execution ID: {}'.format(execution.id)
    _wait(client, execution)


@cfy.pass_client()
def get_info(client, deployment_id, **kwargs):
    nodes = client.nodes.list(deployment_id=deployment_id,
                              sort='id')

    if not nodes:
        print 'No nodes returned for deployment ID {0}. Are you sure this deployment exists?'.format(deployment_id)
        exit(1)

    node_instances = client.node_instances.list(deployment_id=deployment_id)

    compute_nodes=[]
    public_compute_nodes=[]
    nodes_map = {}
    node_instances_map = {}

    for node in nodes:
        nodes_map[node.id] = node

    for node_instance in node_instances:
        node_instances_map[node_instance.id] = node_instance

    for node in nodes:
        if 'lab_vm' in node.type_hierarchy:
            compute_nodes.append(node)
            for rel in node.relationships:
                target_node = nodes_map[rel['target_id']]
                if _is_virtual_ip_node(target_node):
                    public_compute_nodes.append(node.id)
                    continue

    trainees = {}

    for compute_node in compute_nodes:
        node_instances = client.node_instances.list(deployment_id=deployment_id,
                                                    node_id=compute_node.id)
        for node_instance in node_instances:
            scaling_group_id = node_instance.scaling_groups[0]['id']
            if scaling_group_id in trainees:
                trainee = trainees[scaling_group_id]
            else:
                trainee = {}
                trainees[scaling_group_id] = trainee

            trainee[node_instance.node_id] = {}
            trainee[node_instance.node_id]['private'] = node_instance.runtime_properties['ip']
            trainee[node_instance.node_id]['instance'] = node_instance.id

            for rel in node_instance.relationships:
                target_node = nodes_map[rel['target_name']]
                if _is_virtual_ip_node(target_node):
                    target_node_instance = node_instances_map[rel['target_id']]
                    trainee[node_instance.node_id]['public'] = target_node_instance.runtime_properties['aws_resource_id']
                    break

    header_elements = ['#']
    for node in compute_nodes:
        display_name = node.properties['display_name']
        header_elements.append("{}".format(display_name))
        # header_elements.append("{} (private)".format(display_name))
        # if node.id in public_compute_nodes:
        #     header_elements.append("{} (public)".format(display_name))

    table = PrettyTable(header_elements,
                        hrules=ALL)
    table.valign = 'm'

    ix = 1
    for trainee in trainees:
        lst = [ix]
        for node in compute_nodes:
            contents = '{}\n' \
                       '{}'.format(
                trainees[trainee][node.id]['instance'],
                trainees[trainee][node.id]['private']
            )
            if node.id in public_compute_nodes:
                contents += '\n{}'.format(
                    trainees[trainee][node.id]['public']
                )
            lst.append(contents)
        table.add_row(lst)
        ix += 1

    print "Note: each cell contains, from top to bottom: instance ID, private IP, public IP"
    print table


if __name__ == '__main__':
    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument('deployment_id',
                               help='ID of the deployment')

    master_parser = argparse.ArgumentParser()
    subparsers = master_parser.add_subparsers()
    subparsers.required = True

    labs_info_parser = subparsers.add_parser('get-info', parents=[common_parser])
    labs_info_parser.set_defaults(func=get_info)

    add_secrets_parser = subparsers.add_parser('add-secrets', parents=[common_parser])
    add_secrets_parser.add_argument('node_id',
                                    choices=['cm_vm', 'manager_vm'],
                                    help="Manager node ID")
    add_secrets_parser.add_argument('file',
                                    help="Secrets file")
    add_secrets_parser.add_argument('password',
                                    help="Password for the admin user")
    add_secrets_parser.set_defaults(func=add_secrets)

    control_parser = subparsers.add_parser('control', parents=[common_parser])
    control_parser.add_argument('op',
                                choices=['start', 'stop', 'restart'],
                                help="Operation to perform")
    control_parser.add_argument('kind',
                                choices=['cli', 'mgr', 'mgr-ami', 'app', 'all'],
                                help="VM's to control")
    control_parser.set_defaults(func=control)

    recreate_parser = subparsers.add_parser('recreate', parents=[common_parser])
    recreate_parser.add_argument('vm_type',
                                 choices=['cli', 'mgr', 'mgr-ami', 'app'],
                                 help="Type of VM to recreate")
    recreate_parser.set_defaults(func=recreate)

    install_cli_parser = subparsers.add_parser('install-cli', parents=[common_parser])
    install_cli_parser.set_defaults(func=install_cli)

    heal_parser = subparsers.add_parser('heal', parents=[common_parser])
    heal_parser.add_argument('node_instance_id',
                             help="ID of node instance to heal")
    heal_parser.set_defaults(func=heal)

    scale_parser = subparsers.add_parser('scale', parents=[common_parser])
    scale_parser.add_argument('delta',
                              help="number of instances/groups to create/delete")
    scale_parser.set_defaults(func=scale)

    refresh_labs_parser = subparsers.add_parser('refresh-labs', parents=[common_parser])
    refresh_labs_parser.set_defaults(func=refresh_labs)

    args = master_parser.parse_args()
    args.func(**vars(args))
