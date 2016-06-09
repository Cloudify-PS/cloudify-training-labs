# Lab: Installing the CLI

## Prerequisites

You will be receiving the following from the instructor:

* Public and private IP's of the VM on which the CLI is going to be installed
* Private key to use in order to access that VM

Copy the private key, provided by the instructor, to the file system on the machine you're going to use
to connect to the various VM's (most likely, that would be your own machine).

**NOTE**: if you are accessing the VM's from Linux, make sure that the private key file has restrictive enough
permissions on it, to avoid being rejected by SSH (`0400` or `0600` would do):

```bash
chmod 0400 <pem_file>
```

## Preparing your CLI VM

`ssh` into your CLI VM, and run the following command:

```
curl https://bootstrap.pypa.io/get-pip.py | sudo python
```

The above commands download the `pip` installer and run it.

**NOTE**: For CentOS/RHEL machines, EPEL contains `pip`; however, it is of an older version that is not supported
by Cloudify.

```
curl -J -O http://repository.cloudifysource.org/org/cloudify3/3.4.0/m5-RELEASE/cloudify-3.4.0~m5-394.el6.x86_64.rpm
sudo yum install -y cloudify-3.4.0~m5-394.el6.x86_64.rpm
```

The above commands download the CLI RPM package, and install it.

### Check Cloudify's version

```bash
cfy --version
```

The output should be similar to the following:

```
Cloudify CLI 3.4.0-m5
```
