# Lab: Running NodeCellar Locally

*NodeCellar* is a sample application, created by Christophe Coenraets, which demonstrates the usage of various technologies
(Backbone.js, Node.js, MongoDB).

In this lab, we will use the Cloudify CLI to deploy NodeCellar on the same CLI machine, using a blueprint.

## Process

### Step 1: Download and extract the NodeCellar blueprints

```bash
cd ~
curl -L -o nodecellar.zip https://github.com/Cloudify-PS/cloudify-nodecellar-example/archive/3.4.1-maint.zip
unzip nodecellar.zip
mv cloudify-nodecellar-example-3.4.1-maint cloudify-nodecellar-example
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
2017-01-29 01:22:02 CFY <local> [nodecellar_upikj8] Starting node
2017-01-29 01:22:02 CFY <local> [nodecellar_upikj8.start] Sending task 'script_runner.tasks.run'
2017-01-29 01:22:02 CFY <local> [nodecellar_upikj8.start] Task started 'script_runner.tasks.run'
2017-01-29 01:22:02 LOG <local> [nodecellar_upikj8.start] INFO: Executing: /tmp/tmpt_cMld-start-nodecellar-app.sh
2017-01-29 01:22:04 LOG <local> [nodecellar_upikj8.start] INFO: MongoDB is located at localhost:27017
2017-01-29 01:22:05 LOG <local> [nodecellar_upikj8.start] INFO: Starting nodecellar application on port 8080
2017-01-29 01:22:05 LOG <local> [nodecellar_upikj8.start] INFO: /tmp/19e4adc5-9939-4a45-af0d-6df517283823/nodejs/nodejs-binaries/bin/node /tmp/19e4adc5-9939-4a45-af0d-6df517283823/nodecellar/nodecellar-source/server.js
2017-01-29 01:22:06 LOG <local> [nodecellar_upikj8.start] INFO: Running Nodecellar liveness detection on port 8080
2017-01-29 01:22:06 LOG <local> [nodecellar_upikj8.start] INFO: [GET] http://localhost:8080 200
2017-01-29 01:22:07 LOG <local> [nodecellar_upikj8.start] INFO: Sucessfully started Nodecellar (9761)
2017-01-29 01:22:07 LOG <local> [nodecellar_upikj8.start] INFO: Execution done (return_code=0): /tmp/tmpt_cMld-start-nodecellar-app.sh
2017-01-29 01:22:07 CFY <local> [nodecellar_upikj8.start] Task succeeded 'script_runner.tasks.run'
2017-01-29 01:22:07 CFY <local> 'install' workflow execution succeeded
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
