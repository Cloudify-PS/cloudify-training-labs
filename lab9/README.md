# Lab 9: Deploying Collectors and Using the Grafana Dashboard

The purpose of this lab is to add monitoring to the Tomcat blueprint used in lab 4.

It is assumed that the lab's files are extracted into `$LAB_ROOT`.

### Step 1: Replace the placeholders

You need to replace all the occurrences of the placeholders (`REPLACE_WITH`) in `tomcat.yaml` and in the blueprint file to add monitoring to the blueprint.

### Step 2: Upload and install the blueprint

```bash
cfy blueprints upload -p $LAB_ROOT/hello-tomcat/tomcat-blueprint.yaml -b hellotomcat-mon
cfy deployments create -b hellotomcat-mon -d hellotomcat-mon -i $LAB_ROOT/hello-tomcat/tomcat.yaml
cfy executions start -d hellotomcat-mon -w install
```

### Step 3: Review monitoring in the UI

1. In the web UI, go to the deployment screen.
2. Click your deployment.
3. Click the "Monitoring" tab.

Now you can see the Grafana dashboard, with a few default metrics defined. This dashboard is dynamically created for every deployment when you click the "Monitoring" tab.

### Step 4: Add a new graph to the dashboard

Now let's add a new graph to the dashboard:

1. Click the add a row button at the bottom right part of the screen 
2. Click the right handle button, and then *Add panel* -> *Graph*
3. Click the graph's title -> Edit
4. Type `cpu` in the *Series* field. You should see a list of series names available in influx (these were pushed into influx by the CPU collector you installed in your blueprint). Choose one of them.
5. Go to the *General* tab and give a meaningful title to your graph. You can also change the `span` attribute to control the width of the graph you just created (`12` being 100% of the dashboard's width). Feel free to play around with the other tabs as well to define your graph.
6. You can also control other aspects of the dashboard, such as the resolution, auto-refresh rate, etc.
7. You can also export your dashboard to JSON by clicking *Save* -> *Export dashboard*.