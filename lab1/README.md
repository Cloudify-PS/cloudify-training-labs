# Lab 1: Installing the CLI

## Prerequisites

You should receive the following from the instructor:

* Public and private IP's of the virtual machine on which the CLI is going to be installed
* Private key to use in order to access that virtual machine

**NOTE**: make sure that the private key file has restrictive enough permissions on it, to avoid being rejected by SSH (`0400` or `0600` would do):

```bash
chmod 0400 <pem_file>
```

## Preparing Your CLI VM

`ssh` into your CLI VM, and run the following commands:

`sudo apt-get update`

`sudo apt-get -y install python-pip python-virtualenv python-dev unzip git`

`curl http://gigaspaces-repository-eu.s3.amazonaws.com/org/cloudify3/get-cloudify.py -o get-cloudify.py`

`python get-cloudify.py --virtualenv cfyenv --version 3.2`

The first two commands will update `apt`'s sources and then install the dependencies for the Cloudify CLI installer, as well as `git` (`git` is not a dependency of the Cloudify CLI; it is a dependency for this lab).

The `curl` command downloads the Cloudify CLI installer, which is then executed in order to install the Cloudify CLI into a Python `virtualenv` called `cfyenv`.

### Clone the training labs

```bash
git clone https://github.com/cloudify-cosmo/cloudify-training-labs
```

*Note*: an alternative clone URL may be provided by the instructor.

### Activate the `cfyenv` virtualenv

```bash
source cfyenv/bin/activate
```

### Check Cloudify's version

```bash
cfy --version
```

The output should be similar to the following:

```
Cloudify CLI 3.2.0
```