# Lab 2: Running Basic Blueprint Locally

From within the VM containing the Cloudify CLI, create a directory to be used for Cloudify's local run:

```bash
mkdir ~/cfylocal && cd ~/cfylocal
```

Next, initialize a Cloudify environment, using the `basic` blueprint:

```bash
cfy local init -p ~/cloudify-training-labs/blueprints/basic/basic.yaml
```

## Invoke the `install` Workflow

```bash
cfy local execute -w install
```

The output should be similar to the following:

```
2015-06-11 01:42:16 CFY <local> Starting 'install' workflow execution
2015-06-11 01:42:16 CFY <local> [host_67871] Creating node
2015-06-11 01:42:16 CFY <local> [host_67871] Configuring node
2015-06-11 01:42:17 CFY <local> [host_67871] Starting node
2015-06-11 01:42:17 CFY <local> [node1_ca32f] Creating node
2015-06-11 01:42:18 CFY <local> [node1_ca32f] Configuring node
2015-06-11 01:42:18 CFY <local> [node1_ca32f] Starting node
2015-06-11 01:42:18 CFY <local> [node1_ca32f.start] Sending task 'script_runner.tasks.run'
2015-06-11 01:42:18 CFY <local> [node1_ca32f.start] Task started 'script_runner.tasks.run'
2015-06-11 01:42:18 LOG <local> [node1_ca32f.start] INFO: Executing: /tmp/tmpwdE5ut-hello.sh
2015-06-11 01:42:19 LOG <local> [node1_ca32f.start] INFO: Hello!
2015-06-11 01:42:19 LOG <local> [node1_ca32f.start] INFO: Execution done (return_code=0): /tmp/tmpwdE5ut-hello.sh
2015-06-11 01:42:19 CFY <local> [node1_ca32f.start] Task succeeded 'script_runner.tasks.run'
2015-06-11 01:42:19 CFY <local> 'install' workflow execution succeeded
```

## Invoke the `uninstall` Workflow

```bash
cfy local execute -w uninstall
```

The output should be similar to the following:

```
2015-06-11 02:58:55 CFY <local> Starting 'uninstall' workflow execution
2015-06-11 02:58:55 CFY <local> [node1_ca32f] Stopping node
2015-06-11 02:58:55 CFY <local> [node1_ca32f.stop] Sending task 'script_runner.tasks.run'
2015-06-11 02:58:55 CFY <local> [node1_ca32f.stop] Task started 'script_runner.tasks.run'
2015-06-11 02:58:55 LOG <local> [node1_ca32f.stop] INFO: Executing: /tmp/tmpa9PcDp-goodbye.sh
2015-06-11 02:58:55 LOG <local> [node1_ca32f.stop] INFO: Goodbye!
2015-06-11 02:58:55 LOG <local> [node1_ca32f.stop] INFO: Execution done (return_code=0): /tmp/tmpa9PcDp-goodbye.sh
2015-06-11 02:58:55 CFY <local> [node1_ca32f.stop] Task succeeded 'script_runner.tasks.run'
2015-06-11 02:58:56 CFY <local> [node1_ca32f] Deleting node
2015-06-11 02:58:56 CFY <local> [host_67871] Stopping node
2015-06-11 02:58:57 CFY <local> [host_67871] Deleting node
2015-06-11 02:58:57 CFY <local> 'uninstall' workflow execution succeeded
```