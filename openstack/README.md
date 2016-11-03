# Lab: OpenStack Bootstrapping and Deployment

### Step 1: Download Manager blueprints and NodeCellar blueprints

The blueprints may have already been downloaded during previous labs. If not:

```bash
cd ~/work
curl -L -o manager-blueprints.zip https://github.com/cloudify-cosmo/cloudify-manager-blueprints/archive/3.4.0.2.zip
unzip manager-blueprints.zip
mv cloudify-manager-blueprints-3.4 cloudify-manager-blueprints

curl -L -o nodecellar.zip https://github.com/Cloudify-PS/cloudify-nodecellar-example/archive/3.4-maint.zip
unzip nodecellar.zip
mv cloudify-nodecellar-example-3.4-maint/ cloudify-nodecellar-example
```

### Step 2: Prepare `inputs.yaml`

From your CLI machine:

```bash
cd ~/work
cp ../cloudify-manager-blueprints/openstack-manager-blueprint-inputs.yaml inputs-os.yaml
```

Then, edit `~/work/inputs-os.yaml` for your values. In particular:

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

### Step 4: Prepare nodecellar's blueprint

```bash
cp ../cloudify-nodecellar-example/inputs/openstack.yaml.template ./nc-os-inputs.yaml
```

Then edit `nc-os-inputs.yaml`:

```yaml
image: <image-id>
flavor: <flavor-id>
agent_user: centos
```

### Step 5: Upload the blueprint, create a deployment, run install

```bash
cfy blueprints upload -p ../cloudify-nodecellar-example/openstack-blueprint.yaml -b nc-os
cfy deployments create -b nc-os -d nc-os -i nc-os-inputs.yaml
cfy executions start -d nc-os -w install -l
```

### Step 6: Test the application

Get the floating IP address of the NodeJS node which was created on OpenStack, by retrieving the deployment's outputs:

```bash
cfy deployments outputs -d nc-os
```

Then browse to it (port 8080).

### Step 7: Cleanup

```bash
cfy executions start -d nc-os -w uninstall -l
cfy deployments delete -d nc-os
cfy blueprints delete -b nc-os
```
