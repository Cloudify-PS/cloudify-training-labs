# Lab 2 - Bootstrap a Manager

The purpose of this lab is to bootstrap a cloudify manager on a fresh instance using the simple manager blueprint. 
Before starting, make sure you have the following details from the trainer: 
*	The private and public IP of the server you should bootstrap on. One server per trainee. 
*	The keypair of the server 

*Step 1: Download the manager blueprint*
In a terminal window (where you installed the CLI) execute the following command: 
wget https://github.com/cloudify-cosmo/cloudify-manager-blueprints/archive/3.1.zip
unzip 3.1.zip
cd cloudify-manager-blueprints-3.1/simple
*Step 2: Configure the inputs file*
cp inputs.json.template inputs.json
vi inputs.json

Fill in the public and private IP, ssh user (ubuntu), as well as the path of the keyfile you were given by the trainer: 
{
    "public_ip": "PUBLIC IP GOES HERE",
    "private_ip": "PRIVATE IP GOES HERE",
    "ssh_user": "ubuntu",
    "ssh_key_filename": "/path/to/key.pem",

    "agents_user": "ubuntu",
    "resources_prefix": ""
}
Step 3: Trigger the bootstrap process
Activate the virtualenv in which you installed the Cloudify CLI, and type the following: 
cfy init
cfy bootstrap --install-plugins -p simple.yaml -i inputs.json

This should take a few minutes, during which you will see the output of the bootstrapping process. At the end of the process you should see the IP address of the manager, e.g.: 

015-01-20 16:13:15 CFY <manager> 'install' workflow execution succeeded
bootstrapping complete
management server is up at 54.91.114.221

Step 4: Verify the manager started successfully 
Type the following command to verify that all manager components are up and running: 
cfy status

You should see the output similar to the following, make sure all components are running:
Getting management services status... [ip=54.91.114.221]

Services:
+--------------------------------+---------+
|            service             |  status |
+--------------------------------+---------+
| Riemann                        | running |
| Celery Management              | running |
| RabbitMQ                       | running |
| Cloudify Manager               | running |
| Elasticsearch                  | running |
| SSH                            | running |
| Webserver                      | running |
| Cloudify UI                    | running |
| Syslog                         | running |
| Logstash                       | running |
+--------------------------------+---------+

Step 5: Access the web UI
Copy the IP address you received at the end of the bootstrap process to your browser's address line. You should get the web UI: 

  






xxxxxxxxxxxxxxx

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
```

```bash
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

