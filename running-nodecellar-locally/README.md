# Lab: Running NodeCellar Locally

*NodeCellar* is a sample application, created by Christophe Coenraets, which demonstrates the usage of various technologies
(Backbone.js, Node.js, MongoDB).

In this lab, we will use the Cloudify CLI to deploy NodeCellar on the same CLI machine, using a blueprint.

## Process

### Step 1: Download and extract the NodeCellar blueprints

```bash
cd ~
curl -L -o nodecellar.zip https://github.com/cloudify-cosmo/cloudify-nodecellar-example/archive/3.3.1.zip
unzip nodecellar.zip
```

### Step 2: Initialize your working directory

```bash
cd ~/cfylocal
cfy local init -p ../cloudify-nodecellar-example-3.3.1/local-blueprint.yaml
```

That will initialize the current directory with the blueprint data:

```
Initiated ../cloudify-nodecellar-example-3.3.1/local-blueprint.yaml
If you make changes to the blueprint, run 'cfy local init -p ../cloudify-nodecellar-example-3.3.1/local-blueprint.yaml' again to apply them
```

### Step 3: Run the `install` workflow

```bash
cfy local execute -w install
```

You should now see the CLI in action - iterating through the blueprint's nodes, creating them, starting them and
instantiating relationships.

```
...
2016-01-29 04:40:18 LOG <local> [nodecellar_2dc99.start] INFO: Sucessfully started Nodecellar (2960)
2016-01-29 04:40:18 LOG <local> [nodecellar_2dc99.start] INFO: Execution done (return_code=0): /tmp/tmpxkdjeq-start-nodecellar-app.sh
2016-01-29 04:40:18 CFY <local> [nodecellar_2dc99.start] Task succeeded 'script_runner.tasks.run'
2016-01-29 04:40:19 CFY <local> 'install' workflow execution succeeded
```

### Step 4: Test the application

The application is now installed. Point your browser to `http://<cli-vm-public-ip>:8080` and you should see
the NodeCellar application.

Also, run the following command:

```bash
cfy local outputs
```

This command will calculate the value of the `outputs` structure in the blueprint, and print it out.

```
{
  "endpoint": {
    "ip_address": "localhost",
    "port": 8080
  }
}
```

### Step 5: Run the `uninstall` workflow

```bash
cfy local execute -w uninstall
```

That will run the `uninstall` built-in workflow, which calls the `stop` and `delete` operations on all nodes, while
also calling `unlink` on all relationships.
