import argparse
from cloudify_rest_client import CloudifyClient
from cloudify_rest_client.client import DEFAULT_PROTOCOL, SECURED_PROTOCOL


def is_virtual_ip_node(node):
    return 'cloudify.nodes.VirtualIP' in node.type_hierarchy


parser = argparse.ArgumentParser()
parser.add_argument('manager_ip', help='hostname or IP address of the manager')
parser.add_argument('username', help='username to authenticate with')
parser.add_argument('password', help='password to authenticate with')
parser.add_argument('deployment_id', help='ID of the deployment to analyze')
parser.add_argument('--tenant', help='tenant to operate on (optional; defaults to the default tenant)')
parser.add_argument('--ssl', help='connect using SSL', action='store_true')

args = parser.parse_args()

tenant_id = args.tenant or 'default_tenant'

client = CloudifyClient(host=args.manager_ip,
                        username=args.username,
                        password=args.password,
                        tenant=tenant_id,
                        protocol=SECURED_PROTOCOL if args.ssl else DEFAULT_PROTOCOL,
                        trust_all=True)
nodes = client.nodes.list(deployment_id=args.deployment_id)

if not nodes:
    print 'No nodes returned for deployment ID {0}. Are you sure this deployment exists?'.format(args.deployment_id)
    exit(1)

node_instances = client.node_instances.list(deployment_id=args.deployment_id)

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
        compute_nodes.append(node.id)
        for rel in node.relationships:
            target_node = nodes_map[rel['target_id']]
            if is_virtual_ip_node(target_node):
                public_compute_nodes.append(node.id)
                continue

trainees = {}

for compute_node in compute_nodes:
    node_instances = client.node_instances.list(deployment_id=args.deployment_id,
                                                node_id=compute_node)
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

header = []
for node in compute_nodes:
    header.append("{}.instance".format(node))
    header.append("{}.private".format(node))
    if node in public_compute_nodes:
        header.append("{}.public".format(node))

print ",".join(header)

for trainee in trainees:
    lst = []
    for node in compute_nodes:
        lst.append(trainees[trainee][node]['instance'])
        lst.append(trainees[trainee][node]['private'])
        if node in public_compute_nodes:
            lst.append(trainees[trainee][node]['public'])
    print ",".join(lst)
