# Lab: Installing the CLI

## Prerequisites

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

## Process

### Install the CLI RPM package

Run the following commands to download the CLI RPM package and install it:

```
curl -J -O http://repository.cloudifysource.org/org/cloudify3/3.3.1/sp-RELEASE/cloudify-centos-Core-cli-3.3.1-sp_b310.x86_64.rpm
sudo yum install -y cloudify-centos-Core-cli-3.3.1-sp_b310.x86_64.rpm
```

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
Cloudify CLI 3.3.1
```
