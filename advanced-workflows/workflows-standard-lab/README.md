# Standard Workflow lab

In this lab, we will be automating the launching of hot air balloons for a Boston-based hot air balloon ride company. Hot air balloon experts warn of a maximum safe wind speed of 8-10 MPH and we must keep people safe!

You’ve been provided a `ha_balloon` node that is scalable up to 5 (the amount of balloons the company has) with a minimum of 0 instances. If a node has been installed, that means it’s been cleared for use. If it’s uninstalled, that means that it has been told to land.

There’s a custom workflow called `check_wind_speed` that should check the wind speed from an external service (see code comments), make a scaling decision based on the reported wind speed, and execute a scaling operation (logging before and after as well as catching exceptions of the built-in `scale` workflow). How you scale based on wind speed is up to you.


## Usage

Since this lab folder includes both the blueprint as well as the needed plugin, there's no need to do separate operations to load the plugin.

```bash
# Upload the blueprint (and plugin) to a manager
cfy blueprints upload -b lab-std-wf -p exercise/blueprint.yaml

# Create a new deployment from the blueprint
cfy deployments create -d lab-std-wf-01 -b lab-std-wf

# Execute the custom workflow
cfy executions start -d lab-std-wf-01 -w check_wind_speed -l
```


## Lab tasks


### Task \#1

Run the custom workflow (see the `Usage` section above). Note, you'll need to complete Task \#2 before scaling will actually work.

### Task \#2

In the `check_wind_speed` workflow code, add the logic to calculate the scaling delta (amount and direction of scaling operation). See in-code comments about the task.

### Task \#3

Using only `cfy` (not modifying code), change the city where the wind speed data will come from and run the custom workflow.

### Task \#4

Add a new workflow parameter called `max_wind_speed` to override the max wind speed threshold. Then, use this custom parameter next time you execute the custom workflow to see a max wind speed to 100.

### Task \#5

Add 2 logging statements, 1 before scaling and 1 after that log the current number of scaling
group instances. *hint: look at the scaling group properties*
