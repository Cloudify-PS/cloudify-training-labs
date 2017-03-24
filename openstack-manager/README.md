# Lab: Cloudify Manager and OpenStack

In this lab, we will create a Cloudify Manager, upload a blueprint to it, create a deployment and install it.

There are two methods for creating a Cloudify Manager:

* Via a provided image (recommended)
* Via bootstrapping

Both approaches will be covered in this lab. You may choose to practice either, or both.

## Part 1: Preparations

The [Cloudify Manager prerequisites page](http://docs.getcloudify.org/3.4.2/manager/prerequisites/) describes a few
networking- and security-related prerequisites. You will have to ensure that you have the following:

* A security group that allows access to the manager via the ports specified in the Prerequisites page:
  * Ports 80, 443 and 22, with the source being any address / CIDR / security group that you'd like to access
    Cloudify Manager from.
  * Ports 5672, 53229 and 8101 from any VM that:
    * Is going to be created by Cloudify; and
    * Is going to have the Cloudify Agent installed on it.
* A security group that allows access to agents, as specified in the [Agent prerequisites description](http://docs.getcloudify.org/3.4.2/agents/overview/).
* A network to connect the Cloudify Manager to.
* A keypair to use for SSH'ing into the Cloudify Manager VM.

**TIP**: For maximum flexibility, consider setting the security groups up as follows:

* Create a security group for Cloudify management (for example's sake, we will refer to it as `cloudify-management`).
* Create a security group for Cloudify agents (`cloudify-agents`).
* Edit `cloudify-management`'s rules, allowing:
    * Ports 80, 443 and 22 from anywhere (in production systems, you will most likely want to restrict this by CIDR or
      a security group).
    * Ports 5672, 53229 and 8101 from the security group `cloudify-agents`.
* Edit `cloudify-agents`'s rules, allowing:
    * Ports 22 and 5985 from the security group `cloudify-management`.

The advantage in this security groups setup is that no CIDR masks are involved in security group rules for the purpose
of enabling agent <-> manager communication.

## Part 2: Creating a Cloudify Manager from an Image

### Step 1: Import the Cloudify Manager image to OpenStack

The official Cloudify Manager image is located at: http://repository.cloudifysource.org/org/cloudify3/3.4.2/sp-RELEASE/manager3.4.2-insecure-image.qcow2

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

### Step 3: Configure Cloudify Manager

Open a browser window to `http://<manager-ip-address>`. You will see the Cloudify Manager UI, showing a single blueprint called `CloudifySettings`.

1.  Click *Create Deployment*.
2.  Populate the fields as follows:

    | Field                             | Value                                                                                     |
    |-----------------------------------|-------------------------------------------------------------------------------------------|
    | Deployment Name                   | `settings`                                                                                |
    | `openstack_auth_url`              | Default OpenStack KeyStone URL                                                            |
    | `user_ssh_key`                    | `none`                                                                                    |
    | `agents_security_group`           | Name of security group to create, and that will be automatically associated with new VM's |
    | `openstack_region`                | Default OpenStack region                                                                  |
    | `openstack_password`              | Default OpenStack password                                                                |
    | `agents_to_manager_inbound_ports` | *leave default*                                                                           |
    | `openstack_tenant_name`           | Default OpenStack tenant                                                                  |
    | `agents_user`                     | *leave default*                                                                           |
    | `openstack_username`              | Default OpenStack username                                                                |
    | `agents_keypair_name`             | Name of keypair to create, and that will be associated with new VM's                      |

    As an alternative, you can provide all values as a JSON blob, by selecting the *RAW* button and pasting the JSON.
    For example:
    
    ```json
    {
        "openstack_auth_url": "https://Openstack_MANAGEMENT_IP:5000/v3",
        "user_ssh_key": "none",
        "agents_security_group_name": "cfy-agents",
        "openstack_region": "RegionOne",
        "openstack_password": "my_openstack_password",
        "agents_to_manager_inbound_ports": "5672,8101,53229",
        "openstack_tenant_name": "my_tenant",
        "agents_user": "centos",
        "openstack_username": "my_openstack_username",
        "agents_keypair_name": "cfy-agents-key"
    }
    ```
3.  Click *Create*.
4.  Click the *Execute Workflow* button.
5.  Select *install* and click *Confirm*.

## Part 2: Bootstrapping a Manager

### Step 1: Create a VM

Create a virtual machine for installing the Cloudify Manager on.

* Make sure that you connect the VM to the `cloudify-management` security group.

### Step 2: Bootstrap

Use the instructions provided in the [Manager Bootstrapping lab](../simple-bootstrap) to perform the bootstrap.
 
## Part 3: NodeCellar

NodeCellar may also have been downloaded previously. If not:

```bash
cd ~
curl -L -o nodecellar.zip https://github.com/Cloudify-PS/cloudify-nodecellar-example/archive/3.4.2-maint.zip
unzip nodecellar.zip
mv cloudify-nodecellar-example-3.4.2-maint cloudify-nodecellar-example
```

### Step 1: Switch to a Cloudify directory

If you are using a Cloudify Manager that has been bootstrapped, switch to the directory from which you performed
the bootstrap process (`~/mgr`, unless you deviated from the aforementioned instructions).

If you are using a Cloudify Manager that has been created from an image, create a new directory somewhere, switch
to it, and type:

```bash
cfy use -t <manager's-ip-address>
```

### Step 2: Prepare nodecellar's blueprint

```bash
cp ../cloudify-nodecellar-example/inputs/openstack.yaml.template ./nc-inputs.yaml
```

Then edit `nc-inputs.yaml`:

```yaml
image: <image-id>
flavor: <flavor-id>
agent_user: centos
```

### Step 3: Upload the blueprint, create a deployment, run install

```bash
cfy blueprints upload -p ../cloudify-nodecellar-example/openstack-blueprint.yaml -b nc
cfy deployments create -b nc -d nc -i nc-inputs.yaml
cfy executions start -d nc -w install -l
```

### Step 4: Test the application

Get the floating IP address of the NodeJS node which was created on OpenStack, by retrieving the deployment's outputs:

```bash
cfy deployments outputs -d nc
```

Then browse to it (port 8080).

### Step 5: Cleanup

```bash
cfy executions start -d nc -w uninstall -l
cfy deployments delete -d nc
cfy blueprints delete -b nc
```
