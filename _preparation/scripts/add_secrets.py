#!/usr/bin/env python

import argparse
import yaml
from cloudify_rest_client.client import CloudifyClient
from cloudify_cli.cli import cfy


@cfy.pass_client()
def add_secrets(client, deployment_id, file, password):
    with open(file, 'r') as input_file:
        secrets = yaml.load(input_file)

    node_id = 'cm_vm'

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
            if 'cloudify.nodes.VirtualIP' in target_node.type_hierarchy:
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('deployment_id',
                        help='ID of the deployment')
    parser.add_argument('file',
                        help="Secrets file")
    parser.add_argument('password',
                        help="Password for the admin user")
    args = parser.parse_args()

    add_secrets(deployment_id=args.deployment_id,
                file=args.file,
                password=args.password)
