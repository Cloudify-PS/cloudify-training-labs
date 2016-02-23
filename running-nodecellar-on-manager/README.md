# Lab: Installing NodeCellar on Cloudify Manager

The purpose of this lab is to upload a sample blueprint to the manager you had bootstrapped in the previous step and install it on the same VM as the manager.

Before starting, make sure you have the IP address of the manager you bootstrapped in the previous lab.

The sample blueprint we are going to work on, will install a sample application called *Nodecellar*.
 
## Step 1: Download the Nodecellar blueprint

In a terminal window (where you installed the CLI), execute the following command (this lab assumes that `~/work` is the working directory used during the previous lab):

```bash
cd ~/work
wget -O nodecellar.zip https://github.com/cloudify-cosmo/cloudify-nodecellar-example/archive/3.3.1.zip
unzip nodecellar.zip
```

That will download the latest nodecellar application and its blueprints, and extract them into `./cloudify-nodecellar-example-3.3.1`.

## Step 2: Copy key to manager

The blueprint that we are going to install, instructs Cloudify to install the example application on an existing VM.
Cloudify, therefore, needs access to the private key used to log into that existing VM. In this lab, that "existing VM"
is actually the manager's VM. As all VM's in the training use the same private key, you can copy the private key from
the CLI VM to the manager's VM:

```bash
scp -i cfy-training.pem cfy-training.pem centos@<manager-public-ip>:~/
```

## Step 3: Configure the inputs file

The Nodecellar archive contains a template for a blueprints inputs file. This template should be edited to reflect your environment.

```bash
cp cloudify-nodecellar-example-3.3.1/inputs/singlehost.yaml.template ./nc-singlehost.yaml
vi nc-singlehost.yaml
```

Fill in the manager host's private IP, agent user (`centos`), as well as the path of the keyfile on the manager as written below:

```bash
host_ip: YOUR_MANAGER_INSTANCE'S_PRIVATE_IP
agent_user: ubuntu
agent_private_key_path: /home/centos/cfy-training.pem
```

## Step 4: Upload the blueprint

```bash
cfy blueprints upload -p cloudify-nodecellar-example-3.3.1/simple-blueprint.yaml -b nodecellar
```

You should see the following output:

```
Validating cloudify-nodecellar-example-3.3.1/simple-blueprint.yaml
Blueprint validated successfully
Uploading blueprint cloudify-nodecellar-example-3.3.1/simple-blueprint.yaml to management server <public-ip>
Uploaded blueprint, blueprint's id is: nodecellar
```

Go to the web UI and make sure you see a blueprint named 'nodecellar' in the blueprints screen.

## Step 5: Create a deployment

Once Nodecellar's blueprints are uploaded, we need to create a deployment for it, using the inputs file we customized in step 3.

```bash
cfy deployments create -b nodecellar -i nc-singlehost.yaml -d nc-dep-1
```

You should see the output similar to the following:

```
Creating new deployment from blueprint nodecellar at management server <public-ip>
Deployment created, deployment's id is: nc-dep-1
```

## Step 6: Execute the `install` workflow

Once the deployment has been created, we can install the nodecellar application. Trigger the `install` workflow by typing: 

```bash
cfy executions start -d nc-dep-1 -w install
```

You should see the events being printed to the screen. You can also go to the deployments screen in the UI and see the events there. 

```
...
2016-01-28T06:24:54 CFY <nc-dep-1> [nodecellar_08f06] Starting node
2016-01-28T06:24:54 CFY <nc-dep-1> [nodecellar_08f06.start] Sending task 'script_runner.tasks.run'
2016-01-28T06:24:54 CFY <nc-dep-1> [nodecellar_08f06.start] Task started 'script_runner.tasks.run'
Finished executing workflow 'install' on deployment 'nc-dep-1'
* Run 'cfy events list --include-logs --execution-id 71b4a788-9923-4773-8b9d-cebe2734976d' to retrieve the execution's events/logs
```

## Step 7: Access the application

Point your browser to your manager's public IP, port 8080. You should now see the Nodecellar application. click the "Start browsing nodecellar" button and see the list of wines that is retrieved from the mongo database.

![Nodecellar](../../../raw/3.3.1/running-nodecellar-on-manager/nodecellar.png "Nodecellar")

## Step 8: View executions

```bash
cfy executions list -d nc-dep-1
```

That will view all workflow executions that have been started on the `nc-dep-1` deployment.

## Step 9: View outputs

```bash
cfy deployments outputs -d nc-dep-1
```
