# Lab: Installing Application using Cloudify Manager

In this lab, we will install a sample application on Cloudify Manager.

We will install the Cloudify "Hello World" application, available on your CLI VM under `~/hello-world`.

## Step 1: Switch CLI to use your manager

Make sure that your CLI's active profile points at a Cloudify Manager:

```bash
cfy profiles list
```

Otherwise, use the `cfy profiles use` command to switch to a Cloudify Manager profile.

## Step 2: Upload the blueprint

```bash
cfy blueprints upload ~/hello-world/singlehost-blueprint.yaml -b helloworld
```

## Step 3: Create an inputs file

The `hello-world` blueprint requires a few inputs. For convenience, prepare a YAML file with values for those inputs:

```bash
vi ~/hw-inputs.yaml
```

Populate the following parameters:

```yaml
server_ip: <your-app-vm-ip-address>
agent_user: centos
agent_private_key_path: /etc/cloudify/cfy-training.pem
```

## Step 4: Create a deployment

```bash
cfy deployments create hw1 -b helloworld -i ~/hw-inputs.yaml
```

## Step 5: Install the topology

```bash
cfy executions start install -d hw1
```

## Step 6: Access the application

The application can now be accessed by going to `http://<app-vm-ip>:8080`.

## Step 7: Uninstall the application

```bash
cfy uninstall hw1
```

This will run the `uninstall` workflow, and then delete the `hw1` deployment and its associated blueprint.
