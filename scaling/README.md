# Lab: Manager Scaling

The purpose of this lab is to deploy and scale an example web application.

## Step 1: Download example application

```bash
wget -O helloworld.zip https://github.com/cloudify-cosmo/cloudify-hello-world-example/archive/3.4rc1.zip
unzip helloworld.zip
mv cloudify-hello-world-example-3.4rc1/ cloudify-hello-world
```

This will download the latest Hello World example application and extract it to `./cloudify-hello-world`.


## Step 2: Copy scaling blueprint to application root

```bash
cp scaling-blueprint.yaml ./cloudify-hello-world/
```

This will move our scaling blueprint into the application root directory.


## Step 3: Deploy the application

```bash
cfy blueprints upload -b appscale -p cloudify-hello-world/scaling-blueprint.yaml
cfy deployments create -d appscale -b appscale
cfy executions start -w install -d appscale -l
```

This will upload the blueprint, create a deployment, and execute the deployment's "install" workflow. By default,
this will instantiate 2 AWS EC2 instances (with public IPs) and expose port 8080/HTTP to show a Cloudify
example web page.


## Step 4: Scale the application

```bash
cfy executions start -w scale -p '{"delta": 2, "scalable_entity_name": "vm_and_ip"}' -d appscale
```

This will execute the deployment's "scale" workflow which will, in turn, scale the application
to 4 instances (from 2 instances).  The `delta` parameter determines by how much to scale an application.
This will also give each new instance its own public IP address.

To scale back an application, simply use a negative number for the `delta` parameter.
