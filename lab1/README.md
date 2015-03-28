# Lab 1: Configuring Vagrant and Installing CLI

## Prerequisites

### Install Vagrant
Download from [http://www.vagrantup.com/downloads.html] (http://www.vagrantup.com/downloads.html)

### Install the vbguest plugin
Check whether the vbguest plugin is installed:

```bash
vagrant plugin list
```

If `vagrant-vbguest` is not listed, install it:

```bash
vagrant plugin install vagrant-vbguest
```

## Process

### Download ubuntu-14.04 vagrant box
Download [https://github.com/kraksoft/vagrant-box-ubuntu/releases/download/14.04/ubuntu-14.04-amd64.box](https://github.com/kraksoft/vagrant-box-ubuntu/releases/download/14.04/ubuntu-14.04-amd64.box)

```bash
wget https://github.com/kraksoft/vagrant-box-ubuntu/releases/download/14.04/ubuntu-14.04-amd64.box
```

### Add the box to vagrant:

```bash
vagrant box add --name ub1404 ubuntu-14.04-amd64.box
```

### initialize a vagrant file  
```bash
vagrant init 
```

### Vagrantfile
Edit the Vagrantfile and set the following in the Vagrantfile (make sure it's uncommented)
```bash
config.vm.box = "ub1404"
config.vm.network "private_network", ip: "192.168.33.10"
```

### Start the vm
```bash
vagrant up
```

### Login
Now use one of the following (user and password are vagrant):
```bash
vagrant ssh 
 #or
ssh vagrant@192.168.33.10
```
 or on Windows
```bat
 putty.exe -ssh 192.168.33.10 -l vagrant -pw vagrant
```

### In the VM
Once you've ssh'd into the box, run the following (use sudo only if you're not root).

If your image isn't updated: 
```bash
sudo apt-get -y -q update
```

```bash
sudo apt-get install -y -q python-dev python-virtualenv unzip
```

### Create virtualenv name myenv
```bash
virtualenv myenv
```

### Activate the myenv virtualenv
```bash
source myenv/bin/activate
```

### Installation
```bash
pip install cloudify==3.2
```

### Run the following command : 
```bash
cfy --version
```

#### You should see the following output :
```bat
 Cloudify CLI 3.2.0     (build: 85, date: )
```