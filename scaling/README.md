# Lab: Manager Scaling

The purpose of this lab is to deploy and scale an example web application.

## Step 1: Download example application

```bash
cd ~
curl -L -o helloworld.zip https://github.com/cloudify-cosmo/cloudify-hello-world-example/archive/3.4.zip
unzip helloworld.zip
mv cloudify-hello-world-example-3.4 cloudify-hello-world
```

This will download the latest Hello World example application and extract it to `~/cloudify-hello-world`.


## Step 2: Copy scaling blueprint to application root

```bash
cp ~/cloudify-training-labs/scaling/scaling-blueprint.yaml cloudify-hello-world/
```

This will copy our scaling blueprint into the application root directory.

## Step 3: Prepare inputs file

```bash
cd ~/work
cp ~/cloudify-training-labs/scaling/inputs.yaml.template scaling-inputs.yaml
```

Then edit the file `scaling-inputs.yaml`:

```yaml
default_scale_count: 1
vm_image_id: <image-id>
vm_flavor: <flavor-id>
webserver_port: 8080
agent_user: centos
```

## Step 4: Deploy the application

```bash
cfy blueprints upload -b appscale -p ~/cloudify-hello-world/scaling-blueprint.yaml
cfy deployments create -d appscale -b appscale -i scaling-inputs.yaml
cfy executions start -w install -d appscale -l
```

This will upload the blueprint, create a deployment, and execute the deployment's `install` workflow. By default,
this will instantiate one instance (with a public IP) and expose port 8080/HTTP to show a Cloudify
example web page.

## Step 5: Scale the application

```bash
cfy executions start -w scale -p '{"delta":1,"scalable_entity_name":"vm_and_ip"}' -d appscale -l
```

This will execute the deployment's "scale" workflow which will, in turn, scale the application
to 2 instances (from 1 instance).  The `delta` parameter determines by how much to scale an application.
This will also give each new instance its own public IP address.

To scale back an application, simply use a negative number for the `delta` parameter:

```bash
cfy executions start -w scale -p '{"delta":-1,"scalable_entity_name":"vm_and_ip"}' -d appscale -l
```

## Step 6: Cleanup

```bash
cfy executions start -w uninstall -d appscale -l
cfy deployments delete -d appscale
cfy blueprints delete -b appscale
```
