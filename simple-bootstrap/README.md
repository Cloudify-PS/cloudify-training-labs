# Lab: Manager Bootstrapping

The purpose of this lab is to bootstrap a Cloudify manager on a fresh VM using the `simple`` manager blueprint.

## Prerequisites

### Working on a GigaSpaces-provided VM

If you are working on this lab as part of the Cloudify official training course, you will be receiving
the following from the instructor:

* Public and private IP's of the VM on which the CLI is going to be installed

**NOTE**: the private key, used to access the VM on which the Cloudify Manager is to be installed, is identical
to the private key used to access the CLI VM. *This is not a Cloudify requirement*, but instead a design
of the training labs, in favour of simplicity.

### Creating your own Cloudify Manager VM

If you don't have a Manager VM provided to you, or you would like to use your own image:

* Use a CentOS 7.0 image
* Ensure that the VM answers to the prerequisites documented in Cloudify's documentation website (http://docs.getcloudify.org/3.4.0/manager/prerequisites/),
with the following exceptions:
  * The minimum amount of RAM should be 3GB.
  * The security group to which this VM is connected should have more permissive rules than the ones stated,
  because other labs (that depend on this one) install topologies on the very same VM as the Manager's.
  It is recommended to allow incoming traffic on all ports.
* Make sure that `iptables` is disabled. Similarly to the CLI VM's case, this is not a Cloudify requirement but a training
material requirement.

## Process

*Note*: These steps should be executed on your CLI VM, *not* on the intended Manager VM.

### Step 1: Create a working directory

For clarity and convenience, create a new directory that will serve as Cloudify's working directory.

Our labs will assume that the chosen directory is `~/work`.

```bash
mkdir ~/work && cd ~/work
```

### Step 2: Have your Manager VM's private key available

The private key, required to connect to your manager VM, needs to be accessible to the Cloudify CLI. Copy the private key file to your CLI machine (either by either `scp` [linux], `pscp`/`winscp` [Windows] or by pasting the key's contents into an editor).
For documentation purposes, it is assumed that the key file is available at `~/work/cfy-training.pem`.

### Step 3: Download the manager blueprint

Execute the following command:

```bash
wget -O blueprints.zip https://github.com/cloudify-cosmo/cloudify-manager-blueprints/archive/3.4m5.zip
unzip blueprints.zip
```

That will download the latest manager blueprints and extract them into `./cloudify-manager-blueprints-3.4m5`.

### Step 4: Configure the inputs file

The provided manager blueprints ship with templates for manager inputs. These templates have to be edited to reflect the environment in which the manager is to be installed.

(Back at `~/work`)

```bash
cp cloudify-manager-blueprints-3.4m5/simple-manager-blueprint-inputs.yaml ./manager-inputs.yaml
vi manager-inputs.yaml
```

Fill in the public and private IP's, SSH user (`centos` for CentOS 7.0), as well as the path to the private key used to SSH to the Manager's VM:

```yaml
public_ip: MANAGER_INSTANCE_PUBLIC_IP
private_ip: MANAGER_INSTANCE_PRIVATE_IP
ssh_user: centos
ssh_key_filename: ~/work/cfy-training.pem

agents_user: centos
resources_prefix: ''
```

### Step 5: Trigger the bootstrap process

Activate the `virtualenv` in which you installed the Cloudify CLI (if it isn't already activated), and type the following:

```bash
cfy init -r
cfy bootstrap --install-plugins -p cloudify-manager-blueprints-3.4m5/simple-manager-blueprint.yaml -i manager-inputs.yaml
```

The first command initializes a Cloudify CLI working directory inside the current working directory.

The second command triggers the bootstrap process. It should take around 15 minutes to complete, during which you will see the output of the bootstrapping process. At the end of the process you should see the IP address of the Manager printed out, e.g.:

```
bootstrapping complete
management server is up at <manager's-public-ip>
```

### Step 6: Verify that the manager started successfully

Type the following command to verify that all manager components are up and running:

```bash
cfy status
```

You should see output similar to the following. Make sure all components are running:

```bash
Getting management services status... [ip=<manager\'s-public-ip>]

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

### Step 7: Access the web UI

Using your browser, navigate to your Cloudify Manager's public IP address. For example: http://15.125.87.108

You should get the Cloudify Manager's Web UI:

![Cloudify 3.3.1 Web UI](../../../raw/3.3.1/simple-bootstrap/cfy-3.3.1-ui.png "Cloudify 3.3.1 Web UI")
