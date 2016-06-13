# Lab: Running a Basic Blueprint Locally

In this lab, we will run a very basic blueprint using Cloudify.

From within the VM containing the Cloudify CLI, create a directory to be used for Cloudify's local run:

```bash
mkdir ~/cfylocal && cd ~/cfylocal
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
2016-06-13 09:39:16 CFY <local> Starting 'install' workflow execution
2016-06-13 09:39:16 CFY <local> [my_host_841a8] Creating node
2016-06-13 09:39:17 CFY <local> [my_host_841a8] Configuring node
2016-06-13 09:39:17 CFY <local> [my_host_841a8] Starting node
2016-06-13 09:39:18 CFY <local> [my_application_661f7] Creating node
2016-06-13 09:39:18 CFY <local> [my_application_661f7.create] Sending task 'script_runner.tasks.run'
2016-06-13 09:39:18 CFY <local> [my_application_661f7.create] Task started 'script_runner.tasks.run'
2016-06-13 09:39:18 LOG <local> [my_application_661f7.create] INFO: Executing: /tmp/tmpBJQt6Q-creating.sh
2016-06-13 09:39:18 LOG <local> [my_application_661f7.create] INFO: Creating!
2016-06-13 09:39:18 LOG <local> [my_application_661f7.create] INFO: Execution done (return_code=0): /tmp/tmpBJQt6Q-creating.sh
2016-06-13 09:39:18 CFY <local> [my_application_661f7.create] Task succeeded 'script_runner.tasks.run'
2016-06-13 09:39:18 CFY <local> [my_application_661f7] Configuring node
2016-06-13 09:39:19 CFY <local> [my_application_661f7.configure] Sending task 'script_runner.tasks.run'
2016-06-13 09:39:19 CFY <local> [my_application_661f7.configure] Task started 'script_runner.tasks.run'
2016-06-13 09:39:19 LOG <local> [my_application_661f7.configure] INFO: Executing: /tmp/tmpJREpEn-configuring.sh
2016-06-13 09:39:19 LOG <local> [my_application_661f7.configure] INFO: Configuring!
2016-06-13 09:39:19 LOG <local> [my_application_661f7.configure] INFO: Execution done (return_code=0): /tmp/tmpJREpEn-configuring.sh
2016-06-13 09:39:19 CFY <local> [my_application_661f7.configure] Task succeeded 'script_runner.tasks.run'
2016-06-13 09:39:19 CFY <local> [my_application_661f7] Starting node
2016-06-13 09:39:19 CFY <local> [my_application_661f7.start] Sending task 'script_runner.tasks.run'
2016-06-13 09:39:19 CFY <local> [my_application_661f7.start] Task started 'script_runner.tasks.run'
2016-06-13 09:39:19 LOG <local> [my_application_661f7.start] INFO: Executing: /tmp/tmpYSqFcN-starting.sh
2016-06-13 09:39:19 LOG <local> [my_application_661f7.start] INFO: Starting!
2016-06-13 09:39:19 LOG <local> [my_application_661f7.start] INFO: Execution done (return_code=0): /tmp/tmpYSqFcN-starting.sh
2016-06-13 09:39:19 CFY <local> [my_application_661f7.start] Task succeeded 'script_runner.tasks.run'
2016-06-13 09:39:19 CFY <local> 'install' workflow execution succeeded
```

## Invoke the `uninstall` workflow

```bash
cfy local execute -w uninstall
```

The output should be similar to the following:

```
2016-06-13 09:39:39 CFY <local> Starting 'uninstall' workflow execution
2016-06-13 09:39:40 CFY <local> [my_application_661f7] Stopping node
2016-06-13 09:39:40 CFY <local> [my_application_661f7.stop] Sending task 'script_runner.tasks.run'
2016-06-13 09:39:40 CFY <local> [my_application_661f7.stop] Task started 'script_runner.tasks.run'
2016-06-13 09:39:40 LOG <local> [my_application_661f7.stop] INFO: Executing: /tmp/tmpq5iqPw-stopping.sh
2016-06-13 09:39:40 LOG <local> [my_application_661f7.stop] INFO: Stopping!
2016-06-13 09:39:40 LOG <local> [my_application_661f7.stop] INFO: Execution done (return_code=0): /tmp/tmpq5iqPw-stopping.sh
2016-06-13 09:39:40 CFY <local> [my_application_661f7.stop] Task succeeded 'script_runner.tasks.run'
2016-06-13 09:39:40 CFY <local> [my_application_661f7] Deleting node
2016-06-13 09:39:40 CFY <local> [my_application_661f7.delete] Sending task 'script_runner.tasks.run'
2016-06-13 09:39:40 CFY <local> [my_application_661f7.delete] Task started 'script_runner.tasks.run'
2016-06-13 09:39:40 LOG <local> [my_application_661f7.delete] INFO: Executing: /tmp/tmp_PjU1g-deleting.sh
2016-06-13 09:39:41 LOG <local> [my_application_661f7.delete] INFO: Deleting!
2016-06-13 09:39:41 LOG <local> [my_application_661f7.delete] INFO: Execution done (return_code=0): /tmp/tmp_PjU1g-deleting.sh
2016-06-13 09:39:41 CFY <local> [my_application_661f7.delete] Task succeeded 'script_runner.tasks.run'
2016-06-13 09:39:41 CFY <local> [my_host_841a8] Stopping node
2016-06-13 09:39:42 CFY <local> [my_host_841a8] Deleting node
2016-06-13 09:39:42 CFY <local> 'uninstall' workflow execution succeeded
```
