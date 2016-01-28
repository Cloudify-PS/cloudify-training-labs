# Lab 2: Running Basic Blueprint Locally

From within the VM containing the Cloudify CLI, create a directory to be used for Cloudify's local run:

```bash
mkdir ~/cfylocal && cd ~/cfylocal
```

Next, initialize a Cloudify environment, using the basic blueprint:

```bash
cfy local init -p ~/cloudify-training-labs/blueprints/basic/basic.yaml
```

## Invoke the `install` Workflow

```bash
cfy local execute -w install
```

The output should be similar to the following:

```
2016-01-25 07:05:28 CFY <local> Starting 'install' workflow execution
2016-01-25 07:05:28 CFY <local> [main_host_c76c6] Creating node
2016-01-25 07:05:28 CFY <local> [main_host_c76c6] Configuring node
2016-01-25 07:05:28 CFY <local> [main_host_c76c6] Starting node
2016-01-25 07:05:29 CFY <local> [test_application_server_f330f] Creating node
2016-01-25 07:05:30 CFY <local> [test_application_server_f330f] Configuring node
2016-01-25 07:05:30 CFY <local> [test_application_server_f330f] Starting node
2016-01-25 07:05:30 CFY <local> [test_application_server_f330f.start] Sending task 'script_runner.tasks.run'
2016-01-25 07:05:30 CFY <local> [test_application_server_f330f.start] Task started 'script_runner.tasks.run'
2016-01-25 07:05:30 LOG <local> [test_application_server_f330f.start] INFO: Executing: /tmp/tmptAF4ya-hello.sh
2016-01-25 07:05:30 LOG <local> [test_application_server_f330f.start] INFO: Hello!
2016-01-25 07:05:30 LOG <local> [test_application_server_f330f.start] INFO: Execution done (return_code=0): /tmp/tmptAF4ya-hello.sh
2016-01-25 07:05:30 CFY <local> [test_application_server_f330f.start] Task succeeded 'script_runner.tasks.run'
2016-01-25 07:05:31 CFY <local> 'install' workflow execution succeeded
```

## Invoke the `uninstall` Workflow

```bash
cfy local execute -w uninstall
```

The output should be similar to the following:

```
2016-01-25 07:05:50 CFY <local> Starting 'uninstall' workflow execution
2016-01-25 07:05:50 CFY <local> [test_application_server_f330f] Stopping node
2016-01-25 07:05:50 CFY <local> [test_application_server_f330f.stop] Sending task 'script_runner.tasks.run'
2016-01-25 07:05:50 CFY <local> [test_application_server_f330f.stop] Task started 'script_runner.tasks.run'
2016-01-25 07:05:50 LOG <local> [test_application_server_f330f.stop] INFO: Executing: /tmp/tmpmlFCf0-goodbye.sh
2016-01-25 07:05:51 LOG <local> [test_application_server_f330f.stop] INFO: Goodbye!
2016-01-25 07:05:51 LOG <local> [test_application_server_f330f.stop] INFO: Execution done (return_code=0): /tmp/tmpmlFCf0-goodbye.sh
2016-01-25 07:05:51 CFY <local> [test_application_server_f330f.stop] Task succeeded 'script_runner.tasks.run'
2016-01-25 07:05:51 CFY <local> [test_application_server_f330f] Deleting node
2016-01-25 07:05:51 CFY <local> [main_host_c76c6] Stopping node
2016-01-25 07:05:52 CFY <local> [main_host_c76c6] Deleting node
2016-01-25 07:05:52 CFY <local> 'uninstall' workflow execution succeeded
```
