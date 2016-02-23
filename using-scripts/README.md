# Lab 4: Using Scripts in Lifecycle Events

The purpose of this lab is to fix a broken blueprint, install it locally and also upload it a Cloudify Manager.

It is assumed that the `LAB_ROOT` environment variable points to the exercise's root directory. Otherwise, export it:

```bash
export LAB_ROOT=~/cloudify-training-labs/using-scripts/exercise
```

### Step 1: Replace placeholders

You need to replace **_all_** the occurrences of the placeholders (“`REPLACE_WITH`”) wherever they are located under
`$LAB_ROOT`, with the suitable values and to add missing parts as well.
 
To search:

```bash
grep -r "REPLACE_WITH" $LAB_ROOT
```

### Step 2: Run in local mode

Once you're done, you can run the application in local mode:

```bash
cd ~/work
cfy local init -p $LAB_ROOT/blueprint/blueprint.yaml -i $LAB_ROOT/inputs/local.yaml
cfy local execute -w install
```

Then, run the following CLI command:

```bash
cfy local outputs
```

This command will display the deployment's outputs, as defined in the application's blueprint.

Browse to `http://<cli-machine-public-ip>:8081/helloworld`. The test application should show up:

![HelloWorld app](../../../raw/master/using-scripts/helloworld.png "HelloWorld app")

To clean up:

```bash
cfy local execute -w uninstall
```
