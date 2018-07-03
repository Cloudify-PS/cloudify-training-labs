'''Copyright Gigaspaces, 2017, All Rights Reserved'''
from cloudify_aws.connection import EC2ConnectionClient
from cloudify_aws.ec2.instance import Instance as AwsInstance


def stop(ctx, **_):
    '''
        Stops an instance

    ..note:

        This is slightly modified version of the built-in
        AWS Instance stop lifecycle. The difference is
        that this executes on nodes marked as external.
    '''
    ctx.instance.runtime_properties['aws_resource_id'] = \
        ctx.node.properties['resource_id']
    inst = AwsInstance()
    ctx.logger.info('Attempting to stop instance %s' % inst.resource_id)
    if inst.stop():
        return inst.post_stop()
    return ctx.operation.retry(
        'Waiting for instance %s to stop. Retrying...'
        % inst.resource_id)


def start(ctx, **_):
    '''
        Starts an instance

    ..note:

        This is slightly modified version of the built-in
        AWS Instance start lifecycle. The difference is
        that this executes on nodes marked as external.
    '''
    ctx.instance.runtime_properties['aws_resource_id'] = \
        ctx.node.properties['resource_id']
    inst = AwsInstance()
    ctx.logger.info('Attempting to start instance %s' % inst.resource_id)
    if inst.start():
        return inst.post_start()
    return ctx.operation.retry(
        'Waiting for instance %s to be running. Retrying...'
        % inst.resource_id)


def create_snapshots(ctx, **_):
    '''
        Creates snapshots of all volumes attached to an instance
    '''
    client = EC2ConnectionClient().client()
    inst = AwsInstance().get_resource()
    snapshot_ids = ctx.instance.runtime_properties.get(
        'snapshot_ids_creating', list())
    # If this is the first try, create the snapshots
    if ctx.operation.retry_number == 0:
        for dev in inst.block_device_mapping.itervalues():
            ctx.logger.info('Creating snapshot of volume %s' % dev.volume_id)
            snapshot = client.create_snapshot(dev.volume_id)
            snapshot_ids.append(snapshot.id)
            ctx.logger.info('Snapshot %s (volume: %s) is creating. Status: %s'
                            % (snapshot.id, dev.volume_id, snapshot.status))
        ctx.instance.runtime_properties['snapshot_ids'] = snapshot_ids
    # Verify that all snapshots are completed
    for snapshot in client.get_all_snapshots(snapshot_ids=snapshot_ids):
        if snapshot.status != 'completed':
            return ctx.operation.retry(
                'Waiting for snapshot %s (status: %s) to complete. Retrying...'
                % (snapshot.id, snapshot.status))


def delete_snapshots(ctx, **_):
    '''
        Deletes snapshots of all volumes attached to an instance
    '''
    client = EC2ConnectionClient().client()
    inst = AwsInstance().get_resource()
    snapshot_ids = ctx.instance.runtime_properties.get(
        'snapshot_ids_deleting', list())
    # If this is the first try, delete the volume snapshots
    if ctx.operation.retry_number == 0:
        # Get all attached volume IDs
        volume_ids = list()
        for dev in inst.block_device_mapping.itervalues():
            volume_ids.append(dev.volume_id)
        # Delete all volume snapshots
        for volume in client.get_all_volumes(volume_ids):
            ctx.logger.info('Finding all snapshots of volume %s' % volume.id)
            for snapshot in volume.snapshots():
                snapshot_ids.append(snapshot.id)
                ctx.logger.info('Deleting snapshot %s of volume %s'
                                % (snapshot.id, volume.id))
                snapshot.delete()
                ctx.logger.info(
                    'Snapshot %s (volume: %s) is deleting. Status: %s'
                    % (snapshot.id, volume.id, snapshot.status))
        ctx.instance.runtime_properties['snapshot_ids'] = snapshot_ids
