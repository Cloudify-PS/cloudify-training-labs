# Lab: Installing NodeCellar on Cloudify Manager

The purpose of this lab is to upload a sample blueprint to the Manager you had bootstrapped previously, create a deployment for it and install it on the same VM as the manager.

The blueprint we are going to work with, will install a sample application called *NodeCellar* (if you are
currently going through the full training schedule, this is the same application introduced in a previous lab:
"Running NodeCellar Locally". The only difference is that we are going to use a different blueprint for
installing this application).
 
## Step 1: Download the NodeCellar blueprints

**NOTE**: You may already have downloaded the blueprints in an earlier lab. If you have, then please skip
this step.

```bash
cd ~
curl -L -o nodecellar.tar.gz https://github.com/Cloudify-PS/cloudify-nodecellar-example/archive/4.0-maint.tar.gz
mkdir nodecellar && cd nodecellar
tar -zxv --strip-components=1 -f ../nodecellar.tar.gz
```

That will download the latest NodeCellar application and its blueprints, and extract them into `~/nodecellar`.

## Step 2: Copy private key to the Manager's VM

The blueprint that we are going to install, instructs Cloudify to install the example application on existing VMs.
Cloudify, therefore, needs access to the private key used to log into these VMs.

(Run this from the CLI machine)

```bash
scp -i ~/cfy-training.pem ~/cfy-training.pem centos@<manager-ip>:~/
ssh -i ~/cfy-training.pem centos@<manager-ip> 'sudo mv cfy-training.pem /root'
```

## Step 3: Configure the inputs file

The NodeCellar archive contains a template for a blueprints inputs file. This template should be edited to reflect your environment.

```bash
cp ~/nodecellar/inputs/simple.yaml.template ~/nc-simple.yaml
vi ~/nc-simple.yaml
```

Fill in the manager host's private IP, agent user (`centos`), as well as the path of the private key file on the manager as written below:

```bash
nodejs_host_ip: YOUR_NODEJS_VM_IP
mongod_host_ip: YOUR MONGOD_VM_IP
agent_user: centos
agent_private_key_path: /root/cfy-training.pem
```

**NOTE**: `agent_private_key_path` should be the path to the key file *as it is known to the Cloudify Manager*.

## Step 4: Upload the blueprint

```bash
cfy blueprints upload ~/nodecellar/simple-blueprint.yaml -b nodecellar
```

You should see the following output:

```
Uploading blueprint /home/centos/nodecellar/simple-blueprint.yaml...
 simple-blueprint.... |################################################| 100.0%
Blueprint uploaded. The blueprint's id is nodecellar
```

To witness that the blueprint has been uploaded:

*   Through the CLI:

    ```bash
    cfy blueprints list
    ```
*   Through the UI: Go to the Cloudify Manager's web UI and select the "Local Blueprints" section.

## Step 5: Create a deployment

Once NodeCellar's blueprint is uploaded, we need to create a deployment for it, using the inputs file we customized in step 3.

```bash
cfy deployments create nc-dep-1 -b nodecellar -i ~/nc-simple.yaml
```

You should see the output similar to the following:

```
Creating new deployment from blueprint nodecellar...
Deployment created. The deployment's id is nc-dep-1
```

## Step 6: Execute the `install` workflow

Once the deployment has been created, we can install the NodeCellar application. Trigger the `install` workflow by typing:

```bash
cfy executions start -d nc-dep-1 install
```

You should see the events being printed to the screen. You can also go to the deployments screen in the UI and see the events there. 

```
...
2017-04-08 20:31:02.096  CFY <nc-dep-1> [nodecellar_xdef0b] Starting node
2017-04-08 20:31:02.321  CFY <nc-dep-1> [nodecellar_xdef0b.start] Sending task 'script_runner.tasks.run'
2017-04-08 20:31:02.338  CFY <nc-dep-1> [nodecellar_xdef0b.start] Task started 'script_runner.tasks.run'
2017-04-08 20:31:02.904  LOG <nc-dep-1> [nodecellar_xdef0b.start] INFO: Downloaded scripts/nodecellar/start-nodecellar-app.sh to /tmp/W6D31/start-nodecellar-app.sh
2017-04-08 20:31:02.917  LOG <nc-dep-1> [nodecellar_xdef0b.start] INFO: Executing: /tmp/W6D31/start-nodecellar-app.sh
2017-04-08 20:31:05.139  LOG <nc-dep-1> [nodecellar_xdef0b.start] INFO: MongoDB is located at 172.31.26.191:27017
2017-04-08 20:31:05.469  LOG <nc-dep-1> [nodecellar_xdef0b.start] INFO: Starting nodecellar application on port 8080
2017-04-08 20:31:05.800  LOG <nc-dep-1> [nodecellar_xdef0b.start] INFO: /tmp/f2b27bb3-184d-4c3a-926f-106f30a29492/nodejs/nodejs-binaries/bin/node /tmp/f2b27bb3-184d-4c3a-926f-106f30a29492/nodecellar/nodecellar-source/server.js
2017-04-08 20:31:06.338  LOG <nc-dep-1> [nodecellar_xdef0b.start] INFO: Running Nodecellar liveness detection on port 8080
2017-04-08 20:31:06.764  LOG <nc-dep-1> [nodecellar_xdef0b.start] INFO: [GET] http://localhost:8080 200
2017-04-08 20:31:07.399  LOG <nc-dep-1> [nodecellar_xdef0b.start] INFO: Sucessfully started Nodecellar (10361)
2017-04-08 20:31:07.512  LOG <nc-dep-1> [nodecellar_xdef0b.start] INFO: Execution done (return_code=0): /tmp/W6D31/start-nodecellar-app.sh
2017-04-08 20:31:07.639  CFY <nc-dep-1> [nodecellar_xdef0b.start] Task succeeded 'script_runner.tasks.run'
2017-04-08 20:31:08.420  CFY <nc-dep-1> 'install' workflow execution succeeded
Finished executing workflow install on deployment nc-dep-1
* Run 'cfy events list -e f2b27bb3-184d-4c3a-926f-106f30a29492' to retrieve the execution's events/logs
```

## Step 7: Access the application

Point your browser to your NodeJS's public IP, port 8080. You should now see the NodeCellar application. click the "Start Browsing Node Cellar" button and see the list of wines that is retrieved from the installed Mongo database.

![Nodecellar](../../../raw/4.0/running-nodecellar-on-manager/nodecellar.png "NodeCellar")

## Step 8: View executions

```bash
cfy executions list -d nc-dep-1
```

That will view all workflow executions that have been started on the `nc-dep-1` deployment.

## Step 9: View outputs

You can view the deployment's outputs by using the following command:

```bash
cfy deployments outputs nc-dep-1
```

## Step 10: Execute the `uninstall` workflow

To uninstall the application, trigger the `uninstall` workflow:

```bash
cfy executions start -d nc-dep-1 uninstall
```

The NodeCellar application will be uninstalled, and will no longer be available for browsing. Then, delete the deployment
and the blueprint:

```bash
cfy deployments delete nc-dep-1
cfy blueprints delete nodecellar
```
