# Lab: Workflows

Ensure that the `LAB_ROOT` environment variable points to the exercise's root directory by executing:

```bash
export LAB_ROOT=~/cloudify-training-labs/workflows/exercise
```

## Part I: `execute_operation`

`$LAB_ROOT/blueprint/blueprint.yaml` is a very simple blueprint, defining a node called `lab`.
Your task consists of:

1.  Add an operation to the `lab` node
2.  Bind the operation to the included script, `scripts/my-logging-operation.sh`
3.  Use the `execute_operation` workflow to invoke the script

### Step 1: Replace placeholders

Grep the blueprint for `REPLACE_WITH`. Replace that string with an operation definition.

### Step 2: Run in local mode

Run the `execute_operation` workflow in local mode:

```bash
cfy init $LAB_ROOT/blueprint/blueprint.yaml -b workflows
cfy executions start -b workflows -p ~/execution-parameters.yaml execute_operation
```

The `execution-parameters.yaml` file should be a YAML file that you create, containing parameters to pass to the `execute_operation` workflow, such as:

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
cfy node-instances -b workflows
```

The output shows all node instances in the topology. For each node instance, both the instance ID and the node ID are shown. The node ID is the name of the
node in the blueprint; the node instance ID is the ID of the particular instance of that node.

Then, execute the `heal` workflow. For example:

```bash
cfy executions start -b workflows -p 'node_instance_id=lab_vm_a644a' heal
```

## Part III: Uninstall

Use the commands learned in previous labs to uninstall the lab application.
