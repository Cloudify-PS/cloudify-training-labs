# Lab: Running a Basic Blueprint Locally

In this lab, we will run a very basic blueprint using Cloudify.

As we are going to run this blueprint locally, we need to initialize the CLI's local profile first:

```bash
cfy init ~/cloudify-training-labs/running-basic-locally/blueprint/basic.yaml
```

That initializes the current user's local Cloudify profile by setting the provided blueprint as a context.

## Invoke the `install` workflow

```bash
cfy executions start install
```

The output should be similar to the following:

```
2017-04-08 15:39:19.221  CFY <local> Starting 'install' workflow execution
2017-04-08 15:39:19.342  CFY <local> [my_host_80nls2] Creating node
2017-04-08 15:39:19.772  CFY <local> [my_host_80nls2] Configuring node
2017-04-08 15:39:20.152  CFY <local> [my_host_80nls2] Starting node
2017-04-08 15:39:21.047  CFY <local> [my_application_qlovfd] Creating node
2017-04-08 15:39:21.137  CFY <local> [my_application_qlovfd.create] Sending task 'script_runner.tasks.run'
2017-04-08 15:39:21.162  CFY <local> [my_application_qlovfd.create] Task started 'script_runner.tasks.run'
2017-04-08 15:39:21.237  LOG <local> [my_application_qlovfd.create] INFO: Executing: /tmp/tmpjjK7Zm-creating.sh
2017-04-08 15:39:21.512  LOG <local> [my_application_qlovfd.create] INFO: Creating!
2017-04-08 15:39:21.613  LOG <local> [my_application_qlovfd.create] INFO: Execution done (return_code=0): /tmp/tmpjjK7Zm-creating.sh
2017-04-08 15:39:21.614  CFY <local> [my_application_qlovfd.create] Task succeeded 'script_runner.tasks.run'
2017-04-08 15:39:21.893  CFY <local> [my_application_qlovfd] Configuring node
2017-04-08 15:39:21.951  CFY <local> [my_application_qlovfd.configure] Sending task 'script_runner.tasks.run'
2017-04-08 15:39:21.957  CFY <local> [my_application_qlovfd.configure] Task started 'script_runner.tasks.run'
2017-04-08 15:39:21.958  LOG <local> [my_application_qlovfd.configure] INFO: Executing: /tmp/tmpzDOKnm-configuring.sh
2017-04-08 15:39:22.236  LOG <local> [my_application_qlovfd.configure] INFO: Configuring!
2017-04-08 15:39:22.337  LOG <local> [my_application_qlovfd.configure] INFO: Execution done (return_code=0): /tmp/tmpzDOKnm-configuring.sh
2017-04-08 15:39:22.337  CFY <local> [my_application_qlovfd.configure] Task succeeded 'script_runner.tasks.run'
2017-04-08 15:39:22.684  CFY <local> [my_application_qlovfd] Starting node
2017-04-08 15:39:22.765  CFY <local> [my_application_qlovfd.start] Sending task 'script_runner.tasks.run'
2017-04-08 15:39:22.799  CFY <local> [my_application_qlovfd.start] Task started 'script_runner.tasks.run'
2017-04-08 15:39:22.800  LOG <local> [my_application_qlovfd.start] INFO: Executing: /tmp/tmp4HQSGc-starting.sh
2017-04-08 15:39:23.076  LOG <local> [my_application_qlovfd.start] INFO: Starting!
2017-04-08 15:39:23.177  LOG <local> [my_application_qlovfd.start] INFO: Execution done (return_code=0): /tmp/tmp4HQSGc-starting.sh
2017-04-08 15:39:23.177  CFY <local> [my_application_qlovfd.start] Task succeeded 'script_runner.tasks.run'
2017-04-08 15:39:23.585  CFY <local> 'install' workflow execution succeeded
```

## Invoke the `uninstall` workflow

```bash
cfy executions start uninstall
```

The output should be similar to the following:

```
2017-04-08 15:40:12.877  CFY <local> Starting 'uninstall' workflow execution
2017-04-08 15:40:12.995  CFY <local> [my_application_qlovfd] Stopping node
2017-04-08 15:40:13.182  CFY <local> [my_application_qlovfd.stop] Sending task 'script_runner.tasks.run'
2017-04-08 15:40:13.209  CFY <local> [my_application_qlovfd.stop] Task started 'script_runner.tasks.run'
2017-04-08 15:40:13.286  LOG <local> [my_application_qlovfd.stop] INFO: Executing: /tmp/tmpKi_UMS-stopping.sh
2017-04-08 15:40:13.566  LOG <local> [my_application_qlovfd.stop] INFO: Stopping!
2017-04-08 15:40:13.667  LOG <local> [my_application_qlovfd.stop] INFO: Execution done (return_code=0): /tmp/tmpKi_UMS-stopping.sh
2017-04-08 15:40:13.668  CFY <local> [my_application_qlovfd.stop] Task succeeded 'script_runner.tasks.run'
2017-04-08 15:40:14.129  CFY <local> [my_application_qlovfd] Deleting node
2017-04-08 15:40:14.194  CFY <local> [my_application_qlovfd.delete] Sending task 'script_runner.tasks.run'
2017-04-08 15:40:14.194  CFY <local> [my_application_qlovfd.delete] Task started 'script_runner.tasks.run'
2017-04-08 15:40:14.195  LOG <local> [my_application_qlovfd.delete] INFO: Executing: /tmp/tmpmRWCC4-deleting.sh
2017-04-08 15:40:14.476  LOG <local> [my_application_qlovfd.delete] INFO: Deleting!
2017-04-08 15:40:14.577  LOG <local> [my_application_qlovfd.delete] INFO: Execution done (return_code=0): /tmp/tmpmRWCC4-deleting.sh
2017-04-08 15:40:14.578  CFY <local> [my_application_qlovfd.delete] Task succeeded 'script_runner.tasks.run'
2017-04-08 15:40:14.821  CFY <local> [my_host_80nls2] Stopping node
2017-04-08 15:40:15.665  CFY <local> [my_host_80nls2] Deleting node
2017-04-08 15:40:16.019  CFY <local> 'uninstall' workflow execution succeeded
```

## Invoke it all at once

Since the sequence of initializing a blueprint and running the `install` workflow is very common,
there is a command that performs both at the same time:

```bash
cfy install ~/cloudify-training-labs/running-basic-locally/blueprint/basic.yaml
```

Conversely, the following runs the `uninstall` workflow:

```bash
cfy uninstall
```