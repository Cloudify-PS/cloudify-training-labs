# Lab 5: Deploying Docker Containers

### Step 1: Verify security group

The Docker container that is going to be installed, requires port 8080 to be open for inbound communications. Make sure that the VM, on which the container is going to be installed, is associated with a security group that allows this.

### Step 2: Edit `singlehost.yaml`

Edit the file `$LAB_ROOT/blueprint/singlehost.yaml` by replacing all strings beginning with `REPLACE_WITH` with correct values.

### Step 3: Edit `inputs.yaml`

Edit the file `$LAB_ROOT/blueprint/inputs.yaml` to contain values applicable to your environment.

### Step 4: Upload the blueprint, create a deployment and install

```bash
cfy blueprints upload -p $LAB_ROOT/blueprint/singlehost.yaml -b nc-docker
cfy deployments create -b nc-docker -d nc-docker -i $LAB_ROOT/blueprint/inputs.yaml
cfy executions start -d nc-docker -w install
```

### Step 5: Verify installation

Navigate to port 8080 on the public IP that is associated with the machine on which Nodecellar was installed. For example:

```
http://15.125.87.108:8080
```

You should be presented with the Node Cellar application.

### Step 6: Cleanup

```bash
cfy executions start -d nc-docker -w uninstall
cfy deployments delete -d nc-docker
cfy blueprints delete -b nc-docker
```