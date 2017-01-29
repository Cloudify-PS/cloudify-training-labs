# Lab: Running a Basic Blueprint Locally

In this lab, we will run a very basic blueprint using Cloudify.

From within the VM containing the Cloudify CLI, create a directory to be used for Cloudify's local run:

```bash
mkdir -p ~/cfylocal && cd ~/cfylocal
```

Next, initialize a Cloudify environment, using the basic blueprint:

```bash
cfy local init -p ~/cloudify-training-labs/running-basic-locally/blueprint/basic.yaml
```

## Invoke the `install` workflow

```bash
cfy local execute -w install
```

The output should be similar to the following:

```
2017-01-29 01:10:07 CFY <local> Starting 'install' workflow execution
2017-01-29 01:10:07 CFY <local> [my_host_p0gwyb] Creating node
2017-01-29 01:10:07 CFY <local> [my_host_p0gwyb] Configuring node
2017-01-29 01:10:08 CFY <local> [my_host_p0gwyb] Starting node
2017-01-29 01:10:09 CFY <local> [my_application_l0cx8e] Creating node
2017-01-29 01:10:09 CFY <local> [my_application_l0cx8e.create] Sending task 'script_runner.tasks.run'
2017-01-29 01:10:09 CFY <local> [my_application_l0cx8e.create] Task started 'script_runner.tasks.run'
2017-01-29 01:10:09 LOG <local> [my_application_l0cx8e.create] INFO: Executing: /tmp/tmpS6QSbs-creating.sh
2017-01-29 01:10:09 LOG <local> [my_application_l0cx8e.create] INFO: Creating!
2017-01-29 01:10:09 LOG <local> [my_application_l0cx8e.create] INFO: Execution done (return_code=0): /tmp/tmpS6QSbs-creating.sh
2017-01-29 01:10:09 CFY <local> [my_application_l0cx8e.create] Task succeeded 'script_runner.tasks.run'
2017-01-29 01:10:09 CFY <local> [my_application_l0cx8e] Configuring node
2017-01-29 01:10:09 CFY <local> [my_application_l0cx8e.configure] Sending task 'script_runner.tasks.run'
2017-01-29 01:10:09 CFY <local> [my_application_l0cx8e.configure] Task started 'script_runner.tasks.run'
2017-01-29 01:10:09 LOG <local> [my_application_l0cx8e.configure] INFO: Executing: /tmp/tmpTQyGLe-configuring.sh
2017-01-29 01:10:10 LOG <local> [my_application_l0cx8e.configure] INFO: Configuring!
2017-01-29 01:10:10 LOG <local> [my_application_l0cx8e.configure] INFO: Execution done (return_code=0): /tmp/tmpTQyGLe-configuring.sh
2017-01-29 01:10:10 CFY <local> [my_application_l0cx8e.configure] Task succeeded 'script_runner.tasks.run'
2017-01-29 01:10:10 CFY <local> [my_application_l0cx8e] Starting node
2017-01-29 01:10:10 CFY <local> [my_application_l0cx8e.start] Sending task 'script_runner.tasks.run'
2017-01-29 01:10:10 CFY <local> [my_application_l0cx8e.start] Task started 'script_runner.tasks.run'
2017-01-29 01:10:10 LOG <local> [my_application_l0cx8e.start] INFO: Executing: /tmp/tmpuMvXsj-starting.sh
2017-01-29 01:10:11 LOG <local> [my_application_l0cx8e.start] INFO: Starting!
2017-01-29 01:10:11 LOG <local> [my_application_l0cx8e.start] INFO: Execution done (return_code=0): /tmp/tmpuMvXsj-starting.sh
2017-01-29 01:10:11 CFY <local> [my_application_l0cx8e.start] Task succeeded 'script_runner.tasks.run'
2017-01-29 01:10:11 CFY <local> 'install' workflow execution succeeded
```

## Invoke the `uninstall` workflow

```bash
cfy local execute -w uninstall
```

The output should be similar to the following:

```
2017-01-29 01:10:32 CFY <local> Starting 'uninstall' workflow execution
2017-01-29 01:10:33 CFY <local> [my_application_l0cx8e] Stopping node
2017-01-29 01:10:33 CFY <local> [my_application_l0cx8e.stop] Sending task 'script_runner.tasks.run'
2017-01-29 01:10:33 CFY <local> [my_application_l0cx8e.stop] Task started 'script_runner.tasks.run'
2017-01-29 01:10:33 LOG <local> [my_application_l0cx8e.stop] INFO: Executing: /tmp/tmplSh7dC-stopping.sh
2017-01-29 01:10:33 LOG <local> [my_application_l0cx8e.stop] INFO: Stopping!
2017-01-29 01:10:33 LOG <local> [my_application_l0cx8e.stop] INFO: Execution done (return_code=0): /tmp/tmplSh7dC-stopping.sh
2017-01-29 01:10:33 CFY <local> [my_application_l0cx8e.stop] Task succeeded 'script_runner.tasks.run'
2017-01-29 01:10:34 CFY <local> [my_application_l0cx8e] Deleting node
2017-01-29 01:10:34 CFY <local> [my_application_l0cx8e.delete] Sending task 'script_runner.tasks.run'
2017-01-29 01:10:34 CFY <local> [my_application_l0cx8e.delete] Task started 'script_runner.tasks.run'
2017-01-29 01:10:34 LOG <local> [my_application_l0cx8e.delete] INFO: Executing: /tmp/tmp1KcTsp-deleting.sh
2017-01-29 01:10:34 LOG <local> [my_application_l0cx8e.delete] INFO: Deleting!
2017-01-29 01:10:34 LOG <local> [my_application_l0cx8e.delete] INFO: Execution done (return_code=0): /tmp/tmp1KcTsp-deleting.sh
2017-01-29 01:10:34 CFY <local> [my_application_l0cx8e.delete] Task succeeded 'script_runner.tasks.run'
2017-01-29 01:10:35 CFY <local> [my_host_p0gwyb] Stopping node
2017-01-29 01:10:35 CFY <local> [my_host_p0gwyb] Deleting node
2017-01-29 01:10:36 CFY <local> 'uninstall' workflow execution succeeded
```

## Invoke it all at once

Since the sequence of initializing a blueprint and running the `install` workflow is very common,
there is a command that performs both at the same time:

```bash
cfy local install -p ~/cloudify-training-labs/running-basic-locally/blueprint/basic.yaml
```

Conversely, the `cfy local uninstall` command runs the `uninstall` workflow.