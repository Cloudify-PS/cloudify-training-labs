# Lab: Running a Basic Blueprint Locally

In this lab, we will run a very basic blueprint using Cloudify.

## Add your IP address

Edit the file `~/cloudify-training-labs/running-basic-blueprint/blueprint/basic.yaml`,
and replace the string `REPLACE_WITH_IP_ADDRESS` with your **APP VM**'s IP address.
It doesn't matter which of the IP addresses (private / public) you use, as long as
the IP address is routable from within the Cloudify Manager (in the official Cloudify Training Course,
both IP addresses are routable).

## Upload the blueprint

```bash
cfy blueprints upload ~/cloudify-training-labs/running-basic-blueprint/blueprint/basic.yaml -b basic
```

Now the blueprint is available on the Cloudify Manager, with the ID `basic`.

## Create a deployment

```bash
cfy deployments create dep1 -b basic
```

This will create an "instance" of the blueprint called `basic`. The "instance"'s name is `dep1`.

## Run the `install` workflow

```bash
cfy executions start install -d dep1
```

The output should be similar to the following:

```
2018-03-04 14:30:00.451  CFY <basic> Starting 'install' workflow execution
2018-03-04 14:30:00.571  CFY <basic> [my_host_kgn2md] Creating node
2018-03-04 14:30:01.001  CFY <basic> [my_host_kgn2md] Configuring node
2018-03-04 14:30:01.409  CFY <basic> [my_host_kgn2md] Starting node
2018-03-04 14:30:02.405  CFY <basic> [my_application_l6mowd] Creating node
2018-03-04 14:30:02.465  CFY <basic> [my_application_l6mowd.create] Sending task 'script_runner.tasks.run'
2018-03-04 14:30:02.470  CFY <basic> [my_application_l6mowd.create] Task started 'script_runner.tasks.run'
2018-03-04 14:30:02.525  LOG <basic> [my_application_l6mowd.create] INFO: Executing: /tmp/NDRSZ/tmpda4XDQ-creating.sh, stdout: /tmp/cloudify/logs/tasks/052993e3-f7e4-4501-acf8-b7014626d0ed.out, stderr: /tmp/cloudify/logs/tasks/052993e3-f7e4-4501-acf8-b7014626d0ed.err
2018-03-04 14:30:02.529  LOG <basic> [my_application_l6mowd.create] INFO: Process created, PID: 9567
2018-03-04 14:30:02.804  LOG <basic> [my_application_l6mowd.create] INFO: Creating!
2018-03-04 14:30:02.847  LOG <basic> [my_application_l6mowd.create] INFO: Process 9567 ended
2018-03-04 14:30:02.905  LOG <basic> [my_application_l6mowd.create] INFO: Execution done (return_code=0): /tmp/NDRSZ/tmpda4XDQ-creating.sh
2018-03-04 14:30:02.905  CFY <basic> [my_application_l6mowd.create] Task succeeded 'script_runner.tasks.run'
2018-03-04 14:30:03.235  CFY <basic> [my_application_l6mowd] Configuring node
2018-03-04 14:30:03.293  CFY <basic> [my_application_l6mowd.configure] Sending task 'script_runner.tasks.run'
2018-03-04 14:30:03.299  CFY <basic> [my_application_l6mowd.configure] Task started 'script_runner.tasks.run'
2018-03-04 14:30:03.300  LOG <basic> [my_application_l6mowd.configure] INFO: Executing: /tmp/7PKZN/tmpfdnjV2-configuring.sh, stdout: /tmp/cloudify/logs/tasks/0b409dc6-a6d4-421e-ab31-29cc21cb55d4.out, stderr: /tmp/cloudify/logs/tasks/0b409dc6-a6d4-421e-ab31-29cc21cb55d4.err
2018-03-04 14:30:03.305  LOG <basic> [my_application_l6mowd.configure] INFO: Process created, PID: 9572
2018-03-04 14:30:03.579  LOG <basic> [my_application_l6mowd.configure] INFO: Configuring!
2018-03-04 14:30:03.623  LOG <basic> [my_application_l6mowd.configure] INFO: Process 9572 ended
2018-03-04 14:30:03.680  LOG <basic> [my_application_l6mowd.configure] INFO: Execution done (return_code=0): /tmp/7PKZN/tmpfdnjV2-configuring.sh
2018-03-04 14:30:03.681  CFY <basic> [my_application_l6mowd.configure] Task succeeded 'script_runner.tasks.run'
2018-03-04 14:30:04.028  CFY <basic> [my_application_l6mowd] Starting node
2018-03-04 14:30:04.114  CFY <basic> [my_application_l6mowd.start] Sending task 'script_runner.tasks.run'
2018-03-04 14:30:04.143  CFY <basic> [my_application_l6mowd.start] Task started 'script_runner.tasks.run'
2018-03-04 14:30:04.144  LOG <basic> [my_application_l6mowd.start] INFO: Executing: /tmp/1YPE0/tmpsq7hOp-starting.sh, stdout: /tmp/cloudify/logs/tasks/4728c4b2-327a-41c7-9cf8-a5126474ab75.out, stderr: /tmp/cloudify/logs/tasks/4728c4b2-327a-41c7-9cf8-a5126474ab75.err
2018-03-04 14:30:04.149  LOG <basic> [my_application_l6mowd.start] INFO: Process created, PID: 9577
2018-03-04 14:30:04.424  LOG <basic> [my_application_l6mowd.start] INFO: Starting!
2018-03-04 14:30:04.467  LOG <basic> [my_application_l6mowd.start] INFO: Process 9577 ended
2018-03-04 14:30:04.525  LOG <basic> [my_application_l6mowd.start] INFO: Execution done (return_code=0): /tmp/1YPE0/tmpsq7hOp-starting.sh
2018-03-04 14:30:04.525  CFY <basic> [my_application_l6mowd.start] Task succeeded 'script_runner.tasks.run'
2018-03-04 14:30:04.833  CFY <basic> 'install' workflow execution succeeded
```

## Invoke the `uninstall` workflow

```bash
cfy executions start uninstall -b basic
```

The output should be similar to the following:

```
2018-03-04 14:30:25.041  CFY <basic> Starting 'uninstall' workflow execution
2018-03-04 14:30:25.159  CFY <basic> [my_application_l6mowd] Stopping node
2018-03-04 14:30:25.346  CFY <basic> [my_application_l6mowd.stop] Sending task 'script_runner.tasks.run'
2018-03-04 14:30:25.374  CFY <basic> [my_application_l6mowd.stop] Task started 'script_runner.tasks.run'
2018-03-04 14:30:25.419  LOG <basic> [my_application_l6mowd.stop] INFO: Executing: /tmp/KCQG5/tmpP92y26-stopping.sh, stdout: /tmp/cloudify/logs/tasks/9ff31fb5-1507-4700-9a6e-4f9ede37845b.out, stderr: /tmp/cloudify/logs/tasks/9ff31fb5-1507-4700-9a6e-4f9ede37845b.err
2018-03-04 14:30:25.423  LOG <basic> [my_application_l6mowd.stop] INFO: Process created, PID: 9588
2018-03-04 14:30:25.697  LOG <basic> [my_application_l6mowd.stop] INFO: Stopping!
2018-03-04 14:30:25.740  LOG <basic> [my_application_l6mowd.stop] INFO: Process 9588 ended
2018-03-04 14:30:25.798  LOG <basic> [my_application_l6mowd.stop] INFO: Execution done (return_code=0): /tmp/KCQG5/tmpP92y26-stopping.sh
2018-03-04 14:30:25.798  CFY <basic> [my_application_l6mowd.stop] Task succeeded 'script_runner.tasks.run'
2018-03-04 14:30:26.292  CFY <basic> [my_application_l6mowd] Deleting node
2018-03-04 14:30:26.376  CFY <basic> [my_application_l6mowd.delete] Sending task 'script_runner.tasks.run'
2018-03-04 14:30:26.406  CFY <basic> [my_application_l6mowd.delete] Task started 'script_runner.tasks.run'
2018-03-04 14:30:26.408  LOG <basic> [my_application_l6mowd.delete] INFO: Executing: /tmp/6A7F0/tmpDjsMX4-deleting.sh, stdout: /tmp/cloudify/logs/tasks/051e8367-9e8d-45d3-9b39-8092bdb8fccf.out, stderr: /tmp/cloudify/logs/tasks/051e8367-9e8d-45d3-9b39-8092bdb8fccf.err
2018-03-04 14:30:26.412  LOG <basic> [my_application_l6mowd.delete] INFO: Process created, PID: 9593
2018-03-04 14:30:26.685  LOG <basic> [my_application_l6mowd.delete] INFO: Deleting!
2018-03-04 14:30:26.729  LOG <basic> [my_application_l6mowd.delete] INFO: Process 9593 ended
2018-03-04 14:30:26.786  LOG <basic> [my_application_l6mowd.delete] INFO: Execution done (return_code=0): /tmp/6A7F0/tmpDjsMX4-deleting.sh
2018-03-04 14:30:26.786  CFY <basic> [my_application_l6mowd.delete] Task succeeded 'script_runner.tasks.run'
2018-03-04 14:30:27.023  CFY <basic> [my_host_kgn2md] Stopping node
2018-03-04 14:30:27.817  CFY <basic> [my_host_kgn2md] Deleting node
2018-03-04 14:30:28.098  CFY <basic> 'uninstall' workflow execution succeeded
```

## Invoke it all at once

Since the sequence of initializing a blueprint and running the `install` workflow is very common,
there is a command that performs both at the same time:

```bash
cfy install ~/cloudify-training-labs/running-basic-locally/blueprint/basic.yaml -b basic
```

Conversely, the following runs the `uninstall` workflow:

```bash
cfy uninstall -b basic
```