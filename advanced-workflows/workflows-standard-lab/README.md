# Standard Workflow lab

In this lab we will be getting the weather for a US city. This lab solely focuses on custom workflow development and has no functional node_templates defined.

There’s a custom workflow called `check_wind_speed` that should check the wind speed from an external weather service (API) and log the results.


## Usage

Since this lab folder includes both the blueprint as well as the needed plugin, there's no need to do separate operations to load the plugin.

**Running on a Cloudify Manager**

```bash
# Upload the blueprint (and plugin) to a manager
cfy blueprints upload -b lab-std-wf -p exercise/blueprint.yaml

# Create a new deployment from the blueprint
cfy deployments create -d lab-std-wf-01 -b lab-std-wf

# Execute the custom workflow
cfy executions start -d lab-std-wf-01 -w check_wind_speed -l
```

**Running locally** _(requires being in a VirtualEnv)_

```bash
# Uninstall any previously installed version of the plugin
# Windows users: If using Cygwin, use "winpty" before "pip".
pip uninstall -y lab-wf-standard-plugin

# Install the local plugin into your VirtualEnv
pip install ./exercise/plugins/lab/

# Initialize the deployment and execute the custom workflow
cfy local install --install-plugins --debug \
	--blueprint-path exercise/blueprint.yaml \
    --inputs exercise/inputs.yaml \
    --task-retries 60 --task-retry-interval 15 \
    --workflow refresh_snapshots
```


## Lab tasks


### Task \#1

Run the custom workflow (see the `Usage` section above) and make sure it's working.

### Task \#2

Add a new workflow parameter called `city_name` to override the workflow's city name (which is currently statically set to "Boston, MA"). Remove the the default value for `city_name` from
the workflow method arguments (read the comments!).

### Task \#3

Using only `cfy` (not modifying code), change the city where the wind speed data will come from and run the custom workflow. You must complete task #\2 to complete this task.

### Task \#4

Rename the folder at `<labroot>/exercise/plugins/lab` to `<labroot>/exercise/plugins/custom` and fix any newly broken references. *hint: check plugin.yaml*

Delete your existing deployment & blueprint and re-run everything to make sure it works.
