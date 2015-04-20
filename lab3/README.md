# Lab 3: Uploading and Deploying a Sample Blueprint

The purpose of this lab is to upload a sample blueprint to the manager you bootstrapped in the previous step and install it on the same VM.

Before starting, make sure you have the IP address of the manager you bootstrapped in the previous lab.

## Step 1: Download the nodecellar blueprint

In a terminal window (where you installed the CLI), execute the following command (this lab assumes that `~/work` is the working directory used during the previous lab):

```bash
cd ~/work
wget -O nodecellar.zip https://github.com/cloudify-cosmo/cloudify-nodecellar-example/archive/3.2.zip
unzip nodecellar.zip
```

## Step 2: Step 2: Configure the inputs file

```bash
cp cloudify-nodecellar-example-3.2/inputs/singlehost.yaml.template nc-singlehost.yaml
vi nc-singlehost.yaml
```

Fill in the host IP (your instance's private IP), agent user (`ubuntu`), as well as the path of the keyfile on the manager as written below:

```bash
host_ip: YOUR INSTANCE'S PRIVATE IP
agent_user: ubuntu
agent_private_key_path: /home/ubuntu/.ssh/agent_key.pem
```

## Step 3: Upload the blueprint

```bash
cfy blueprints upload -p cloudify-nodecellar-example-3.2/singlehost-blueprint.yaml -b nodecellar
```

You should see the following output:

```
Validating cloudify-nodecellar-example-3.2/singlehost-blueprint.yaml
Blueprint validated successfully
Uploading blueprint cloudify-nodecellar-example-3.2/singlehost-blueprint.yaml to management server 54.91.114.221
Uploaded blueprint, blueprint's id is: nodecellar
```

Go to the web UI and make sure you see a blueprint named 'nodecellar' in the blueprints screen.

![alt text](https://raw.githubusercontent.com/cloudify-cosmo/cloudify-training-labs/master/lab3/blueprints-screen.png "Blueprints screen")

## Step 4: Create a deployment

```bash
cfy deployments create -b nodecellar -i nc-singlehost.yaml -d nodecellar
```

You should see the output similar to the following:

```
Creating new deployment from blueprint nodecellar at management server 54.91.114.221
Deployment created, deployment's id is: nodecellar
```

## Step 5: Execute the `install` workflow

Trigger the `install` workflow by typing: 

```bash
cfy executions start -d nodecellar -w install
```

You should see the events being printed to the screen. You can also go to the deployments screen in the UI and see the events there. 

```
Executing workflow 'install' on deployment 'nodecellar' at management server 54.91.114.221 [timeout=900 seconds]
2015-01-21T02:11:53 CFY <nodecellar> Starting 'install' workflow execution
2015-01-21T02:11:53 CFY <nodecellar> [host_ff674] Creating node
2015-01-21T02:11:54 CFY <nodecellar> [host_ff674] Configuring node
2015-01-21T02:11:54 CFY <nodecellar> [host_ff674] Starting node
2015-01-21T02:11:54 CFY <nodecellar> [host_ff674] Installing worker
2015-01-21T02:11:54 CFY <nodecellar> [host_ff674.install] Sending task 'worker_installer.tasks.install'
...
```

## Step 6: Access the application

Point your browser to your manager's public IP, port 8080. You should now see the nodecellar application. click the "Start browsing nodecellar" button and see the list of wines that is retrieved from the mongo database.

![alt text](https://raw.githubusercontent.com/cloudify-cosmo/cloudify-training-labs/master/lab3/nodecellar.png "Nodecellar")