# Lab 3: Manager Bootstrapping Using the Simple Manager Blueprint

The purpose of this lab is to bootstrap a Cloudify manager on a fresh instance using the simple manager blueprint.

## Prerequisites

Before starting, make sure you have the following details from the instructor:

* The private and public IP's of the server you are going to bootstrap the manager on.
* The keypair of the server.

## Process

*Note*: These steps should be executed on your CLI VM, *not* on the intended Manager VM.

### Step 1: Create a working directory

For clarity and convenience, create a new directory that will serve as Cloudify's working directory.

Our labs will assume that the chosen directory is `~/work`.

```bash
mkdir ~/work && cd ~/work
```

### Step 2: Have your Manager VM's private key available

The private key, required to connect to your manager VM, needs to be accessible to the Cloudify CLI. Copy the private key file to your CLI machine (either by either `scp` [linux], `pscp`/`winscp` [Windows] or by pasting the key's contents into an editor). For documentation purposes, it is assumed that the key file is available at `/home/ubuntu/work/cfy-training.pem`.

### Step 3: Download the manager blueprint

Execute the following command:

```bash
wget -O blueprints.zip https://github.com/cloudify-cosmo/cloudify-manager-blueprints/archive/3.2.1.zip
unzip blueprints.zip
```

That will download the latest manager blueprints and extract them into `./cloudify-manager-blueprints-3.2.1`.

### Step 4: Edit the sample `simple` blueprint for the correct Docker container URL

The Cloudify Manager, implemented as a Docker container, ships in two forms:

* A non-commercial version
* A commercial version, which includes the Cloudify UI

The manager blueprints, available through GitHub, refer to the non-commercial Docker container. For the purpose of this course, we will edit the manager blueprint to point at the commercial version.

Edit `./cloudify-manager-blueprints-3.2.1/simple/simple-manager-blueprint.yaml` and replace the value for `docker_url` with the following: `http://gigaspaces-repository-eu.s3.amazonaws.com/org/cloudify3/3.2.1/ga-RELEASE/cloudify-docker-commercial_3.2.1-ga-b212.tar`
 
### Step 5: Configure the inputs file

The provided manager blueprints ship with templates for manager inputs. These templates have to be edited to reflect the environment in which the manager is to be installed.

(Back at `~/work`)

```bash
cp cloudify-manager-blueprints-3.2.1/simple/inputs.yaml.template manager-inputs.yaml
vi manager-inputs.yaml
```

Fill in the public and private IP's, SSH user (`ubuntu`), as well as the path of the keyfile you were provided by the instructor:

```yaml
public_ip: MANAGER_INSTANCE_PUBLIC_IP
private_ip: MANAGER_INSTANCE_PRIVATE_IP
ssh_user: ubuntu
ssh_key_filename: /home/ubuntu/work/cfy-training.pem

agents_user: ubuntu
resources_prefix: ''
```

### Step 6: Trigger the bootstrap process

Activate the `virtualenv` in which you installed the Cloudify CLI (if it isn't already activated), and type the following:

```bash
cfy init
cfy bootstrap --install-plugins -p cloudify-manager-blueprints-3.2.1/simple/simple-manager-blueprint.yaml -i manager-inputs.yaml
```

The first command initializes a Cloudify CLI working directory inside the current working directory.

The second command triggers the bootstrap process. It should take a few minutes to complete, during which you will see the output of the bootstrapping process. At the end of the process you should see the IP address of the manager printed out, e.g.:

```
2015-06-15 02:18:42 CFY <manager> 'install' workflow execution succeeded
bootstrapping complete
management server is up at 15.125.87.108
```

### Step 7: Verify that the manager started successfully

Type the following command to verify that all manager components are up and running:

```bash
cfy status
```

You should see output similar to the following. Make sure all components are running:

```bash
Getting management services status... [ip=15.125.87.108]

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

### Step 8: Access the web UI

Using your browser, navigate to your Cloudify Manager's public IP address. For example: `http://15.125.87.108`

You should get the web UI:

![Cloudify 3.2.1 Web UI](../../../raw/master/lab3/cfy-3.2.1-ui.png "Cloudify 3.2.1 Web UI")