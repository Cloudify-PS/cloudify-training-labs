# Lab 2: Manager Bootstrapping Using the Simple Manager Blueprint

The purpose of this lab is to bootstrap a Cloudify manager on a fresh instance using the simple manager blueprint.
Before starting, make sure you have the following details from the instructor:

* The private and public IP's of the server you are going to bootstrap the manager on (one server per trainee).
* The keypair of the server.

### Step 1: Create a working directory

For clarity and convenience, create a new directory that will serve as Cloudify's working directory. We will also place edited files there, in order to simplify the `cfy` commands we run.

Our labs will assume that the chosen directory is `~/work`.

```bash
mkdir ~/work && cd ~/work
```

### Step 2: Download the manager blueprint

Execute the following command:

```bash
wget -O blueprints.zip https://github.com/cloudify-cosmo/cloudify-manager-blueprints/archive/3.2.zip
unzip blueprints.zip
```

### Step 3: Configure the inputs file

```bash
cp cloudify-manager-blueprints-3.2/simple/inputs.yaml.template manager-inputs.yaml
vi manager-inputs.yaml
```

Fill in the public and private IP's, SSH user (`ubuntu`), as well as the path of the keyfile you were provided by the instructor:

```yaml
public_ip: PUBLIC IP GOES HERE
private_ip: PRIVATE IP GOES HERE
ssh_user: ubuntu
ssh_key_filename: /path/to/key.pem

agents_user: ubuntu
resources_prefix: ''
```

### Step 4: Trigger the bootstrap process

Activate the virtualenv in which you installed the Cloudify CLI (if it isn't already activated), and type the following:

```bash
cfy init
cfy bootstrap --install-plugins -p cloudify-manager-blueprints-3.2/simple/simple-manager-blueprint.yaml -i manager-inputs.yaml
```

This should take a few minutes, during which you will see the output of the bootstrapping process. At the end of the process you should see the IP address of the manager, e.g.:

```
015-01-20 16:13:15 CFY <manager> 'install' workflow execution succeeded
bootstrapping complete
management server is up at 54.91.114.221
```

### Step 5: Verify the manager started successfully

Type the following command to verify that all manager components are up and running:

```bash
cfy status
```

You should see the output similar to the following. Make sure all components are running:

```bash
Getting management services status... [ip=54.91.114.221]

Services:
+--------------------------------+---------+
|            service             |  status |
+--------------------------------+---------+
| Riemann                        |    up   |
| Celery Management              |    up   |
| Manager Rest-Service           |    up   |
| AMQP InfluxDB                  |    up   |
| RabbitMQ                       |    up   |
| Elasticsearch                  |    up   |
| Webserver                      |    up   |
| Cloudify UI                    |    up   |
| Logstash                       |    up   |
+--------------------------------+---------+
```

### Step 6: Access the web UI

Copy the IP address you received at the end of the bootstrap process to your browser's address line. You should get the web UI:

![alt text](https://raw.githubusercontent.com/cloudify-cosmo/cloudify-training-labs/master/lab2/cfy32.png "Cloudify 3.2 Web UI")