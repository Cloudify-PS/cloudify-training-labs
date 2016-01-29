# Lab 8: Workflows

It is assumed that the `LAB_ROOT` environment variable points to the exercise's root directory. Otherwise, export it:

```bash
export LAB_ROOT=~/cloudify-training-labs/lab6/exercise
```

## Part I: `execute_operation`

### Step 1: Replace placeholders

In `$LAB_ROOT`, you’ll find a folder which contains the `hello-tomcat` blueprint, where an additional interface has been added to the `web_server` type, and an additional simple script `my-logging-operation.sh` now appears.

Replace **_all_** the occurrences of the placeholders (“`REPLACE_WITH`”) wherever they are located under `$LAB_ROOT` (you can use `grep` to look for these occurrences), with suitable values. At the end, the `tomcat_server` node will have an operation mapping for the new interface, and so that the mapping's implementation will be the new `my-logging-operation.sh` script. Note that the latter uses a `message` parameter.

### Step 2: Run in local mode

Run the `execute_operation` workflow in local mode (you should be able to complete the commands by yourself):

```bash
cd $LAB_ROOT
cfy local init -p ... -i ...
cfy local execute -w execute_operation -p <execution-parameters.yaml> ...
```

The `<execution-parameters.yaml>` file should be a YAML file that you create, containing parameters to pass to the `execute_operation` workflow, such as:

* `operation`
* `node_ids`
* etc.

The execution should pass a message as a parameter (rather than the message being an input of the operation in the blueprint). *Note that the operation should only be performed on the relevant node instance*.

_Tip_: Use the `execute_operation` workflow documentation.
