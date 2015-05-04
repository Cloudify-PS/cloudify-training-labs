# Lab 1: Configuring Vagrant and Installing CLI

## Prerequisites

### Install Vagrant
Download from [http://www.vagrantup.com/downloads.html](http://www.vagrantup.com/downloads.html).

### Install the `vbguest` plugin
Check whether the `vbguest` plugin is installed:

```bash
vagrant plugin list
```

If `vagrant-vbguest` is not listed, install it:

```bash
vagrant plugin install vagrant-vbguest
```

## Process

### Download Cloudify's `ubuntu-14.04` vagrant box

```bash
wget https://github.com/kraksoft/vagrant-box-ubuntu/releases/download/14.04/ubuntu-14.04-amd64.box
```

### Add the box to vagrant:

```bash
vagrant box add --name ub1404 ubuntu-14.04-amd64.box
```

### Initialize a vagrant file and edit it

```bash
vagrant init
```

Then, edit `Vagrantfile` and set the following (certain keys may already exist commented — just uncomment & modify them if so):

```
config.vm.box = "ub1404"
config.vm.network "private_network", ip: "192.168.33.10"
```

### Start the VM

```bash
vagrant up
```

### Login

Use one of the following (username and password are `vagrant`):

```bash
vagrant ssh
```

or

```bash
ssh vagrant@192.168.33.10
```

or, on Windows:

```bat
putty.exe vagrant@192.168.33.10 -pw vagrant
```

### In the VM

Once you've `ssh`'d into the box, run the following:

```bash
curl http://gigaspaces-repository-eu.s3.amazonaws.com/org/cloudify3/get-cloudify.py -o get-cloudify.py
python get-cloudify.py --virtualenv myenv --version 3.2
```

That will install the Cloudify CLI, as well as its dependencies (such as `python-dev`, `gcc` and so forth), into a Python `virtualenv` named `myenv`.

### Activate the `myenv` virtualenv

```bash
source myenv/bin/activate
```

### Check Cloudify's version

```bash
cfy --version
```

The output should be similar to the following:

```
Cloudify CLI 3.2.0     (build: 85, date: )
```