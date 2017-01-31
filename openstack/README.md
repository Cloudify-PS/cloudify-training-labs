# Lab: Working with OpenStack

In this lab, we will create a Cloudify Manager installation, upload a blueprint to it, create a deployment and install it.

There are two methods for creating a Cloudify Manager installation:

* Via a provided image (recommended)
* Via bootstrapping

Both approaches will be covered in this lab. You may choose to practice either, or both.

## Part 1: Creating a Cloudify Manager from an Image

### Step 1: Import the Cloudify Manager image to OpenStack

The official Cloudify Manager image is located at: http://repository.cloudifysource.org/org/cloudify3/3.4.0/ga-RELEASE/manager3.4_insecure_image.qcow2

You can use Horizon to import the QCOW2 image into OpenStack:

1. Go to *Compute* -> *Images*.
2. Click *Create Image*.
3. Provide the image's URL, as well as minimum RAM of 4GB and minimum disk space of 20GB.
4. Click *Create Image*. The QCOQ2 file will be downloaded and imported into OpenStack.

### Step 2: Prepare networking prerequisites

The [Cloudify Manager prerequisites page](http://docs.getcloudify.org/3.4.1/manager/prerequisites/) describes a few
networking- & security-related prerequisites. You will have to ensure that you have the following:

* A security group that allows access to the manager via the ports specified in the Prerequisites page:
  * Ports 80, 443 and 22 from anywhere.
  * Ports 5672, 53229 and 8101 from any VM that is going to be managed by Cloudify and has the Cloudify Agent installed on it.
* A security group that allows access to agents, as specified in the [Agent prerequisites description](http://docs.getcloudify.org/3.4.1/agents/overview/).
* A network to connect the Cloudify Manager to.
* A keypair to use for SSH'ing into the Cloudify Manager VM.

### Step 3: Create a VM

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

### Step 4: Configure Cloudify Manager

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
        "openstack_auth_url": "",
        "user_ssh_key": "none",
        "agents_security_group_name": "cfy-agents",
        "openstack_region": "RegionOne",
        "openstack_password": "my_password",
        "agents_to_manager_inbound_ports": "5672,8101,53229",
        "openstack_tenant_name": "my_tenant",
        "agents_user": "centos",
        "openstack_username": "my_username",
        "agents_keypair_name": "cfy-agents-key"
    }
    ```
3.  Click *Create*.
4.  Click the *Execute Workflow* button.
5.  Select *install* and click *Confirm*.

## Part 2: Bootstrapping a Manager

### Step 1: Download Manager blueprints and NodeCellar blueprints

The blueprints may have already been downloaded during previous labs. If not:

```bash
cd ~
curl -L -o manager-blueprints.zip https://github.com/cloudify-cosmo/cloudify-manager-blueprints/archive/3.4.1.zip
unzip manager-blueprints.zip
mv cloudify-manager-blueprints-3.4.1 cloudify-manager-blueprints
```

### Step 2: Prepare `inputs.yaml`

```bash
cd ~/mgr
cp ../cloudify-manager-blueprints/openstack-manager-blueprint-inputs.yaml inputs-os.yaml
```

Then, edit `~/mgr/inputs-os.yaml` for your values. In particular:

*   **`keystone_username`**: for authenticating against KeyStone
*   **`keystone_password`**: for authenticating against KeyStone
*   **`keystone_tenant_name`**: the OpenStack tenant name to use
*   **`keystone_url`**: the URL to use when contacting KeyStone
*   **`region`**: the region to use (optional, if there is only one region defined)
*   **`skip_openstack_cert_verification`**: set to `true` if your OpenStack endpoints are accessed by HTTPS, *and* expose a certificate that is not trusted by any certificate authority installed on the machine from where the bootstrap runs.
*   **`ssh_key_filename`**: should point to the location where the private key, used to connect to the new manager VM, should be stored.
*   **`agent_private_key_path`**: should point to the location where the private key, used *by default* to connect to newly-created VM's, should be stored.
*   **`manager_public_key_name`**: should be the name to assign to the new keypair created to access the Cloudify Manager VM.
*   **`agent_public_key_name`**: should be the name to assign to the new keypair that Cloudify will use to log into VM's in order to install the Cloudify Agent.
*   **`image_id`**: should contain the ID of the image to use for the manager's VM's creation. This must be either a CentOS 7.0 or RHEL 7.0 image.
*   **`flavor_id`**: should contain the ID of the flavour to use for the manager's VM's creation.
*   **`external_network_name`**: should contain the name (not the ID) of OpenStack's external network.
*   **`ssh_user`**: should contain the username that is used to connect to the new manager's VM. For CentOS 7.0 images, this is usually `centos`.
*   **`agents_user`**: is the username that is used, *by default*, to connect to VM's that Cloudify Manager creates, in order to install the Cloudify Agent. As we only deal with CentOS VM's during the training course, you should set this value to `centos`.
*   **`management_subnet_dns_nameservers`** should normally stay an empty list; however, if your OpenStack environment is not configured to provide default DNS servers, then this input should contain a list of DNS nameservers to use. Otherwise, the manager won't be able to access the external network to download artifacts. (While Cloudify can also operate in a completely offline mode, this subject is not covered in the basic training curriculum)

### Step 3: Bootstrap the manager

```bash
cfy bootstrap --install-plugins -p ../cloudify-manager-blueprints/openstack-manager-blueprint.yaml -i inputs-os.yaml
```

## Part 3: NodeCellar

NodeCellar may also have been downloaded previously. If not:

```bash
cd ~
curl -L -o nodecellar.zip https://github.com/Cloudify-PS/cloudify-nodecellar-example/archive/3.4.1-maint.zip
unzip nodecellar.zip
mv cloudify-nodecellar-example-3.4.1-maint cloudify-nodecellar-example
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
cp ../cloudify-nodecellar-example/inputs/openstack.yaml.template ./nc-os-inputs.yaml
```

Then edit `nc-os-inputs.yaml`:

```yaml
image: <image-id>
flavor: <flavor-id>
agent_user: centos
```

### Step 3: Upload the blueprint, create a deployment, run install

```bash
cfy blueprints upload -p ../cloudify-nodecellar-example/openstack-blueprint.yaml -b nc-os
cfy deployments create -b nc-os -d nc-os -i nc-os-inputs.yaml
cfy executions start -d nc-os -w install -l
```

### Step 4: Test the application

Get the floating IP address of the NodeJS node which was created on OpenStack, by retrieving the deployment's outputs:

```bash
cfy deployments outputs -d nc-os
```

Then browse to it (port 8080).

### Step 5: Cleanup

```bash
cfy executions start -d nc-os -w uninstall -l
cfy deployments delete -d nc-os
cfy blueprints delete -b nc-os
```
