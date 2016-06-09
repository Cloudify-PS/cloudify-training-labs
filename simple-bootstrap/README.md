# Lab: Manager Bootstrapping

The purpose of this lab is to bootstrap a Cloudify manager on a fresh VM using the `simple` manager blueprint.

## Prerequisites

If you are working on this lab as part of the Cloudify official training course, you will be receiving
the following from the instructor:

* Private IP of the VM on which the manager is going to be installed

**NOTE**: the private key, used to access the VM on which the Cloudify Manager is to be installed, is identical
to the private key used to access the CLI VM. *This is not a Cloudify requirement*, but instead a design
of the training labs, in favour of simplicity.

<<<<<<< HEAD
=======
### Creating your own Cloudify Manager VM

If you don't have a Manager VM provided to you, or you would like to use your own image:

* Use a CentOS 7.x or RHEL 7.x image
* Ensure that the VM answers to the prerequisites documented in Cloudify's documentation website (http://docs.getcloudify.org/3.4.0/manager/prerequisites/),
with the following exceptions:
  * Minimum 4GB memory, 8GB recommended.
  * Minimum 2 vCPUs, 4 vCPUs recommended.
  * Minimum 5GB storage.
  * The security group to which this VM is connected should have more permissive rules than the ones stated,
  because other labs (that depend on this one) install topologies on the very same VM as the Manager's.
  It is recommended to allow incoming traffic on all ports for the labs.
* Make sure that `iptables` is disabled. Similarly to the CLI VM's case, this is not a Cloudify requirement but a training
material requirement.

>>>>>>> josh/master
## Process

*Note*: These steps should be executed on your CLI VM, *not* on the intended Manager VM.

### Step 1: Create a working directory

For clarity and convenience, create a new directory that will serve as Cloudify's working directory.

Our labs will assume that the chosen directory is `~/work`.

```bash
mkdir ~/work && cd ~/work
```

### Step 2: Have your Manager VM's private key available

The private key, required to connect to your manager VM, needs to be accessible to the Cloudify CLI. Copy the private key file to your CLI machine (either by either `scp` [Linux], `pscp`/`winscp` [Windows] or by pasting the key's contents into an editor).
For documentation purposes, it is assumed that the key file is available at `~/work/cfy-training.pem`.

### Step 3: Download the manager blueprint

Execute the following command:

```bash
<<<<<<< HEAD
wget -O blueprints.zip https://github.com/GigaSpaces-ProfessionalServices/cloudify-manager-blueprints/archive/3.3.1-maint.zip
unzip blueprints.zip
mv cloudify-manager-blueprints-3.3.1-maint cloudify-manager-blueprints-3.3.1
```

(**NOTE**: The GitHub URL above refers to a post-3.3.1 release of Cloudify. The original URL: https://github.com/cloudify-cosmo/cloudify-manager-blueprints/archive/3.3.1.zip)

That will download the latest manager blueprints and extract them into `./cloudify-manager-blueprints-3.3.1`.
=======
wget -O blueprints.zip https://github.com/cloudify-cosmo/cloudify-manager-blueprints/archive/3.4m5.zip
unzip blueprints.zip
mv cloudify-manager-blueprints-3.4m5/ cloudify-manager-blueprints
```

That will download the latest manager blueprints and extract them into `./cloudify-manager-blueprints`.
>>>>>>> josh/master

### Step 4: Configure the inputs file

The provided manager blueprints ship with templates for manager inputs. These templates have to be edited to reflect the environment in which the manager is to be installed.

(Back at `~/work`)

```bash
cp cloudify-manager-blueprints/simple-manager-blueprint-inputs.yaml ./manager-inputs.yaml
vi manager-inputs.yaml
```

Fill in the public and private IP's, SSH user (`centos` for CentOS 7.0), as well as the path to the private key used to SSH to the Manager's VM:

```yaml
public_ip: MANAGER_INSTANCE_IP
private_ip: MANAGER_INSTANCE_IP
ssh_user: centos
ssh_key_filename: ~/work/cfy-training.pem
<<<<<<< HEAD
=======
agents_user: centos
>>>>>>> josh/master
```

If deploying on a system with 4GB or less of memory, it may be necessary to limit the amount of memory
ElasticSearch allocates (for development / testing purposes).  This can be accomplished using
the following inputs.

```yaml
# Minimize the ElasticSearch footprint on dev managers
elasticsearch_heap_size: 1g
# Update the minimum amount of memory that's required to pass validation
minimum_required_total_physical_memory_in_mb: 3192
```

### Step 5: Trigger the bootstrap process

```bash
cfy init -r
cfy bootstrap --install-plugins -p cloudify-manager-blueprints/simple-manager-blueprint.yaml -i manager-inputs.yaml
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
Getting management services status... [ip=<manager-public-ip>]

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

![Cloudify 3.4.0 Web UI](cfy-3.4.0-ui.png "Cloudify 3.4.0 Web UI")
