# Lab: Manager Bootstrapping

The purpose of this lab is to bootstrap a Cloudify manager on a fresh VM using the `simple` manager blueprint.

## Prerequisites

If you are working on this lab as part of the Cloudify official training course, you will be receiving
the following from the instructor:

* Private IP of the VM on which the manager is going to be installed

**NOTE**: the private key, used to access the VM on which the Cloudify Manager is to be installed, is identical
to the private key used to access the CLI VM. *This is not a Cloudify requirement*, but instead a design
of the training labs, in favour of simplicity.

### Manager blueprints

If you installed the CLI from the official CLI RPM, then the manager blueprints are available to you at `/opt/cfy/cloudify-manager-blueprints`.
The rest of this lab assumes that that is the case. If it isn't, you'll have to download the manager blueprints from GitHub
(http://github.com/cloudify-cosmo/cloudify-manager-blueprints; **make sure you use the correct tag**) and adjust the commands
below accordingly.

## Process

*Note*: These steps should be executed on your CLI VM, *not* on the intended Manager VM.

### Step 1: Create a working directory

For clarity and convenience, create a new directory that will serve as Cloudify's working directory.

Our labs will assume that the chosen directory is `~/mgr`.

```bash
mkdir ~/mgr
```

### Step 2: Have your Manager VM's private key available

The private key, required to connect to your manager VM, needs to be accessible to the Cloudify CLI. Copy the private key file to your CLI machine (either by either `scp` [linux], `pscp`/`winscp` [Windows] or by pasting the key's contents into an editor).
For documentation purposes, it is assumed that the key file is available at `~/cfy-training.pem`.

### Step 3: Configure the inputs file

The provided manager blueprints ship with templates for manager inputs. These templates have to be edited to reflect the environment in which the manager is to be installed.

```bash
cd ~/mgr
cp /opt/cfy/cloudify-manager-blueprints/simple-manager-blueprint-inputs.yaml ./manager-inputs.yaml
vi manager-inputs.yaml
```

Fill in the public and private IP's, SSH user (`centos` for CentOS 7.x), as well as the path to the private key used to SSH to the Manager's VM:

```yaml
public_ip: MANAGER_VM_PUBLIC_IP
private_ip: MANAGER_VM_PRIVATE_IP
ssh_user: centos
ssh_key_filename: ~/cfy-training.pem
```

**NOTES**

1. If deploying on a system with 3GB RAM or less, it may be necessary to limit the amount of memory
   ElasticSearch allocates (for development / testing purposes). This can be accomplished using
   the following input:

   ```yaml
   elasticsearch_heap_size: 1g
   ```

2. If deploying on a system with less than 3792MB RAM, you'll have to adjust the `minimum_required_total_physical_memory_in_mb`
   input:
   
   ```yaml
   minimum_required_total_physical_memory_in_mb: 3500
   ```

### Step 4: Trigger the bootstrap process

```bash
cfy init -r
cfy bootstrap -p /opt/cfy/cloudify-manager-blueprints/simple-manager-blueprint.yaml -i manager-inputs.yaml
```

The first command initializes a Cloudify CLI working directory inside the current working directory.

The second command triggers the bootstrap process. It should take around 15 minutes to complete, during which you will see the output of the bootstrapping process. At the end of the process you should see the IP address of the Manager printed out, e.g.:

```
Bootstrap complete
Manager is up at <manager's-public-ip>
```

### Step 5: Verify that the manager started successfully

Type the following command to verify that all manager components are up and running:

```bash
cfy status
```

You should see output similar to the following. Make sure all components are running:

```bash
Retrieving management services status... [ip=<manager's-public-ip>]

Services:
+--------------------------------+---------+
|            service             |  status |
+--------------------------------+---------+
| InfluxDB                       | running |
| Celery Management              | running |
| Logstash                       | running |
| RabbitMQ                       | running |
| AMQP InfluxDB                  | running |
| Manager Rest-Service           | running |
| Cloudify UI                    | running |
| Webserver                      | running |
| Riemann                        | running |
| Elasticsearch                  | running |
+--------------------------------+---------+
```

### Step 6: Access the web UI

Using your browser, navigate to your Cloudify Manager's public IP address. For example: http://15.125.87.108

You should get the Cloudify Manager's Web UI:

![Cloudify 3.4.2 Web UI](../../../raw/3.4.2/simple-bootstrap/cfy-3.4.2-ui.png "Cloudify 3.4.2 Web UI")
