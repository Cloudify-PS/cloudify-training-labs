# Lab: Monitoring

The purpose of this lab is to add monitoring to an existing blueprint.

Ensure that the `LAB_ROOT` environment variable points to the exercise's root directory by executing:

```bash
export LAB_ROOT=~/cloudify-training-labs/monitoring/exercise
```

### Step 1: Replace the placeholders

You need to replace all the occurrences of the placeholders (`REPLACE_WITH`) in `inputs.yaml` and in `blueprint/blueprint.yaml` to add monitoring to the blueprint.

You can use the Diamond collectors' reference for information how to configure collectors: https://github.com/python-diamond/Diamond/wiki/Collectors
 
### Step 2: Upload and install the blueprint

**NOTE**: Replace `<app-vm-ip-address>` with the private IP address of your application VM.

```bash
cfy blueprints upload $LAB_ROOT/blueprint/blueprint.yaml -b monitoring
cfy deployments create mon -b monitoring -i vm_ip_address=<app-vm-ip-address>
cfy executions start -d mon install
```

### Step 3: Show metrics in the UI

1.  Log in to the UI.
2.  Go to the Deployments screen.
3.  Click your deployment.
4.  Click your username at the top right, and select "Edit Mode".
5.  Click the "Add Widget" button.
6.  Select the "Deployment metric graph" widget. Click "Add".
7.  Click the cogwheel icon at the top right corner of the new widget.
8.  Under "Node Filter":
    a. Select "Deployment" and then click your deployment's name.
    b. Select "Node Instance" and select your VM's instance ID.
9.  In the "Charts" table, focus on the first row and click the "Metric" dropdown list. Then select `cpu_total_user`.
10. In the "Label" field, type "CPU (Total)".
11. Click "Save".
12. Click your username at the top right, and select "Exit Edit Mode".
13. To see the CPU load changing, log into the app VM and execute some command that generates load. For example, you can use the `openssl speed` command.

The metrics widget will now appear on the screen.

### Step 5: Uninstall the application

```bash
cfy executions start -d mon uninstall
cfy deployments delete mon
cfy blueprints delete monitoring
```
