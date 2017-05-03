# Lab: High Availability

In this lab, we will:

1. Create a few Cloudify Managers
2. Join them into a cluster
3. Bring down the active Cloudify Manager and witness how a standby instance takes control.

## Step 1: Create Cloudify Managers

Create three Cloudify Manager instances, either You can do this either via bootstrapping, or via a Cloudify Manager image.

We will refer to these managers as `cm1`, `cm2` and `cm3`.

* `cm1` will be the initial designated master.
* `cm2` and `cm3` will be the initial standby's.
 
## Step 2: Switch CLI to control the designated master

Ensure that your CLI's active profile points to `cm1`.

*   If you created `cm1` via bootstrapping, then your CLI environment already has a profile for `cm1`. Switch to it by
    using the `cfy profiles use <ip-address>` command.
*   If you created `cm1` from an image, you'll have to use the `cfy profiles use` command and specify all required
    connectivity parameters (username, password, tenant ID).

## Step 3: Start the cluster

```bash
cfy cluster start --cluster-host-ip <ip-address> --cluster-node-name master
```

*   The `ip-address` field should be replaced with an IP address that all other cluster participants can access; if this
    parameter is not specified, then the default value is taken from the CLI profile.

    **IMPORTANT NOTE**: Sometimes, the IP address from the CLI profile may not work out. For example, consider the scenario
    when your CLI profile refers to `cm1` by its public IP address, and your network configuration doesn't allow other
    cluster participants to access `cm1` by its public IP.

    Typically, you will want to provide `cm1`'s private IP address here.

*   The `--cluster-node-name` value can be any string; it is used for conveniently recognizing nodes within the cluster.

## Step 4: Switch CLI to control the first standby

Use the `cfy profiles use` command to set the `cm2` profile as the active profile, as described in Step 2 above.

## Step 5: Add `cm2` to the cluster

```bash
cfy cluster join <master-profile> --cluster-host-ip <ip-address> --cluster-node-name backup_1
```

*   `<master-profile>` is the name of the CLI profile that points to the cluster's master.
*   `<ip-address>` is the IP address of `cm2`, as it is going to be presented to the cluster. It **must** be an IP
    address that is reachable by other cluster members. Typically, you'd want to specify `cm2`'s private IP address here.
*   `backup_1` can be replaced with any other name to your liking.

## Step 6: Add `cm3` to the cluster

Repeat steps 4 & 5 above, for `cm3`.

## Step 7: Check the cluster's status

You can check the cluster's status by issuing the following command on any cluster member:

```bash
cfy cluster status
```

You'll see output similar to the following:

```
Cloudify Manager cluster initialized!
Encryption key: pyYUkPgZ5Uvw1kSWrivYTg==
```













To see the list of nodes in the cluster, and their status:

```bash
cfy cluster nodes list
```