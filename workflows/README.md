# Lab: Workflows

It is assumed that the `LAB_ROOT` environment variable points to the exercise's root directory. Otherwise, export it:

```bash
export LAB_ROOT=~/cloudify-training-labs/workflows/exercise
```

## Part I: `execute_operation`

### Step 1: Replace placeholders

In `$LAB_ROOT`, you’ll find a folder which contains the `hello-tomcat` blueprint, where an additional interface has been added to the `web_server` type, and an additional simple script `my-logging-operation.sh` now appears.

Replace **_all_** the occurrences of the placeholders (“`REPLACE_WITH`”) wherever they are located under `$LAB_ROOT` (you can use `grep` to look for these occurrences), with suitable values. At the end, the `tomcat_server` node will have an operation mapping for the new interface, and so that the mapping's implementation will be the new `my-logging-operation.sh` script. Note that the latter uses a `message` parameter.

### Step 2: Run in local mode

Run the `execute_operation` workflow in local mode (you should be able to complete the commands by yourself):

```bash
cd $LAB_ROOT
cfy local init -p blueprint/blueprint.yaml -i inputs/local.yaml
cfy local execute -w execute_operation -p <execution-parameters.yaml> ...
```

The `<execution-parameters.yaml>` file should be a YAML file that you create, containing parameters to pass to the `execute_operation` workflow, such as:

* `operation`
* `node_ids`
* etc.

The execution should pass a message as a parameter (rather than the message being an input of the operation in the blueprint). *Note that the operation should only be performed on the relevant node instance*.

_Tip_: Use the `execute_operation` workflow documentation.

## Part II: `heal`

In this part, we will demonstrate the `heal` workflow.

First, we need to find the instance ID of the node we would like to heal. Remember: the `heal` workflow uninstalls, and then reinstalls, the *entire* Compute node containing the node we wish to heal; therefore, you may either look for the instance ID of the Compute node itself, or of any node which is contained in (directly or indirectly) that Compute node.

To find the node instance, execute the following command (from the CLI VM):

```bash
cfy local instances
```

Then, execute the `heal` workflow. For example:

```bash
cfy local execute -w heal -p 'node_instance_id: host_f4c49'
```

## Part III: `scale`

In this part, we will demonstrate the `scale` workflow.

### Step 1: Execute the `scale` workflow

First, we need to find the ID of the node we would like to scale (*note*: unlike the `heal` workflow, the `scale` workflow requires the node's ID, *not* a node's instance ID).

We will scale the `scale_node` node.

```bash
cfy local execute -w scale -p '{node_id: scale_node, scale_compute: false, delta: 1}'
```

### Step 2: Verify

Run the following command:

```bash
cfy local instances
```

And verify that another node instance was added for the `scale_node` node.

### Step 3: Scale down

Execute a similar command, to scale the `scale_node` node down by 1:

```bash
cfy local execute -w scale -p '{node_id: scale_node, scale_compute: false, delta: -1}'
```

### Step 4: Verify

At the same view as in Step 2 above, you should now see that the instance count of `scale_node` has decreased to 1.

## Part IV: Uninstall

Use the commands learned in previous labs to uninstall the deployment you had created, delete the deployment and remove the `hello-tomcat` application.
