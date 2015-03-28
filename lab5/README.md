# Lab 5: Bootstrapping a Docker Manager and Deploying Docker Containers

## Section A: Bootstrapping a Docker Manager

```bash
cd ~/work
```

Also, ensure that the machine on which the manager is going to be bootstrapped, is configured so the user - under which
bootstrapping is being done - is not prompted for a password when executing `sudo` commands.

sudo apt-get update
sudo apt-get install -y docker.io
### Step 1: Prepare `inputs.yaml`

You may have an `inputs.yaml` file ready from an earlier lab, where you had bootstrapped a manager using the `simple` blueprint.
As the `simple-docker` blueprint uses exactly the same inputs, you may reuse the existing file. Otherwise:

```bash
cp cloudify-manager-blueprints-3.2/simple/inputs.yaml.template ./inputs.yaml
```

And then edit `inputs.yaml` with the appropriate values.

```bash
```
### Step 2: Bootstrap the manager

```bash
cfy init -r
cfy bootstrap --install-plugins -p cloudify-manager-blueprints-3.2/simple/simple-docker.yaml -i inputs.yaml
cfy status
```

The `cfy status` command should display all of Cloudify's components as `up`.

Log into the manager by `ssh`ing to it, and then:

```bash
sudo docker ps
```

You will get a list of Docker containers. Note the container's name - should be `cfy`.
Use the Docker command-line utility to view the manager's logs:

```bash
sudo docker logs cfy
```

## Section B: Deploying Docker Containers

### Step 3: Edit `singlehost.yaml`

Edit the file `LAB_ROOT/blueprint/singlehost.yaml` by replacing all strings beginning with `REPLACE_WITH` with correct values.

### Step 4: Upload the blueprint, create a deployment and install

```bash
cfy blueprints upload -p LAB_ROOT/blueprints/singlehost.yaml -b nc-docker
cfy deployments create -b nc-docker -d nc-docker
cfy executions start -d nc-docker -w install
```



cfy deployments create -b hellotomcat-mon -d hellotomcat-mon -i LAB_ROOT/hello-tomcat/tomcat.yaml
cfy executions start -d hellotomcat-mon -w install





## Section B: Deploying Docker Containers