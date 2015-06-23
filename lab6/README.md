# Lab 6: Using Scripts in Lifecycle Events

The purpose of this lab is to fix a broken blueprint, install it locally and also upload it a Cloudify Manager.

It is assumed that the `LAB_ROOT` environment variable points to the exercise's root directory. Otherwise, export it:

```bash
export LAB_ROOT=~/cloudify-training-labs/lab6/exercise
```

### Step 1: Replace placeholders

You need to replace **_all_** the occurrences of the placeholders (“`REPLACE_WITH`”) wherever they are located under `$LAB_ROOT`, with the suitable values and to add missing parts as well.

### Step 2: Run in local mode

Once you're done, you can run the application in local mode:

```bash
cd ~/work
cfy local init -p $LAB_ROOT/hello-tomcat/tomcat-blueprint.yaml -i $LAB_ROOT/hello-tomcat/tomcat-local.yaml
cfy local execute -w install
```

Now browse to `http://127.0.0.1:8080/helloworld` (from the CLI machine, or `http://<cli-machine-public-ip>/helloworld` from elsewhere) and then run the following CLI command:

```bash
cfy local outputs
```

To clean up:

```bash
cfy local execute -w uninstall
```

### Step 3: Existing manager

Upload the blueprint to the existing Cloudify manager, created in previous labs:

```bash
cd ~/work
cfy blueprints upload -p $LAB_ROOT/hello-tomcat/tomcat-blueprint.yaml -b hellotomcat
cfy deployments create -b hellotomcat -d hellotomcat -i $LAB_ROOT/hello-tomcat/tomcat.yaml
cfy executions start -d hellotomcat -w install
```

Notes:

1. For the `deployments create` command, we used a different YAML file for inputs, than we used for running locally.
2. The blueprint is uploaded under the name `hellotomcat`. The deployment created is also named `hellotomcat`. That is *not* a requirement; the deployment's name may be different from its associated blueprint's name.

To test, navigate to port 8080 of the public IP associated with the VM on which installation was made:

```
http://15.125.87.108:8080
```

### Step 4: Cleanup

In order to clean up:

1. Uninstall the application.
2. Remove the `hellotomcat` deployment.
3. Remove the `hellotomcat` blueprint.

```bash
cfy executions start -d hellotomcat -w uninstall
cfy deployments delete -d hellotomcat
cfy blueprints delete -b hellotomcat
```