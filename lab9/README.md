# Lab 9: Workflows

## Part I: `execute_workflow`

In the exercise folder of this lab, you’ll find a folder which contains the `hello-tomcat` blueprint, where an additional interface has been added to the `web_server` type, and an additional simple script `my-logging-operation.sh` now appears.

Your task is to fix this blueprint, so that the `tomcat_server` node will have an operation mapping for the new interface, and so that the mapping's implementation will be the new `my-logging-operation.sh` script. Note that the latter uses a `message` parameter.

Then, run the `execute_operation` plugin (in local mode):

```bash
cfy local init -p ... -i ...
cfy local execute -w execute_operation ...
```

The execution should pass a message as a parameter (rather than the message being an input of the operation in the blueprint). Note that the operation should only be performed on the relevant node instance (there is more than one way to achieve this).

_Tip_: Use the `execute_operation` workflow documentation.

## Part II: `heal`

In this part, we will demonstrate the usage of the `heal` internal workflow.

### Step 1: Deploy and install the `hello-tomcat` application

In Part I, you ran the `hello-tomcat` application in local mode. Use commands studied in previous labs to install `hello-tomcat` on your Cloudify Manager.

For the purpose of this exercise, it will be assumed that the deployment's name is `hellotomcat`.

### Step 2: Execute the `heal` workflow

First, we need to find the instance ID of the node we would like to heal. Remember: the `heal` workflow uninstalls, and then reinstalls, the *entire* Compute node containing the node we wish to heal; therefore, you may either look for the instance ID of the Compute node itself, or of any node which is contained in (directly or indirectly) that Compute node.

Then, execute the `heal` workflow. For example:

```bash
cfy executions start -d hellotomcat -w heal -p 'node_instance_id: host_f4c49'
```

## Part III: `scale`

### Step 1: Execute the `scale` workflow

First, we need to find the ID of the node we would like to scale (*note*: unlike the `heal` workflow, the `scale` workflow requires the node's ID, *not* a node's instance ID).

We will scale the `tomcat_server` node.

```bash
cfy executions start -d hellotomcat -w scale -p '{node_id: tomcat_server, scale_compute: false, delta: 1}'
```

### Step 2: Verify

Log in to the Cloudify web UI. Select your deployment and then the "Topology" tab. You should see that the number of instances of the `tomcat_server` node has changed to `2`.

### Step 3: Scale down

Execute a similar command, to scale the `tomcat_server` node down by 1:

```bash
cfy executions start -d hellotomcat -w scale -p '{node_id: tomcat_server, scale_compute: false, delta: -1}'
```

### Step 4: Verify

At the same view as in Step 2 above, you should now see that the instance count of `tomcat_server` has decreased to 1.