# Lab: OpenStack Bootstrapping and Deployment

### Step 1: Download Manager Blueprints and Nodecellar

The blueprints may have already been downloaded during previous labs. If not:

```bash
cd ~/work
wget -O blueprints.zip https://github.com/cloudify-cosmo/cloudify-manager-blueprints/archive/3.2.zip
unzip blueprints.zip
```

To download the Nodecellar-Docker example:

```bash
wget -O nodecellar-docker.zip https://github.com/cloudify-cosmo/cloudify-nodecellar-docker-example/archive/3.2.zip
unzip nodecellar-docker.zip
```

### Step 2: Prepare `openstack_config.json`

Create a file named `~/openstack_config.json` according to the following template:

```bash
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
* `nova_url` and `neutron_url` are optional, and should only be used to explicitly override the Nova and/or Neutron URLs listed in Keystone.

### Step 3: Prepare `inputs.yaml`

```bash
cp cloudify-manager-blueprints-3.2/openstack-docker/inputs.yaml.template inputs-os.yaml
```

Then, edit `~/work/inputs-os.yaml` for your values.

*NOTE*: ensure that you assign unique names to the various resources (management network, router etc). While Cloudify supports using existing resources, the sample `openstack-docker` blueprint does not provide
the option to specify a value for the `use_existing_resource` property. Alternatively, copy the `openstack-docker.yaml` blueprint aside and edit it to include `use_existing_resource`.

### Step 4: Bootstrap the manager

```bash
cfy bootstrap --install-plugins -p cloudify-manager-blueprints-3.2/openstack-docker/openstack-docker.yaml -i inputs-os.yaml
```

### Step 5: Prepare nodecellar's blueprint

```bash
cp cloudify-nodecellar-docker-example-3.2/blueprint/cfy-openstack-inputs.json .
```

Then edit `cfy-openstack-inputs.json` to add the image ID and the flavor ID.

### Step 6: Upload the blueprint, create a deployment, run install

```bash
cfy blueprints upload -p cloudify-nodecellar-docker-example-3.2/blueprint/openstack.yaml -b ns-docker
cfy deployments create -d ns-docker -b ns-docker -i cfy-openstack-inputs.json
cfy executions start -d ns-docker -w install
```

### Step 7: Test the application

Find out the floating IP attached to the Compute node running NodeJS, and browse it: `http://<ip-address>:8080`.