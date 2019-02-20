# Lab: Cloudify Manager and OpenStack

In this lab, we will create a Cloudify Manager, upload a blueprint to it, create a deployment and install it.

There are two methods for creating a Cloudify Manager:

* Via a provided image (recommended)
* Via bootstrapping

Both approaches will be covered in this lab. You may choose to practice either, or both.

## Part 1: Preparations

The [Cloudify Manager prerequisites page](https://docs.cloudify.co/4.5.5/install_maintain/installation/prerequisites/) describes a few
networking- and security-related prerequisites. You will have to ensure that you have the following:

* A security group that allows access to the manager via the ports specified in the Prerequisites page:
  * Ports 80, 443 and 22, with the source being any address / CIDR / security group that you'd like to access
    Cloudify Manager from.
  * Ports 5671, 5672, 53229, and 53333 from any VM that:
    * Is going to be created by Cloudify; and
    * Is going to have the Cloudify Agent installed on it.
* A security group that allows access to agents, as specified in the [Agent prerequisites description](https://docs.cloudify.co/4.5.5/install_maintain/agents/).
* A network to connect the Cloudify Manager to.
* A keypair to use for SSH'ing into the Cloudify Manager VM.

**TIP**: For maximum flexibility, consider setting the security groups up as follows:

* Create a security group for Cloudify management (for example's sake, we will refer to it as `cloudify-management`).
* Create a security group for Cloudify agents (`cloudify-agents`).
* Edit `cloudify-management`'s rules, allowing:
    * Ports 80, 443 and 22 from anywhere (in production systems, you will most likely want to restrict this by CIDR or
      a security group).
    * Ports 5671, 5672, 53229, and 53333 from the security group `cloudify-agents`.
* Edit `cloudify-agents`'s rules, allowing:
    * Ports 22 and 5985 from the security group `cloudify-management`.

The advantage in this security groups setup is that no CIDR masks are involved in security group rules for the purpose
of enabling agent <-> manager communication.

## Part 2: Creating a Cloudify Manager from an Image

### Step 1: Import the Cloudify Manager image to OpenStack

The official Cloudify Manager image is located at: http://repository.cloudifysource.org/cloudify/4.5.5/ga-release/cloudify-manager-4.5.5ga.qcow2

You can use Horizon to import the QCOW2 image into OpenStack:

1. Go to *Compute* -> *Images*.
2. Click *Create Image*.
3. Provide the image's URL, as well as minimum RAM of 4GB and minimum disk space of 20GB.
4. Click *Create Image*. The QCOW2 file will be downloaded and imported into OpenStack.

### Step 2: Create a VM

From Horizon:

1.  Click *Launch Instance*.
2.  In the *Instance Name* field, provide a name for the VM that is going to be created.
3.  In the *Source* screen, select the Cloudify Manager image.
4.  From the *Flavor* screen, select a flavour that can accommodate the Cloudify Manager VM.
5.  From the *Networks* screen, select the network you'd like the Cloudify Manager to be a part of.
6.  From the *Security Groups* screen, add a security group that satisfies the prerequisites (see above).
7.  From the *Key Pair* screen, select a keypair to associate with the new VM.
8.  Launch the VM.

Back at the *Instances* view, associate a floating IP to the new VM (unless the VM is on a network that is routable from
within the machine you're accessing the manager from).

### Step 3: Access Cloudify Manager

Open a browser window to `http://<manager-ip-address>`. You will see the Cloudify Manager UI.

**NOTE**: You may need to associate a floating IP to the new VM first (depending on your network setup).

## Part 2: Bootstrapping a Manager

### Step 1: Create a VM

Create a virtual machine for installing the Cloudify Manager on.

* Make sure that you connect the VM to the `cloudify-management` security group.

### Step 2: Bootstrap

Use the instructions provided in the [Manager Bootstrapping lab](../manager-installation) to perform the bootstrap.

### Step 3: Upload plugins

Once bootstrapping is complete, upload the OpenStack plugin and Diamond-plugin packages:

```bash
cfy plugins upload -y http://www.getcloudify.org/spec/openstack-plugin/2.0.1/plugin.yaml http://repository.cloudifysource.org/cloudify/wagons/cloudify-openstack-plugin/2.0.1/cloudify_openstack_plugin-2.0.1-py27-none-linux_x86_64-centos-Core.wgn
cfy plugins upload -y http://www.getcloudify.org/spec/diamond-plugin/1.3.14/plugin.yaml http://repository.cloudifysource.org/cloudify/wagons/cloudify-diamond-plugin/1.3.14/cloudify_diamond_plugin-1.3.14-py27-none-linux_x86_64-centos-Core.wgn
```

## Part 3: Orchestrate Application

We will orchestrate Cloudify's "Hello World" application. The blueprints already exist on your CLI VM, under
`~/hello-world`.

### Step 1: Prepare CLI profile

Switch to a CLI profile that is configured to communicate with your manager.

*   If you are using a Cloudify Manager that has been bootstrapped using the instructions of "Part 2" above, then the
    profile already exists and is the currently "active" one.
*   If you are using a Cloudify Manager that has been created from an image, or a Cloudify Manager for which there's
    no CLI profile configured yet:

    ```bash
    cfy profiles use -t <manager's-ip-address> -u <manager-username> -p <manager-password> -t default_tenant
    ```

### Step 2: Prepare inputs file

Create a new YAML file, `~/hw-inputs.yaml`, to contain inputs for the Hello World application.
Looking at `~/hello-world/openstack-blueprint.yaml`, construct your inputs YAML file to contain values that
are relevant to your environment.

**NOTE**: as the blueprint is designed to use an existing keypair, you'll have to provide the private key file to the manager.
That is the purpose of the `private_key_path` input. Before continuing, you must ensure that the private key is available
*at the manager side*, in the location you specified in `private_key_path`.

### Step 3: Upload the blueprint, create a deployment, run install

```bash
cfy install ~/hello-world/openstack-blueprint.yaml -b helloworld -d helloworld -i ~/hw-inputs.yaml
```

### Step 4: Test the application

Get the floating IP address of the NodeJS node which was created on OpenStack, by retrieving the deployment's outputs:

```bash
cfy deployments outputs nc
```

Then browse to it (port 8080).

### Step 5: Cleanup

```bash
cfy executions start -d nc uninstall
cfy deployments delete nc
cfy blueprints delete nc
```
