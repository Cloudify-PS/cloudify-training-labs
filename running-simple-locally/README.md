# Lab: Running Simple Blueprint Locally

In this lab, we will use the Cloudify CLI to deploy a simple application using a blueprint.

## Process

### Step 1: Download and extract the sample blueprint

```bash
mkdir ~/work && cd ~/work
curl -L -o sample-blueprint.zip https://github.com/cloudify-examples/simple-python-webserver-blueprint/archive/master.zip
unzip sample-blueprint.zip
mv simple-python-webserver-blueprint-master simple-python-webserver-blueprint
```

### Step 2: Initialize your working directory

```bash
mkdir -p ~/work/cfylocal && cd ~/work/cfylocal
cfy local init -p ../simple-python-webserver-blueprint/blueprint.yaml
```

That will initialize the current directory with the blueprint data:

```
Initiated ../simple-python-webserver-blueprint/blueprint.yaml
If you make changes to the blueprint, run `cfy local init -p ../simple-python-webserver-blueprint/blueprint.yaml` again to apply them
```

### Step 3: Run the `install` workflow

```bash
cfy local execute -w install
```

You should now see the CLI in action - iterating through the blueprint's nodes, creating them, starting them and
instantiating relationships.

```
2016-06-09 07:21:38 CFY <local> Starting 'install' workflow execution
2016-06-09 07:21:38 CFY <local> [host_85727] Creating node
2016-06-09 07:21:38 CFY <local> [host_85727] Configuring node
2016-06-09 07:21:39 CFY <local> [host_85727] Starting node
2016-06-09 07:21:40 CFY <local> [http_web_server_b98c7] Creating node
2016-06-09 07:21:40 CFY <local> [http_web_server_b98c7.create] Sending task 'script_runner.tasks.run'
2016-06-09 07:21:40 CFY <local> [http_web_server_b98c7.create] Task started 'script_runner.tasks.run'
2016-06-09 07:21:40 LOG <local> [http_web_server_b98c7.create] INFO: Running WebServer locally on port: 8000
2016-06-09 07:21:40 LOG <local> [http_web_server_b98c7.create] INFO: Setting `pid` runtime property: 2079
2016-06-09 07:21:40 CFY <local> [http_web_server_b98c7.create] Task succeeded 'script_runner.tasks.run'
2016-06-09 07:21:40 CFY <local> [http_web_server_b98c7] Configuring node
2016-06-09 07:21:41 CFY <local> [http_web_server_b98c7] Starting node
2016-06-09 07:21:41 CFY <local> 'install' workflow execution succeeded
```

### Step 4: Test the application

The sample HTTP server is now installed. Point your browser to `http://<cli-vm-public-ip>:8000` to verify.

Also, run the following command:

```bash
cfy local outputs
```

This command will calculate the value of the `outputs` structure in the blueprint, and print it out.

```
{
  "http_endpoint": "http://localhost:8000"
}
```

### Step 5: Run the `uninstall` workflow

```bash
cfy local execute -w uninstall
```

That will run the `uninstall` built-in workflow, which calls the `stop` and `delete` operations on all nodes, while
also calling `unlink` on all relationships.
