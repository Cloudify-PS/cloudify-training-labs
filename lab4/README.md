# Lab 4: Using Scripts in Lifecycle Events

The purpose of this lab is to fix a broken blueprint, install it locally and also upload it a Cloudify Manager.

It is assumed that the `LAB_ROOT` environment variable points to the exercise's root directory. Otherwise, export it:

```bash
export LAB_ROOT=~/cloudify-training-labs/lab4/exercise
```

### Step 1: Replace placeholders

You need to replace **_all_** the occurrences of the placeholders (“`REPLACE_WITH`”) wherever they are located under
`$LAB_ROOT` (you can use `grep` to look for these occurrences), with the suitable values and to add missing parts as
well. 

### Step 2: Run in local mode

Once you're done, you can run the application in local mode:

```bash
cd ~/work
cfy local init -p $LAB_ROOT/hello-tomcat/tomcat-blueprint.yaml -i $LAB_ROOT/hello-tomcat/tomcat-local.yaml
cfy local execute -w install
```

Now browse to `http://127.0.0.1:8081/helloworld` (from the CLI machine, or `http://<cli-machine-public-ip>:8081/helloworld`
from elsewhere) and then run the following CLI command:

```bash
cfy local outputs
```

To clean up:

```bash
cfy local execute -w uninstall
```