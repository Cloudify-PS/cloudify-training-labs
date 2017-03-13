# Graph-based Workflow lab

In this lab we will be execute a complex, graph-based workflow that will stop a running VM,
delete all existing VM volume snapshots, create fresh snapshots, and start the VM again.

This lab requires Amazon Web Services (AWS) API access as well as a running AWS EC2 instance
running. Before attempting to run this lab, make sure you the following information on hand:

* AWS API access key ID
* AWS API secret access key
* AWS region name (ex. "us-east-1")
* A running AWS EC2 instance ID


## Usage

Since this lab folder includes both the blueprint as well as the needed plugin, there's no need to do separate operations to load the plugin.

**Running on a Cloudify Manager**

```bash
# Upload the blueprint (and plugin) to a manager
cfy blueprints upload -b lab-graphs-wf -p exercise/blueprint.yaml

# Create a new deployment from the blueprint
cfy deployments create -d lab-graphs-wf-01 -b lab-graphs-wf -i exercise/inputs.yaml

# Execute the custom workflow
cfy executions start -d lab-graphs-wf-01 -w refresh_snapshots -l
```

**Running locally** _(requires being in a VirtualEnv)_

```bash
# Uninstall any previously installed version of the plugin
# Windows users: If using Cygwin, use "winpty" before "pip".
pip uninstall -y lab-wf-graphs-plugin

# Install the local plugin into your VirtualEnv
pip install ./exercise/plugins/lab/

# Initialize the deployment and execute the custom workflow
cfy local install --install-plugins --debug \
	--blueprint-path exercise/blueprint.yaml \
    --inputs exercise/inputs.yaml \
    --task-retries 60 --task-retry-interval 15 \
    --workflow refresh_snapshots
```


## Lab tasks


### Task \#1

Run the custom workflow (see the `Usage` section above) and make sure it's working. If you're
logged into your AWS console, you should see the EC2 instance stop, take a snapshot, and start again.

*DON'T FORGET TO UPDATES YOUR `inputs.yaml` FILE!*

### Task \#2

Remove the `create_snapshots` operation from the `hacker.aws.nodes.Instance` node type and
make any updates necessary to the plugin / workflow itself to make it work.
The result should be that the instance will stop, delete all of its snapshots, and
start back up without ever creating new snapshots.

Remember, if running locally, you'll need to remove and re-install the plugin package after making
changes to the plugin / workflow code. This is outlined in the first 2 steps of `Running locally`.

### Task \#3

Rename the folder at `<labroot>/exercise/plugins/lab` to `<labroot>/exercise/plugins/custom` and fix any newly broken references. *hint: check plugin.yaml*

Delete your existing deployment & blueprint and re-run everything to make sure it works.
