# Lab 2: Manager Bootstrapping Using the Simple Manager Blueprint

The purpose of this lab is to bootstrap a Cloudify manager on a fresh instance using the simple manager blueprint.
Before starting, make sure you have the following details from the trainer:
*	The private and public IP of the server you should bootstrap on. One server per trainee.
*	The keypair of the server.

### Step 1: Create a working directory
For clarity and convenience's sake, create a new directory that will serve as Cloudify's working directory. We will also place
edited files there, in order to simplify the `cfy` commands we run.

Our labs will assume that the chosen directory is `~/work`.

```bash
mkdir ~/work && cd ~/work
```

### Step 2: Download the manager blueprint
In a terminal window (where you installed the CLI), execute the following command:
```bash
wget -O blueprints.zip https://github.com/cloudify-cosmo/cloudify-manager-blueprints/archive/3.2.zip
unzip blueprints.zip
```

### Step 3: Configure the inputs file
```bash
cp cloudify-manager-blueprints-3.2/simple/inputs.yaml.template inputs.yaml
vi inputs.yaml
```

Fill in the public and private IP, ssh user (ubuntu), as well as the path of the keyfile you were provided by the trainer:
```yaml
public_ip: PUBLIC IP GOES HERE
private_ip: PRIVATE IP GOES HERE
ssh_user: ubuntu
ssh_key_filename: /path/to/key.pem

agents_user: ubuntu
resources_prefix: ''
```

### Step 4: Trigger the bootstrap process
Activate the virtualenv in which you installed the Cloudify CLI, and type the following:
```bash
cfy init
cfy bootstrap --install-plugins -p cloudify-manager-blueprints-3.2/simple/simple.yaml -i inputs.yaml
```

This should take a few minutes, during which you will see the output of the bootstrapping process. At the end of the process you should see the IP address of the manager, e.g.: 
```bash
015-01-20 16:13:15 CFY <manager> 'install' workflow execution succeeded
bootstrapping complete
management server is up at 54.91.114.221
```

### Step 5: Verify the manager started successfully 
Type the following command to verify that all manager components are up and running: 
```bash
cfy status
```

You should see the output similar to the following, make sure all components are running:
Getting management services status... [ip=54.91.114.221]

```bash
Services:
+--------------------------------+---------+
|            service             |  status |
+--------------------------------+---------+
| Riemann                        | running |
| Celery Management              | running |
| RabbitMQ                       | running |
| Cloudify Manager               | running |
| Elasticsearch                  | running |
| SSH                            | running |
| Webserver                      | running |
| Cloudify UI                    | running |
| Syslog                         | running |
| Logstash                       | running |
+--------------------------------+---------+
```

### Step 6: Access the web UI
Copy the IP address you received at the end of the bootstrap process to your browser's address line. You should get the web UI: 


![alt text](https://raw.githubusercontent.com/cloudify-cosmo/cloudify-training-labs/master/lab2/cfy32.png "Cloudify 3.2 Web UI")

