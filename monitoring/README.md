# Lab: Deploying Collectors and Using the Grafana Dashboard

The purpose of this lab is to add monitoring to an existing blueprint.

It is assumed that the `LAB_ROOT` environment variable points to the exercise's root directory. Otherwise, export it:

```bash
export LAB_ROOT=~/cloudify-training-labs/monitoring/exercise
```

### Step 1: Replace the placeholders

You need to replace all the occurrences of the placeholders (`REPLACE_WITH`) in `inputs.yaml` and in `blueprint/blueprint.yaml` to add monitoring to the blueprint.

You can use the Diamond collectors' reference for information how to configure collectors: https://github.com/python-diamond/Diamond/wiki/Collectors
 
### Step 2: Upload and install the blueprint

```bash
cd ~/mgr
cfy blueprints upload -p $LAB_ROOT/blueprint/blueprint.yaml -b monitoring
cfy deployments create -b monitoring -d mon -i $LAB_ROOT/inputs.yaml
cfy executions start -d mon -w install -l
```

### Step 3: Review monitoring in the UI

1. In the web UI, go to the Deployments screen.
2. Click your deployment.
3. Click the "Monitoring" tab.

Now you can see the Grafana dashboard, with a few default metrics defined. This dashboard is dynamically created for every deployment when you click the "Monitoring" tab.

### Step 4: Add a new graph to the dashboard

Now let's add a new graph to the dashboard:

1. Click the *Add a Row* button at the bottom right part of the screen. 
2. Click the left handle button, and then *Add panel* -> *Graph*.
3. Click the graph's title -> *Edit*.
4. Type `cpu` in the *Series* field. You should see a list of series names available in InfluxDB (these were pushed into InfluxDB by the CPU collector you installed in your blueprint). Choose one of them (`mon.host.host_xxxxxx.cpu_total_user` for example).
5. Go to the *General* tab and give a meaningful title to your graph. You can also change the `span` attribute to control the width of the graph you just created (`12` being 100% of the dashboard's width). Feel free to play around with the other tabs as well to define your graph.
6. You can also control other aspects of the dashboard, such as the resolution, auto-refresh rate, etc.
7. You can also export your dashboard to JSON by clicking *Save* -> *Export dashboard*.

### Step 5: Uninstall the application

```bash
cfy executions start -d mon -w uninstall -l
cfy deployments delete -d mon
cfy blueprints delete -b monitoring
```
