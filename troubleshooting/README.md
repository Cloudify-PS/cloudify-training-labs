# Lab: Troubleshooting

In this lab, we will walk through a few troubleshooting scenarios.

## Failing tasks

This lab contains a blueprint ([failed-task/blueprint.yaml](failed-task/blueprint.yaml)) that runs a script that will
always fail. You will run it, and then practice inspecting the relevant logs.

The blueprint is structured so the failing script is being run twice: once on the manager, and once on an agent. For an
agent, we will pick one of the VM's we have in our disposal - say, the NodeJS VM.

### Preparation

```bash
export LAB_ROOT=~/cfy-training-labs/troubleshooting/failed-tasks
```

### Execute the blueprint

```bash
cfy blueprints create -b fail -p $LAB_ROOT/blueprint.yaml
cfy deployments create -b fail -d fail -i 'vm_ip=<nodejs-vm-private-ip>'
cfy executions start -d fail -w install -l
```

### Analysis

As the `install` workflow execution progresses, Cloudify will invoke the following operations concurrently:

* `manager_script:create`
* `agent_script:create`

As the operations are executed concurrently, the Cloudify log may contain log records from both operations intermingled.
Inspecting the output of the `install` execution, you should see lines similar to the following:

```
2017-02-23T13:54:43 CFY <test> [manager_script_q5fjwa] Creating node
2017-02-23T13:54:43 CFY <test> [manager_script_q5fjwa.create] Sending task 'script_runner.tasks.run'
2017-02-23T13:54:43 CFY <test> [manager_script_q5fjwa.create] Task started 'script_runner.tasks.run'
2017-02-23T13:54:43 LOG <test> [manager_script_q5fjwa.create] INFO: Downloaded scripts/fail.py to /tmp/MBZB3/fail.py
2017-02-23T13:54:44 CFY <test> [manager_script_q5fjwa.create] Task failed 'script_runner.tasks.run' -> integer division or modulo by zero
```

- describing the failure at the manager-side failure script, and the following:

```
2017-02-23T13:54:57 CFY <test> [agent_script_2burqg.create] Sending task 'script_runner.tasks.run'
2017-02-23T13:54:57 CFY <test> [agent_script_2burqg.create] Task started 'script_runner.tasks.run'
2017-02-23T13:54:58 LOG <test> [agent_script_2burqg.create] INFO: Downloaded scripts/fail.py to /tmp/WAFUW/fail.py
2017-02-23T13:54:58 CFY <test> [agent_script_2burqg.create] Task failed 'script_runner.tasks.run' -> integer division or modulo by zero
```

- describing the failure at the agent-side failure script.

#### Manager-side script

For manager-side operations, the main logs are located in `/var/log/cloudify/mgmtworker`:

```bash
cd /var/log/cloudify/mgmtworker/logs
ls -la
```

Each deployment has one log file, named `<deployment_id>.log` (the log file is routinely rotated by a `logrotate` policy).

Display it:

```bash
vi test.log
```

Scroll to the location in the log file that shows log lines around the time of failure. You should see something along
the lines of:

```
2017-02-23 13:54:43,875 [ERROR] Task script_runner.tasks.run[bb89133d-4112-4e41-ab37-f32a13a4ca24] raised:
Traceback (most recent call last):
  File "/tmp/pip-build-MXkfa5/cloudify-plugins-common/cloudify/dispatch.py", line 596, in main
  File "/tmp/pip-build-MXkfa5/cloudify-plugins-common/cloudify/dispatch.py", line 366, in handle
  File "/opt/mgmtworker/env/lib/python2.7/site-packages/script_runner/tasks.py", line 72, in run
    return process_execution(script_func, script_path, ctx, process)
  File "/opt/mgmtworker/env/lib/python2.7/site-packages/script_runner/tasks.py", line 143, in process_execution
    script_func(script_path, ctx, process)
  File "/opt/mgmtworker/env/lib/python2.7/site-packages/script_runner/tasks.py", line 275, in eval_script
    execfile(script_path, eval_globals)
  File "/tmp/MBZB3/fail.py", line 1, in <module>
    x = 3 / 0
ZeroDivisionError: integer division or modulo by zero
```
