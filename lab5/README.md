# Lab 5: Deploying Docker Containers

In this lab, we will demonstrate how to deploy and install a Docker container. We will use a Docker version of the Nodecellar application introduced in previous labs.

It is assumed that the lab's files are extracted into `$LAB_ROOT`.

### Step 1: Edit `singlehost.yaml`

Edit the file `$LAB_ROOT/blueprint/singlehost.yaml` by replacing all strings beginning with `REPLACE_WITH` with correct values.

### Step 2: Edit `inputs.yaml`

Edit the file `$LAB_ROOT/blueprint/inputs.yaml` to contain values applicable to your environment.

### Step 3: Upload the blueprint, create a deployment and install

```bash
cfy blueprints upload -p $LAB_ROOT/blueprint/singlehost.yaml -b nc-docker
cfy deployments create -b nc-docker -d nc-docker -i $LAB_ROOT/blueprint/inputs.yaml
cfy executions start -d nc-docker -w install
```

### Step 4: Verify installation

Navigate to port 8080 on the public IP that is associated with the machine on which Nodecellar was installed. For example:

```
http://15.125.87.108:8080
```

You should be presented with the Nodecellar application.

### Step 5: Cleanup

```bash
cfy executions start -d nc-docker -w uninstall
cfy deployments delete -d nc-docker
cfy blueprints delete -b nc-docker
```