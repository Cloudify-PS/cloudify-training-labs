# Lab: Running NodeCellar Locally

*NodeCellar* is a sample application, created by Christophe Coenraets, which demonstrates the usage of various technologies
(Backbone.js, Node.js, MongoDB).

In this lab, we will use the Cloudify CLI to deploy NodeCellar on the same CLI machine, using a blueprint.

## Process

### Step 1: Download and extract the NodeCellar blueprints

```bash
cd ~
curl -L -o nodecellar.tar.gz https://github.com/Cloudify-PS/cloudify-nodecellar-example/archive/4.0-maint.tar.gz
mkdir nodecellar && cd nodecellar
tar -zxv --strip-components=1 -f ../nodecellar.tar.gz
```

### Step 2: Install the blueprint

```bash
cfy install local-blueprint.yaml
```

You should now see the CLI in action - iterating through the blueprint's nodes, creating them, starting them and
instantiating relationships.

```
...
2017-04-08 19:52:05.682  CFY <local> [nodecellar_6d9ggv] Starting node
2017-04-08 19:52:05.758  CFY <local> [nodecellar_6d9ggv.start] Sending task 'script_runner.tasks.run'
2017-04-08 19:52:05.797  CFY <local> [nodecellar_6d9ggv.start] Task started 'script_runner.tasks.run'
2017-04-08 19:52:05.799  LOG <local> [nodecellar_6d9ggv.start] INFO: Executing: /tmp/tmpdn7ujc-start-nodecellar-app.sh
2017-04-08 19:52:07.782  LOG <local> [nodecellar_6d9ggv.start] INFO: MongoDB is located at localhost:27017
2017-04-08 19:52:08.066  LOG <local> [nodecellar_6d9ggv.start] INFO: Starting nodecellar application on port 8080
2017-04-08 19:52:08.350  LOG <local> [nodecellar_6d9ggv.start] INFO: /tmp/a4aeecee-20be-4aa9-adee-01cc85d9ae93/nodejs/nodejs-binaries/bin/node /tmp/a4aeecee-20be-4aa9-adee-01cc85d9ae93/nodecellar/nodecellar-source/server.js
2017-04-08 19:52:08.934  LOG <local> [nodecellar_6d9ggv.start] INFO: Running Nodecellar liveness detection on port 8080
2017-04-08 19:52:09.426  LOG <local> [nodecellar_6d9ggv.start] INFO: [GET] http://localhost:8080 200
2017-04-08 19:52:09.990  LOG <local> [nodecellar_6d9ggv.start] INFO: Sucessfully started Nodecellar (9915)
2017-04-08 19:52:10.091  LOG <local> [nodecellar_6d9ggv.start] INFO: Execution done (return_code=0): /tmp/tmpdn7ujc-start-nodecellar-app.sh
2017-04-08 19:52:10.092  CFY <local> [nodecellar_6d9ggv.start] Task succeeded 'script_runner.tasks.run'
2017-04-08 19:52:10.685  CFY <local> 'install' workflow execution succeeded
```

### Step 3: Test the application

The application is now installed. Point your browser to `http://<cli-vm-public-ip>:8080` and you should see
the NodeCellar application.

Also, run the following command:

```bash
cfy deployments outputs
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
cfy uninstall
```

That will run the `uninstall` built-in workflow, which calls the `stop` and `delete` operations on all nodes, while
also calling `unlink` on all relationships.
