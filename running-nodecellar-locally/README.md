# Lab: Running NodeCellar Locally

*NodeCellar* is a sample application, created by Christophe Coenraets, which demonstrates the usage of various technologies
(Backbone.js, Node.js, MongoDB).

In this lab, we will use the Cloudify CLI to deploy NodeCellar on the same CLI machine, using a blueprint.

## Process

### Step 1: Download and extract the NodeCellar blueprints

```bash
cd ~
curl -L -o nodecellar.zip https://github.com/Cloudify-PS/cloudify-nodecellar-example/archive/3.4-maint.zip
unzip nodecellar.zip
mv cloudify-nodecellar-example-3.4-maint cloudify-nodecellar-example
```

### Step 2: Install the blueprint

```bash
cd ~/cfylocal
cfy local install -p ../cloudify-nodecellar-example/local-blueprint.yaml
```

You should now see the CLI in action - iterating through the blueprint's nodes, creating them, starting them and
instantiating relationships.

```
...
2016-06-15 17:28:02 CFY <local> [nodecellar_7f2bb] Starting node
2016-06-15 17:28:02 CFY <local> [nodecellar_7f2bb.start] Sending task 'script_runner.tasks.run'
2016-06-15 17:28:02 CFY <local> [nodecellar_7f2bb.start] Task started 'script_runner.tasks.run'
2016-06-15 17:28:02 LOG <local> [nodecellar_7f2bb.start] INFO: Executing: /tmp/tmpQXZZRp-start-nodecellar-app.sh
2016-06-15 17:28:04 LOG <local> [nodecellar_7f2bb.start] INFO: MongoDB is located at localhost:27017
2016-06-15 17:28:04 LOG <local> [nodecellar_7f2bb.start] INFO: Starting nodecellar application on port 8080
2016-06-15 17:28:04 LOG <local> [nodecellar_7f2bb.start] INFO: /tmp/ee4c9789-8292-413a-83c0-9f3fee4cda36/nodejs/nodejs-binaries/bin/node /tmp/ee4c9789-8292-413a-83c0-9f3fee4cda36/nodecellar/nodecellar-source/server.js
2016-06-15 17:28:05 LOG <local> [nodecellar_7f2bb.start] INFO: Running Nodecellar liveness detection on port 8080
2016-06-15 17:28:05 LOG <local> [nodecellar_7f2bb.start] INFO: [GET] http://localhost:8080 200
2016-06-15 17:28:06 LOG <local> [nodecellar_7f2bb.start] INFO: Sucessfully started Nodecellar (9881)
2016-06-15 17:28:06 LOG <local> [nodecellar_7f2bb.start] INFO: Execution done (return_code=0): /tmp/tmpQXZZRp-start-nodecellar-app.sh
2016-06-15 17:28:06 CFY <local> [nodecellar_7f2bb.start] Task succeeded 'script_runner.tasks.run'
2016-06-15 17:28:07 CFY <local> 'install' workflow execution succeeded
```

### Step 3: Test the application

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

### Step 4: Uninstall the application

```bash
cfy local uninstall
```

That will run the `uninstall` built-in workflow, which calls the `stop` and `delete` operations on all nodes, while
also calling `unlink` on all relationships.
