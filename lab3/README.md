# Lab 3: Uploading and Deploying a Sample Blueprint

The purpose of this lab is to upload a sample blueprint to the manager you had bootstrapped in the previous step and install it on the same VM as the manager.

Before starting, make sure you have the IP address of the manager you bootstrapped in the previous lab.

The sample blueprint we are going to work on, will install a sample application called *Nodecellar*.
 
## Step 1: Download the Nodecellar blueprint

In a terminal window (where you installed the CLI), execute the following command (this lab assumes that `~/work` is the working directory used during the previous lab):

```bash
cd ~/work
wget -O nodecellar.zip https://github.com/cloudify-cosmo/cloudify-nodecellar-example/archive/3.2m8.zip
unzip nodecellar.zip
```

That will download the latest nodecellar application and its blueprints, and extract them into `./cloudify-nodecellar-example-3.2m8`.

## Step 2: Step 2: Configure the inputs file

The Nodecellar archive contains a template for a blueprints inputs file. This template should be edited to reflect your environment.

```bash
cp cloudify-nodecellar-example-3.2m8/inputs/singlehost.yaml.template nc-singlehost.yaml
vi nc-singlehost.yaml
```

Fill in the host IP (your instance's private IP), agent user (`ubuntu`), as well as the path of the keyfile on the manager as written below:

```bash
host_ip: YOUR_INSTANCE'S_PRIVATE_IP
agent_user: ubuntu
agent_private_key_path: /root/.ssh/agent_key.pem
```

**Note**: the last parameter, `agent_private_key_path`, specifies the location of the manager's private key, *as known to the Cloudify Manager*.

## Step 3: Upload the blueprint

```bash
cfy blueprints upload -p cloudify-nodecellar-example-3.2m8/singlehost-blueprint.yaml -b nodecellar
```

You should see the following output:

```
Validating cloudify-nodecellar-example-3.2m8/singlehost-blueprint.yaml
Blueprint validated successfully
Uploading blueprint cloudify-nodecellar-example-3.2m8/singlehost-blueprint.yaml to management server 52.0.27.130
Uploaded blueprint, blueprint's id is: nodecellar
```

Go to the web UI and make sure you see a blueprint named 'nodecellar' in the blueprints screen.

![alt text](https://raw.githubusercontent.com/cloudify-cosmo/cloudify-training-labs/master/lab3/blueprints-screen.png "Blueprints screen")

## Step 4: Create a deployment

Once Nodecellar's blueprints are uploaded, we need to create a deployment for it, using the inputs file we customized in step 2.

```bash
cfy deployments create -b nodecellar -i nc-singlehost.yaml -d nodecellar
```

You should see the output similar to the following:

```
Creating new deployment from blueprint nodecellar at management server 52.0.27.130
Deployment created, deployment's id is: nodecellar
```

## Step 5: Execute the `install` workflow

Once the deployment has been created, we can install the nodecellar application. Trigger the `install` workflow by typing: 

```bash
cfy executions start -d nodecellar -w install
```

You should see the events being printed to the screen. You can also go to the deployments screen in the UI and see the events there. 

```
Executing workflow 'install' on deployment 'nodecellar' at management server 52.0.27.130 [timeout=900 seconds]
2015-05-05T23:09:39 CFY <nodecellar> Starting 'install' workflow execution
2015-05-05T23:09:39 CFY <nodecellar> [host_e4657] Creating node
2015-05-05T23:09:40 CFY <nodecellar> [host_e4657] Configuring node
2015-05-05T23:09:40 CFY <nodecellar> [host_e4657] Starting node
2015-05-05T23:09:40 CFY <nodecellar> [host_e4657] Installing worker
2015-05-05T23:09:40 CFY <nodecellar> [host_e4657.install] Sending task 'worker_installer.tasks.install'
...
```

## Step 6: Access the application

Point your browser to your manager's public IP, port 8080. You should now see the Nodecellar application. click the "Start browsing nodecellar" button and see the list of wines that is retrieved from the mongo database.

![alt text](https://raw.githubusercontent.com/cloudify-cosmo/cloudify-training-labs/master/lab3/nodecellar.png "Nodecellar")

## Step 7: Cleanup

To uninstall Nodecellar, first execute the `uninstall` workflow; then, delete the deployment, and finally, delete the blueprint.

```bash
cfy executions start -d nodecellar -w uninstall
cfy deployments delete -d nodecellar
cfy blueprints delete -b nodecellar
```