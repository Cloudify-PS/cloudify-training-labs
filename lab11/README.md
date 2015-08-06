# Lab 11: OpenStack Bootstrapping and Deployment

### Step 1: Download Manager Blueprints and Nodecellar-Docker

The blueprints may have already been downloaded during previous labs. If not:

```bash
cd ~/work
wget -O blueprints.zip https://github.com/cloudify-cosmo/cloudify-manager-blueprints/archive/3.2.1.zip
unzip blueprints.zip
```

To download the Nodecellar-Docker example:

```bash
wget -O nodecellar-docker.zip https://github.com/cloudify-cosmo/cloudify-nodecellar-docker-example/archive/3.2.1.zip
unzip nodecellar-docker.zip
```

### Step 2: Prepare `openstack_config.json`

Create a file named `~/openstack_config.json` according to the following template:

```yaml
{
    "username": "your-keystone-username",
    "password": "your-keystone-password",
    "tenant_name": "openstack-tenant-name",
    "auth_url": "keystone-url",
    "region": "region-code",
    "nova_url": "nova-service-url",
    "neutron_url": "neutron-service-url"
}
```

Notes:

* `region` is optional in environments where only one region is available
* `nova_url` and `neutron_url` are optional, and should only be used in cases when it is required to override the Nova and/or Neutron URLs provided by Keystone.

### Step 3: Prepare `inputs.yaml`

```bash
cp cloudify-manager-blueprints-3.2.1/openstack/inputs.yaml.template inputs-os.yaml
```

Then, edit `~/work/inputs-os.yaml` for your values.

**NOTE**: ensure that you assign unique names to the various resources (management network, router etc). While Cloudify supports using existing resources, the sample `openstack-manager-blueprint` does not provide the option to specify a value for the `use_external_resource` property. Alternatively, you can copy `openstack-manager-blueprint.yaml` aside and edit it to include `use_external_resource` wherever necessary.

### Step 4: Bootstrap the manager

```bash
cfy bootstrap --install-plugins -p cloudify-manager-blueprints-3.2.1/openstack/openstack-manager-blueprint.yaml -i inputs-os.yaml
```

### Step 5: Prepare nodecellar's blueprint

```bash
cp cloudify-nodecellar-docker-example-3.2.1/blueprint/cfy-openstack-inputs.json .
```

Then edit `cfy-openstack-inputs.json` to add the image ID and the flavor ID of the image on which you want Node Cellar to be installed.

### Step 6: Upload the blueprint, create a deployment, run install

```bash
cfy blueprints upload -p cloudify-nodecellar-docker-example-3.2.1/blueprint/openstack.yaml -b nc-docker-os
cfy deployments create -d nc-docker-os -b nc-docker-os -i cfy-openstack-inputs.json
cfy executions start -d nc-docker-os -w install
```

### Step 7: Test the application

Find out the floating IP attached to the Compute node running Node Cellar, and browse it: `http://<ip-address>:8080`.


### Step 8: Cleanup

```bash
cfy executions start -d nc-docker-os -w uninstall
cfy deployments delete -d nc-docker-os
cfy blueprints delete -b nc-docker-os
```