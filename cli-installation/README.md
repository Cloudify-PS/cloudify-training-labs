# Lab: Installing the CLI

## Prerequisites

### Working on a GigaSpaces-provided VM

If you are working on this lab as part of the Cloudify official training course, you will be receiving
the following from the instructor:

* Public and private IP's of the VM on which the CLI is going to be installed
* Private key to use in order to access that VM

Copy the private key, provided by the instructor, to the file system on the machine you're going to use
to connect to the various VM's (most likely, that would be your own machine).

**NOTE**: if you are accessing the VM's from Linux, make sure that the private key file has restrictive enough
permissions on it, to avoid being rejected by SSH (`0400` or `0600` would do):

```bash
chmod 0400 <pem_file>
```

### Creating your own CLI VM

If you don't have a CLI VM provided to you, or you would like to use your own image:

* Use a CentOS 7.0 image
* Allow at least 1GB of RAM and 5GB of storage
* Make sure that `iptables` is disabled. This is not a requirement of the CLI per-se, but rather
a requirement of the training labs; the labs involve using Cloudify in "local mode" to install applications locally, and
in order to verify proper installation, these applications have to be accessible through their designated ports.
  * If you are using `firewalld`, stop it and mask it:

    ```bash
    sudo systemctl stop firewalld
    sudo systemctl mask firewalld
    ```

  * If you are using `iptables-services`, stop it and mask it:

    ```bash
    sudo systemctl stop iptables
    sudo systemctl mask iptables
    ```

* Make sure that the VM is connected to a security group that is very permissive (same reasoning as for
`iptables`).

## Preparing your CLI VM

`ssh` into your CLI VM, and run the following commands:

`sudo yum install unzip git wget`

The above command installs packages that are required for the labs.
**NOTE**: These packages are *not* prerequisites for the Cloudify CLI.

```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo python get-pip.py
```

The above commands download the `pip` installer and run it.

**NOTE**: For CentOS/RHEL machines, EPEL contains `pip`; however, it is of an older version that is not supported
by Cloudify.

```
curl -J -O http://repository.cloudifysource.org/org/cloudify3/3.3.1/sp-RELEASE/cloudify-centos-Core-cli-3.3.1-sp_b310.x86_64.rpm
sudo yum install -y cloudify-centos-Core-cli-3.3.1-sp_b310.x86_64.rpm
```

The above commands download the CLI RPM package, and install it.

### Clone the training labs

```bash
git clone -b 3.4.0 https://github.com/cloudify-cosmo/cloudify-training-labs
```

**NOTE**: an alternative clone URL may be provided by the instructor.

### Activate the `cfy` virtual environment

```bash
source /opt/cfy/env/bin/activate
```

The command above activates the Cloudify CLI *virtual environment*. The virtual environment remains in effect until you
either deactivate it (using the `deactivate` command), or log out.

For simplicity, execute the following command to ensure that the virtual environment is activated automatically upon
logging in:

```bash
echo "source /opt/cfy/env/bin/activate" >> ~/.bash_profile
```

### Check Cloudify's version

```bash
cfy --version
```

The output should be similar to the following:

```
Cloudify CLI 3.4.0
```
