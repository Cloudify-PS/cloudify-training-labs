# Lab: Installing NodeCellar on Cloudify Manager

The purpose of this lab is to upload a sample blueprint to the Manager you had bootstrapped previously, create a deployment for it and install it on the same VM as the manager.

The blueprint we are going to work with, will install a sample application called *NodeCellar* (if you are
currently going through the full training schedule, this is the same application introduced in a previous lab:
"Running NodeCellar Locally". The only difference is that we are going to use a different blueprint for
installing this application).
 
## Step 1: Download the NodeCellar blueprints

**NOTE**: You may already have downloaded the blueprints in an earlier lab. If you have, then please skip
this step.

Obtain the NodeCellar application from GitHub (this lab assumes that `~/mgr` is the working directory used to bootstrap the manager from):

```bash
cd ~
curl -L -o nodecellar.zip https://github.com/Cloudify-PS/cloudify-nodecellar-example/archive/3.4.1-maint.zip
unzip nodecellar.zip
mv cloudify-nodecellar-example-3.4.1-maint cloudify-nodecellar-example
```

That will download the latest NodeCellar application and its blueprints, and extract them into `./cloudify-nodecellar-example`.

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
cd ~/mgr
cp ../cloudify-nodecellar-example/inputs/simple.yaml.template ./nc-simple.yaml
vi nc-simple.yaml
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
cfy blueprints upload -p ../cloudify-nodecellar-example/simple-blueprint.yaml -b nodecellar
```

You should see the following output:

```
Uploading blueprint ../cloudify-nodecellar-example/simple-blueprint.yaml...
Blueprint uploaded. The blueprint's id is nodecellar
```

To witness that the blueprint has been uploaded:

*   Through the CLI:

    ```bash
    cfy blueprints list
    ```
*   Through the UI: Go to the Cloudify Manager's web UI and select the "Blueprints" section.

## Step 5: Create a deployment

Once NodeCellar's blueprint is uploaded, we need to create a deployment for it, using the inputs file we customized in step 3.

```bash
cfy deployments create -b nodecellar -i nc-simple.yaml -d nc-dep-1
```

You should see the output similar to the following:

```
Processing inputs source: nc-simple.yaml
Creating new deployment from blueprint nodecellar...
Deployment created. The deployment's id is nc-dep-1
```

## Step 6: Execute the `install` workflow

Once the deployment has been created, we can install the NodeCellar application. Trigger the `install` workflow by typing:

```bash
cfy executions start -d nc-dep-1 -w install -l
```

You should see the events being printed to the screen. You can also go to the deployments screen in the UI and see the events there. 

```
...
2017-01-29T06:22:51 LOG <nc-dep-1> [nodecellar_r2ptnh.start] INFO: Running Nodecellar liveness detection on port 8080
2017-01-29T06:22:51 LOG <nc-dep-1> [nodecellar_r2ptnh.start] INFO: [GET] http://localhost:8080 200
2017-01-29T06:22:52 LOG <nc-dep-1> [nodecellar_r2ptnh.start] INFO: Sucessfully started Nodecellar (17648)
2017-01-29T06:22:52 LOG <nc-dep-1> [nodecellar_r2ptnh.start] INFO: Execution done (return_code=0): /tmp/CRYCK/start-nodecellar-app.sh
2017-01-29T06:22:52 CFY <nc-dep-1> [nodecellar_r2ptnh.start] Task succeeded 'script_runner.tasks.run'
2017-01-29T06:22:53 CFY <nc-dep-1> 'install' workflow execution succeeded
Finished executing workflow install on deployment nc-dep-1
* Run 'cfy events list --include-logs --execution-id 61c86537-6ee5-4275-8e8f-330ff80b1838' to retrieve the execution's events/logs
```

## Step 7: Access the application

Point your browser to your NodeJS's public IP, port 8080. You should now see the NodeCellar application. click the "Start Browsing Node Cellar" button and see the list of wines that is retrieved from the installed Mongo database.

![Nodecellar](../../../raw/3.4.1/running-nodecellar-on-manager/nodecellar.png "NodeCellar")

## Step 8: View executions

```bash
cfy executions list -d nc-dep-1
```

That will view all workflow executions that have been started on the `nc-dep-1` deployment.

## Step 9: View outputs

You can view the deployment's outputs by using the following command:

```bash
cfy deployments outputs -d nc-dep-1
```

## Step 10: Execute the `uninstall` workflow

To uninstall the application, trigger the `uninstall` workflow:

```bash
cfy executions start -d nc-dep-1 -w uninstall -l
```

The NodeCellar application will be uninstalled, and will no longer be available for browsing. Then, delete the deployment
and the blueprint:

```bash
cfy deployments delete -d nc-dep-1
cfy blueprints delete -b nodecellar
```
