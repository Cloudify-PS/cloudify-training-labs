'''Copyright Gigaspaces, 2017, All Rights Reserved'''
from cloudify.plugins import lifecycle

OP_START = 'hacker.interfaces.lifecycle.start'
OP_STOP = 'hacker.interfaces.lifecycle.stop'
OP_SS_C = 'hacker.interfaces.lifecycle.create_snapshots'
OP_SS_D = 'hacker.interfaces.lifecycle.delete_snapshots'
REQUIRED_OPS = set([OP_START, OP_SS_C, OP_SS_D, OP_STOP])


def build_instance_sequence(instance, operation,
                            state_start=None, state_end=None):
    '''
        Builds sequenced subgraph tasks for an instance

    .. note::

        The sequence will not be built if the instance provided
        does not have a node with an operation defined in the
        operation parameter.

    :param `CloudifyWorkflowNodeInstance` instance:
        Node instance to execute tasks against
    :param str operation:
        Node (lifecycle) operation to execute
    :param str state_start:
        Verb to describe operation start
    :param str state_stop:
        Verb to describe operation finish
    '''
    tasks = list()
    # Only build the sequence if the node operation exists
    if operation not in instance.node.operations:
        return tasks
    # Add task starting state
    if state_start:
        tasks.append(instance.send_event('%s host' % state_start))
        tasks.append(instance.set_state(state_start.lower()))
    # Add task operation
    tasks.append(instance.execute_operation(operation))
    # Add task ended state
    if state_end:
        tasks.append(instance.send_event('%s host' % state_end))
        tasks.append(instance.set_state(state_end.lower()))
    return tasks


def build_instance_subgraph(instance, graph):
    '''
        Builds a subgraph for an instance

    :param `CloudifyWorkflowNodeInstance` instance:
        Node instance to execute tasks against
    :param `TaskDependencyGraph` graph:
        Task graph to create sequences from
    '''
    # Init a "stop instance" subgraph
    sg_stop = graph.subgraph('stop_subgraph')
    seq_stop = sg_stop.sequence()
    seq_stop.add(*build_instance_sequence(
        instance, OP_STOP, 'Stopping', 'Stopped'))
    # Init a "recreate snapshots" subgraph
    sg_snap = graph.subgraph('snapshot_subgraph')
    seq_snap = sg_snap.sequence()
    if OP_SS_D in instance.node.operations:
        seq_snap.add(*build_instance_sequence(instance, OP_SS_D))
    if OP_SS_C in instance.node.operations:
        seq_snap.add(*build_instance_sequence(instance, OP_SS_C))
    # Init a "start instance" subgraph
    sg_start = graph.subgraph('stop_subgraph')
    seq_start = sg_start.sequence()
    seq_start.add(*build_instance_sequence(
        instance, OP_START, 'Starting', 'Started'))
    # Create subgraph dependencies
    graph.add_dependency(sg_snap, sg_stop)
    graph.add_dependency(sg_start, sg_snap)


def refresh_snapshots(ctx, **_):
    '''
        Executes a complex, graph-based set of lifecycle events
        to stop all host (compute) instances, delete all
        existing instance snapshots, take new snapshots
        of all attached volumes, and start the instances
        back up when complete.
    '''
    graph = ctx.graph_mode()
    # Find all compute hosts and build a sequence graph
    for node in ctx.nodes:
        if not REQUIRED_OPS.issubset(node.operations):
            ctx.logger.warn(
                'Skipping refresh_snapshots workflow for node "%s" because '
                'it does not have all required operations defined' % node.id)
            continue
        # Iterate over each node instance
        for instance in node.instances:
            if not lifecycle.is_host_node(instance):
                ctx.logger.warn(
                    'Skipping refresh_snapshots workflow for node instance '
                    '"%s" because it is not a compute host' % instance.id)
                continue
            build_instance_subgraph(instance, graph)
    # Execute the sequences
    return graph.execute()
