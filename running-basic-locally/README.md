# Lab: Running Basic Blueprint Locally

In this lab, we will run a very basic blueprint using Cloudify.

**NOTE**: The basic blueprint demonstrated in the slides is a fully-working blueprint. However, in order to run the blueprint
in so-called "local mode" (without a manager installed), a few extra lines have to be added (specifying
`install_method` as `none`).

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
2016-01-31 20:23:12 CFY <local> Starting 'install' workflow execution
2016-01-31 20:23:13 CFY <local> [main_host_151fc] Creating node
2016-01-31 20:23:13 CFY <local> [main_host_151fc] Configuring node
2016-01-31 20:23:13 CFY <local> [main_host_151fc] Starting node
2016-01-31 20:23:14 CFY <local> [test_application_server_24925] Creating node
2016-01-31 20:23:14 CFY <local> [test_application_server_24925.create] Sending task 'script_runner.tasks.run'
2016-01-31 20:23:14 CFY <local> [test_application_server_24925.create] Task started 'script_runner.tasks.run'
2016-01-31 20:23:14 LOG <local> [test_application_server_24925.create] INFO: Executing: /tmp/tmpsegkLw-creating.sh
2016-01-31 20:23:14 LOG <local> [test_application_server_24925.create] INFO: Creating!
2016-01-31 20:23:14 LOG <local> [test_application_server_24925.create] INFO: Execution done (return_code=0): /tmp/tmpsegkLw-creating.sh
2016-01-31 20:23:14 CFY <local> [test_application_server_24925.create] Task succeeded 'script_runner.tasks.run'
2016-01-31 20:23:15 CFY <local> [test_application_server_24925] Configuring node
2016-01-31 20:23:15 CFY <local> [test_application_server_24925.configure] Sending task 'script_runner.tasks.run'
2016-01-31 20:23:15 CFY <local> [test_application_server_24925.configure] Task started 'script_runner.tasks.run'
2016-01-31 20:23:15 LOG <local> [test_application_server_24925.configure] INFO: Executing: /tmp/tmpwefdQ5-configuring.sh
2016-01-31 20:23:15 LOG <local> [test_application_server_24925.configure] INFO: Configuring!
2016-01-31 20:23:15 LOG <local> [test_application_server_24925.configure] INFO: Execution done (return_code=0): /tmp/tmpwefdQ5-configuring.sh
2016-01-31 20:23:15 CFY <local> [test_application_server_24925.configure] Task succeeded 'script_runner.tasks.run'
2016-01-31 20:23:15 CFY <local> [test_application_server_24925] Starting node
2016-01-31 20:23:15 CFY <local> [test_application_server_24925.start] Sending task 'script_runner.tasks.run'
2016-01-31 20:23:15 CFY <local> [test_application_server_24925.start] Task started 'script_runner.tasks.run'
2016-01-31 20:23:15 LOG <local> [test_application_server_24925.start] INFO: Executing: /tmp/tmpqsRbCT-starting.sh
2016-01-31 20:23:16 LOG <local> [test_application_server_24925.start] INFO: Starting!
2016-01-31 20:23:16 LOG <local> [test_application_server_24925.start] INFO: Execution done (return_code=0): /tmp/tmpqsRbCT-starting.sh
2016-01-31 20:23:16 CFY <local> [test_application_server_24925.start] Task succeeded 'script_runner.tasks.run'
2016-01-31 20:23:16 CFY <local> 'install' workflow execution succeeded
```

## Invoke the `uninstall` workflow

```bash
cfy local execute -w uninstall
```

The output should be similar to the following:

```
2016-01-31 20:23:43 CFY <local> Starting 'uninstall' workflow execution
2016-01-31 20:23:43 CFY <local> [test_application_server_24925] Stopping node
2016-01-31 20:23:44 CFY <local> [test_application_server_24925.stop] Sending task 'script_runner.tasks.run'
2016-01-31 20:23:44 CFY <local> [test_application_server_24925.stop] Task started 'script_runner.tasks.run'
2016-01-31 20:23:44 LOG <local> [test_application_server_24925.stop] INFO: Executing: /tmp/tmpQpz21r-stopping.sh
2016-01-31 20:23:44 LOG <local> [test_application_server_24925.stop] INFO: Stopping!
2016-01-31 20:23:44 LOG <local> [test_application_server_24925.stop] INFO: Execution done (return_code=0): /tmp/tmpQpz21r-stopping.sh
2016-01-31 20:23:44 CFY <local> [test_application_server_24925.stop] Task succeeded 'script_runner.tasks.run'
2016-01-31 20:23:44 CFY <local> [test_application_server_24925] Deleting node
2016-01-31 20:23:44 CFY <local> [test_application_server_24925.delete] Sending task 'script_runner.tasks.run'
2016-01-31 20:23:44 CFY <local> [test_application_server_24925.delete] Task started 'script_runner.tasks.run'
2016-01-31 20:23:44 LOG <local> [test_application_server_24925.delete] INFO: Executing: /tmp/tmpwitsRv-deleting.sh
2016-01-31 20:23:44 LOG <local> [test_application_server_24925.delete] INFO: Deleting!
2016-01-31 20:23:45 LOG <local> [test_application_server_24925.delete] INFO: Execution done (return_code=0): /tmp/tmpwitsRv-deleting.sh
2016-01-31 20:23:45 CFY <local> [test_application_server_24925.delete] Task succeeded 'script_runner.tasks.run'
2016-01-31 20:23:45 CFY <local> [main_host_151fc] Stopping node
2016-01-31 20:23:46 CFY <local> [main_host_151fc] Deleting node
2016-01-31 20:23:46 CFY <local> 'uninstall' workflow execution succeeded
```
