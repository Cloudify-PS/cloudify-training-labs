FROM       phusion/baseimage:latest 

# Update apt-get sources AND install MongoDB
RUN apt-get update && apt-get install -y git nodejs npm

# Install application sources 
RUN git clone https://github.com/cloudify-cosmo/nodecellar.git

WORKDIR /nodecellar

# Install node modules 
RUN npm install --silent
