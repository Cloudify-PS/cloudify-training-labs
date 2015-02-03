#Download ubuntu-14.04 vagrant box
wget https://github.com/kraksoft/vagrant-box-ubuntu/releases/download/14.04/ubuntu-14.04-amd64.box

# Add the box to vagrant:
vagrant box add --name ub1404 ubuntu-14.04-amd64-vbox.box

# initialize a vagrant file  
vagrant init 

# Edit the Vagrantfile and set the following in the Vagrantfile (make sure it's uncommented)
config.vm.box = "ub1404"
config.vm.network "private_network", ip: "192.168.33.10"

# Start the vm
vagrant up

# Now use one of the following (user and password are vagrant):
vagrant ssh 

# or
ssh vagrant@192.168.33.10

# or on win
putty.exe -ssh 192.168.33.10 -l vagrant -pw vagrant

# Once you've ssh'd into the box run the following (use sudo only if you're not root): 

# If you image isn't updated : 
# sudo apt-get -y -q update 

sudo apt-get install -y -q python-dev
sudo apt-get install -y -q python-virtualenv
sudo apt-get install -y -q unzip 

# Create virtualenv name myenv
virtualenv myenv

# Activate the myenv virtualenv
source myenv/bin/activate

# Install...
pip install cloudify==3.1

# Run the following command : 
cfy --version
# You should see the following output :
# Cloudify CLI 3.1.0     (build: 85, date: )

# Get the manager blueprints repo content:
wget https://github.com/cloudify-cosmo/cloudify-manager-blueprints/archive/3.1.zip

# unzip 
unzip 3.1.zip


