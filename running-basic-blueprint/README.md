# Lab: Running a Basic Blueprint

In this lab, we will run a very basic blueprint using Cloudify.

**NOTE**: This lab should be run on your **CLI VM**.

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
2018-04-09 07:40:11.731  CFY <dep1> Starting 'install' workflow execution
2018-04-09 07:40:12.793  CFY <dep1> [my_host_0ifzts] Creating node
2018-04-09 07:40:12.793  CFY <dep1> [my_host_0ifzts] Configuring node
2018-04-09 07:40:13.797  CFY <dep1> [my_host_0ifzts] Starting node
2018-04-09 07:40:13.797  CFY <dep1> [my_host_0ifzts] Creating Agent
2018-04-09 07:40:13.797  CFY <dep1> [my_host_0ifzts.create] Sending task 'cloudify_agent.installer.operations.create'
2018-04-09 07:40:13.797  CFY <dep1> [my_host_0ifzts.create] Task started 'cloudify_agent.installer.operations.create'
2018-04-09 07:40:15.751  LOG <dep1> [my_host_0ifzts.create] INFO: Creating Agent my_host_0ifzts
2018-04-09 07:40:22.344  LOG <dep1> [my_host_0ifzts.create] INFO: % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
2018-04-09 07:40:22.760  LOG <dep1> [my_host_0ifzts.create] INFO: 
2018-04-09 07:40:22.760  LOG <dep1> [my_host_0ifzts.create] INFO:                                  Dload  Upload   Total   Spent    Left  Speed
2018-04-09 07:40:22.760  LOG <dep1> [my_host_0ifzts.create] INFO:   0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
2018-04-09 07:40:22.760  LOG <dep1> [my_host_0ifzts.create] INFO: Successfully corrected cfy-agent`s virtualenv
2018-04-09 07:40:22.760  LOG <dep1> [my_host_0ifzts.create] INFO: 100 16.0M  100 16.0M    0     0  58.2M      0 --:--:-- --:--:-- --:--:-- 58.5M
2018-04-09 07:40:22.760  LOG <dep1> [my_host_0ifzts.create] INFO: Auto-correcting virtualenv /home/centos/my_host_0ifzts/env
2018-04-09 07:40:22.760  LOG <dep1> [my_host_0ifzts.create] INFO: Disabling requiretty directive in sudoers file
2018-04-09 07:40:22.760  LOG <dep1> [my_host_0ifzts.create] INFO: Successfully disabled requiretty for cfy-agent
2018-04-09 07:40:22.760  LOG <dep1> [my_host_0ifzts.create] INFO: No custom env configured
2018-04-09 07:40:22.760  LOG <dep1> [my_host_0ifzts.create] INFO: Creating...
2018-04-09 07:40:22.760  LOG <dep1> [my_host_0ifzts.create] INFO: Successfully created daemon: my_host_0ifzts
2018-04-09 07:40:22.760  LOG <dep1> [my_host_0ifzts.create] INFO: Configuring...
2018-04-09 07:40:22.760  LOG <dep1> [my_host_0ifzts.create] INFO: Starting daemon with command: sudo service celeryd-my_host_0ifzts start
2018-04-09 07:40:22.760  LOG <dep1> [my_host_0ifzts.create] INFO: Deploying celery configuration.
2018-04-09 07:40:22.760  LOG <dep1> [my_host_0ifzts.create] INFO: Creating start-on-boot entry
2018-04-09 07:40:22.760  LOG <dep1> [my_host_0ifzts.create] INFO: Command 'which dpkg' executed with an error.
2018-04-09 07:40:22.760  LOG <dep1> [my_host_0ifzts.create] INFO: code: 1
2018-04-09 07:40:22.760  LOG <dep1> [my_host_0ifzts.create] INFO: error: which: no dpkg in (/home/centos/my_host_0ifzts/env/bin:/home/centos/my_host_0ifzts/env/bin:/home/centos/my_host_0ifzts/env/bin:/sbin:/bin:/usr/sbin:/usr/bin)
2018-04-09 07:40:22.760  LOG <dep1> [my_host_0ifzts.create] INFO: Successfully started daemon: my_host_0ifzts
2018-04-09 07:40:22.760  LOG <dep1> [my_host_0ifzts.create] INFO: output: None
2018-04-09 07:40:22.760  LOG <dep1> [my_host_0ifzts.create] INFO: Successfully configured daemon: my_host_0ifzts
2018-04-09 07:40:22.760  LOG <dep1> [my_host_0ifzts.create] INFO: Starting...
2018-04-09 07:40:22.760  LOG <dep1> [my_host_0ifzts.create] INFO: Agent created, configured and started successfully
2018-04-09 07:40:22.661  CFY <dep1> [my_host_0ifzts.create] Task succeeded 'cloudify_agent.installer.operations.create'
2018-04-09 07:40:23.802  CFY <dep1> [my_application_rh7xe2] Creating node
2018-04-09 07:40:23.802  CFY <dep1> [my_application_rh7xe2.create] Sending task 'script_runner.tasks.run'
2018-04-09 07:40:23.802  CFY <dep1> [my_application_rh7xe2.create] Task started 'script_runner.tasks.run'
2018-04-09 07:40:24.766  LOG <dep1> [my_application_rh7xe2.create] INFO: Executing: /tmp/3ZIKL/tmpIVN2r2-creating.sh, stdout: /home/centos/my_host_0ifzts/work/logs/tasks/86599a14-e79c-4859-beae-f8086711c4ff.out, stderr: /home/centos/my_host_0ifzts/work/logs/tasks/86599a14-e79c-4859-beae-f8086711c4ff.err
2018-04-09 07:40:24.092  LOG <dep1> [my_application_rh7xe2.create] INFO: Downloaded scripts/creating.sh to /tmp/3ZIKL/tmpIVN2r2-creating.sh
2018-04-09 07:40:24.766  LOG <dep1> [my_application_rh7xe2.create] INFO: Process created, PID: 16545
2018-04-09 07:40:24.766  LOG <dep1> [my_application_rh7xe2.create] INFO: Creating!
2018-04-09 07:40:24.766  LOG <dep1> [my_application_rh7xe2.create] INFO: Process 16545 ended
2018-04-09 07:40:24.766  LOG <dep1> [my_application_rh7xe2.create] INFO: Execution done (return_code=0): /tmp/3ZIKL/tmpIVN2r2-creating.sh
2018-04-09 07:40:24.804  CFY <dep1> [my_application_rh7xe2.create] Task succeeded 'script_runner.tasks.run'
2018-04-09 07:40:25.807  CFY <dep1> [my_application_rh7xe2] Configuring node
2018-04-09 07:40:25.807  CFY <dep1> [my_application_rh7xe2.configure] Sending task 'script_runner.tasks.run'
2018-04-09 07:40:25.807  CFY <dep1> [my_application_rh7xe2.configure] Task started 'script_runner.tasks.run'
2018-04-09 07:40:25.769  LOG <dep1> [my_application_rh7xe2.configure] INFO: Downloaded scripts/configuring.sh to /tmp/505MG/tmpIhxJdB-configuring.sh
2018-04-09 07:40:25.769  LOG <dep1> [my_application_rh7xe2.configure] INFO: Executing: /tmp/505MG/tmpIhxJdB-configuring.sh, stdout: /home/centos/my_host_0ifzts/work/logs/tasks/ef9bee55-371c-4609-85d0-996b7e3bf6de.out, stderr: /home/centos/my_host_0ifzts/work/logs/tasks/ef9bee55-371c-4609-85d0-996b7e3bf6de.err
2018-04-09 07:40:25.769  LOG <dep1> [my_application_rh7xe2.configure] INFO: Process created, PID: 16564
2018-04-09 07:40:26.772  LOG <dep1> [my_application_rh7xe2.configure] INFO: Configuring!
2018-04-09 07:40:26.772  LOG <dep1> [my_application_rh7xe2.configure] INFO: Process 16564 ended
2018-04-09 07:40:26.772  LOG <dep1> [my_application_rh7xe2.configure] INFO: Execution done (return_code=0): /tmp/505MG/tmpIhxJdB-configuring.sh
2018-04-09 07:40:26.811  CFY <dep1> [my_application_rh7xe2.configure] Task succeeded 'script_runner.tasks.run'
2018-04-09 07:40:26.811  CFY <dep1> [my_application_rh7xe2] Starting node
2018-04-09 07:40:26.811  CFY <dep1> [my_application_rh7xe2.start] Sending task 'script_runner.tasks.run'
2018-04-09 07:40:26.811  CFY <dep1> [my_application_rh7xe2.start] Task started 'script_runner.tasks.run'
2018-04-09 07:40:27.777  LOG <dep1> [my_application_rh7xe2.start] INFO: Executing: /tmp/IA8Y2/tmp4YBopR-starting.sh, stdout: /home/centos/my_host_0ifzts/work/logs/tasks/f089d03a-2ef4-42de-a98a-5fe2f6429c19.out, stderr: /home/centos/my_host_0ifzts/work/logs/tasks/f089d03a-2ef4-42de-a98a-5fe2f6429c19.err
2018-04-09 07:40:27.777  LOG <dep1> [my_application_rh7xe2.start] INFO: Downloaded scripts/starting.sh to /tmp/IA8Y2/tmp4YBopR-starting.sh
2018-04-09 07:40:27.777  LOG <dep1> [my_application_rh7xe2.start] INFO: Process created, PID: 16583
2018-04-09 07:40:27.777  LOG <dep1> [my_application_rh7xe2.start] INFO: Starting!
2018-04-09 07:40:27.777  LOG <dep1> [my_application_rh7xe2.start] INFO: Process 16583 ended
2018-04-09 07:40:27.777  LOG <dep1> [my_application_rh7xe2.start] INFO: Execution done (return_code=0): /tmp/IA8Y2/tmp4YBopR-starting.sh
2018-04-09 07:40:27.814  CFY <dep1> [my_application_rh7xe2.start] Task succeeded 'script_runner.tasks.run'
2018-04-09 07:40:28.816  CFY <dep1> 'install' workflow execution succeeded
Finished executing workflow install on deployment dep1
* Run 'cfy events list -e a7e82934-24f4-4a4a-b43e-e26f06b3c6b4' to retrieve the execution's events/logs
```

## Run the `uninstall` workflow

To uninstall the application, execute the `uninstall` workflow:

```bash
cfy executions start uninstall -d dep1
```

## Delete the deployment

Once the application is uninstalled, you may delete the deployment:

```bash
cfy deployments delete dep1
```

## Delete the blueprint

Once no deployments exist for a given blueprint, you may delete the blueprint:

```bash
cfy blueprints delete basic
```

## Invoke it all at once

Since the sequence of uploading a blueprint, creating a deployment and running the `install` workflow is very common,
there is a command that performs all at once:

```bash
cfy install ~/cloudify-training-labs/running-basic-blueprint/blueprint/basic.yaml -b basic -d dep1
```

Conversely, the following runs the `uninstall` workflow, deletes the deployment with the provided ID, and - if
no deployments are left of the associated blueprint - deletes the associated blueprint as well:

```bash
cfy uninstall dep1
```
