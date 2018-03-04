# Lab: Manager Bootstrapping

The purpose of this lab is to install a Cloudify manager on a fresh VM.

## Prerequisites

If you are working on this lab as part of the Cloudify official training course, you will be receiving
the following from the instructor:

* Public and private IP's of the VM on which the manager is going to be installed

**NOTE**: the private key, used to access the VM on which the Cloudify Manager is to be installed, is identical
to the private key used to access the CLI VM. *This is not a Cloudify requirement*, but instead a design
of the training labs, in favour of simplicity.

## Process

*Note*: Steps 1-5 should be executed on your *Manager VM*.

### Step 1: Download Cloudify Manager's RPM

```bash
curl -J -O http://repository.cloudifysource.org/cloudify/4.3.0/ga-release/cloudify-manager-install-4.3ga.rpm
```

### Step 2: Install Cloudify Manager's RPM

```bash
sudo yum -y install cloudify-manager-install-4.3ga.rpm
```

### Step 3: Edit the installation's configuration file

Edit the file `/etc/cloudify/config.yaml`.

* Look for `private_ip` and populate your manager VM's private IP.
* Look for `public_ip` and populate your manager VM's public IP.

**NOTES**

1. If deploying on a system with less than 3700MB RAM, you'll have to adjust the `minimum_required_total_physical_memory_in_mb`
   input:
   
   ```yaml
   minimum_required_total_physical_memory_in_mb: 3500
   ```

2. By default, the `admin_password` input is set to an empty string. In that case, the manager will generate a password
   and will display it at the end of the bootstrap process. You may uncomment that input and provide your own value
   instead.

### Step 4: Start the installation process

```bash
cfy_manager install
```

The installation should take approximately 3-4 minutes, during which you will see the output of the installation process.
At the end of the process you should see the IP address of the Manager printed out, as well as the passford for the
administrative user. For example:

```
2018-03-04 14:58:26,795 - [MAIN] - NOTICE - Cloudify Manager successfully installed!
2018-03-04 14:58:26,840 - [MAIN] - NOTICE - Manager is up at http://35.173.99.54
2018-03-04 14:58:26,840 - [MAIN] - NOTICE - ##################################################
2018-03-04 14:58:26,840 - [MAIN] - NOTICE - Manager password is emvAZ47dJ7ou
2018-03-04 14:58:26,840 - [MAIN] - NOTICE - ##################################################
2018-03-04 14:58:26,840 - [MAIN] - NOTICE - To install the default plugins bundle run:
2018-03-04 14:58:26,840 - [MAIN] - NOTICE - 'cfy plugins bundle-upload'
2018-03-04 14:58:26,840 - [MAIN] - NOTICE - ##################################################
2018-03-04 14:58:26,841 - [MAIN] - NOTICE - Finished in 3 minutes and 24 seconds
```

### Step 5: Verify that the manager started successfully

Type the following command to verify that all manager components are up and running:

```bash
cfy status
```

You should see output similar to the following. Make sure all components are running:

```
Retrieving manager services status... [ip=localhost]

Services:
+--------------------------------+---------+
|            service             |  status |
+--------------------------------+---------+
| Cloudify Composer              | running |
| Logstash                       | running |
| Webserver                      | running |
| Cloudify Stage                 | running |
| InfluxDB                       | running |
| AMQP InfluxDB                  | running |
| RabbitMQ                       | running |
| Celery Management              | running |
| PostgreSQL                     | running |
| Manager Rest-Service           | running |
| Riemann                        | running |
+--------------------------------+---------+
```

### Step 6: Access the UI

Using your browser, navigate to your Cloudify Manager's public IP address. For example: http://15.125.87.108

You should get the Cloudify Manager's UI login page:

![Cloudify 4.3 Login](../../../raw/4.3/manager-installation/cfy-ui-login.png "Cloudify UI: Login")

Enter `admin` as the username, and the manager's password. Upon logging in, you'll see the Cloudify UI.

### Step 6: Create a CLI profile pointing at the manager

Log into your CLI VM and use the `cfy profiles` command to create a profile pointing at your manager:

```bash
cfy profiles use <manager-public-ip> -u admin -p <admin-password> -t default_tenant
```

You can use the `cfy status` command to ensure proper connection and function:

```bash
cfy status
```