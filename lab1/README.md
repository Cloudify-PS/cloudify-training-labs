# LAB 1

### Download ubuntu-14.04 vagrant box
Download [https://github.com/kraksoft/vagrant-box-ubuntu/releases/download/14.04/ubuntu-14.04-amd64.box](https://github.com/kraksoft/vagrant-box-ubuntu/releases/download/14.04/ubuntu-14.04-amd64.box)

```bash
wget https://github.com/kraksoft/vagrant-box-ubuntu/releases/download/14.04/ubuntu-14.04-amd64.box
```

### Add the box to vagrant:

```bash
vagrant box add --name ub1404 ubuntu-14.04-amd64-vbox.box
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
If you image isn't updated : 
```bash
sudo apt-get -y -q update 
sudo apt-get install -y -q python-dev
sudo apt-get install -y -q python-virtualenv
sudo apt-get install -y -q unzip 
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
pip install cloudify==3.1
```

### Run the following command : 
```bash
cfy --version
```

#### You should see the following output :
```bat
 Cloudify CLI 3.1.0     (build: 85, date: )
```

### Get the manager blueprints repo content:

Download [!(https://github.com/cloudify-cosmo/cloudify-manager-blueprints/archive/3.1.zip)](https://github.com/cloudify-cosmo/cloudify-manager-blueprints/archive/3.1.zip)
```bash
wget https://github.com/cloudify-cosmo/cloudify-manager-blueprints/archive/3.1.zip
```

### unzip 
```bash
unzip 3.1.zip
```

