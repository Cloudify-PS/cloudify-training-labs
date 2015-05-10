# Lab 1: Configuring Vagrant and Installing CLI

## Prerequisites

### Install Vagrant

Download from [http://www.vagrantup.com/downloads.html](http://www.vagrantup.com/downloads.html).

On Windows, make sure that Vagrant's `bin` subdirectory is added to your `PATH`.

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

### Download an Ubuntu 14.04 Vagrant box

Create a directory that will serve as the Vagrant working directory for the training session. For documentation purposes, it is assumed that this directory is `~/cfy-vagrant`.

```bash
mkdir ~/cfy-vagrant && cd ~/cfy-vagrant
```

Or, on Windows:

```bat
cd /d %USERPROFILE%
mkdir cfy-vagrant
cd cfy-vagrant
```

Next, download the latest Vagrant box:

```bash
wget https://github.com/kraksoft/vagrant-box-ubuntu/releases/download/14.04/ubuntu-14.04-amd64.box
```

(On Windows, simply paste the box's URL into the browser's address bar, and download the file into `%USERPROFILE%/cfy-vagrant`)

### Add the box to Vagrant:

```bash
vagrant box add --name cfy-training ubuntu-14.04-amd64.box
```

### Initialize a `Vagrantfile`

```bash
vagrant init
```

### Edit the `Vagrantfile`

Edit `Vagrantfile` and ensure the following keys are set (certain keys may already exist commented — just uncomment & modify them if so):

```
config.vm.box = "cfy-training"
config.vm.network "private_network", ip: "192.168.33.10"
```

*Notes*:

1. Certain keys may already exist; make sure that their values match the values above and change if necessary.
2. There may be multiple `config.vm.network` keys. The one you need to uncomment and/or edit is the key for `private_network`.

### Start the VM

```bash
vagrant up
```

### Login

SSH into the Vagrant box. Both the username and password are `vagrant`. You may do this using the `vagrant` command-line interface:

```bash
vagrant ssh
```

That will start your local SSH client against the Vagrant box. Alternatively:

```bash
ssh vagrant@192.168.33.10
```

Or, on Windows, you can use PuTTY:

```bat
putty.exe vagrant@192.168.33.10 -pw vagrant
```

### In the VM

Once you've `ssh`'d into the box, run the following:

```bash
sudo apt-get update
sudo apt-get -y install python-pip python-virtualenv python-dev unzip git
curl http://gigaspaces-repository-eu.s3.amazonaws.com/org/cloudify3/get-cloudify.py -o get-cloudify.py
python get-cloudify.py --virtualenv cfyenv --version 3.2a8
```

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
Cloudify CLI 3.2.0-m8     (build: 85, date: )
```