# Lab: Workflows

Ensure that the `LAB_ROOT` environment variable points to the exercise's root directory by executing:

```bash
export LAB_ROOT=~/cloudify-training-labs/workflows/exercise
```

## Part I: `execute_operation`

`$LAB_ROOT/blueprint/blueprint.yaml` is a very simple blueprint, defining a node called `lab`.
Your task consists of:

1.  Adding an operation to the `lab` node
2.  Binding the operation to the included script, `scripts/my-logging-operation.sh`
3.  Using the `execute_operation` workflow to invoke the script

### Step 1: Replace placeholders

Grep the blueprint for `REPLACE_WITH`. Replace that string with an operation definition.

### Step 2: Test your changes

Install the blueprint on the manager:

```bash
cfy install $LAB_ROOT/blueprint/blueprint.yaml -b workflows -d workflows -i ip=<your-app-vm-ip>
```

Prepare a file, `~/execution-parameters.yaml`, containing parameters to pass to the `execute_operation` workflow, such as:

* `operation`
* `node_ids`
* etc.

Run the `execute_operation` workflow, providing the `~/execution-parameters.yaml` file as an input:

```bash
cfy executions start execute_operation -d workflows -p ~/execution-parameters.yaml
```

_Tip_: Use the `execute_operation` workflow documentation.

## Part II: `heal`

In this part, we will demonstrate the `heal` workflow.

First, we need to find the instance ID of the node we would like to heal. Remember: the `heal` workflow uninstalls, and then reinstalls, the *entire* Compute node containing the node we wish to heal; therefore, you may either look for the instance ID of the Compute node itself, or of any node which is contained in (directly or indirectly) that Compute node.

To find the node instance, execute the following command (from the CLI VM):

```bash
cfy node-instances list -d workflows
```

The output shows all node instances in the topology. For each node instance, both the instance ID and the node ID are shown. The node ID is the name of the
node in the blueprint; the node instance ID is the ID of the particular instance of that node.

Then, execute the `heal` workflow. For example:

```bash
cfy executions start heal -d workflows -p node_instance_id=lab_vm_a644a
```

## Part III: Uninstall

Use the commands learned in previous labs to uninstall the lab application.
