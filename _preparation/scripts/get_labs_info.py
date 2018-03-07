#!/usr/bin/env python

import argparse
from prettytable import PrettyTable, ALL
from cloudify_cli.cli import cfy


def is_virtual_ip_node(node):
    return 'cloudify.nodes.VirtualIP' in node.type_hierarchy


@cfy.pass_client()
def get_labs_info(client, deployment_id):
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
                if is_virtual_ip_node(target_node):
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
                if is_virtual_ip_node(target_node):
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
    parser = argparse.ArgumentParser()
    parser.add_argument('deployment_id',
                        help='ID of the deployment to analyze')

    args = parser.parse_args()

    get_labs_info(deployment_id=args.deployment_id)