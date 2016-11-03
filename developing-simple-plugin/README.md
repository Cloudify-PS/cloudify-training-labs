# Lab: Developing a Simple Plugin

In this lab, we will develop a very simple plugin and use it within a blueprint.

The lab is designed so the developed plugin is embedded with the blueprint; however, note that, most typically, plugins are packaged and stored on a server, so they can be reused
by multiple blueprints.

## Step 1: Download the plugin template

```bash
mkdir -p ~/work/plugin-lab && cd ~/work/plugin-lab
curl -L -o template.zip https://github.com/cloudify-cosmo/cloudify-plugin-template/archive/3.4.zip
unzip template.zip
rm template.zip
mv cloudify-plugin-template-3.4 test-plugin
```

That will download `cloudify-plugin-template`, extract it and rename the resulting directory.

## Step 2: Edit `setup.py`

```bash
vi test-plugin/setup.py
```

Edit the `setup.py` file for your needs. In particular, note the `install_requires` and `test_requires` keys: these ensure that proper dependencies are provided to the plugin during build and runtime.

## Step 3: Edit `tasks.py`

```bash
vi test-plugin/plugin/tasks.py
```

Modify the `my_task` method (you may rename it as well). Our goal is to write an operation that:

* Receives two arguments, `str1` and `str2`
* Prints the arguments
* Stores a concat of these two strings under a runtime property called `result` on the same node instance that the plugin operates on
* Prints the result to the Cloudify log

## Step 4: Edit `test_plugin.yaml`

```bash
vi test-plugin/plugin/tests/blueprint/test_plugin.yaml
```

This YAML file is intended to function as a `plugin.yaml` file for the plugin, when run through integration tests. Edit it as follows:

* `plugin_name` should be replaced with any name you desire. That would be the plugin's name as it is referred-to in blueprints.

## Step 5: Edit `blueprint.yaml`

```bash
vi test-plugin/plugin/tests/blueprint/blueprint.yaml
```

This YAML file is a standard blueprints file, against which the plugin test runs. Change it to accommodate your plugin. In particular, pay attention to the following:

* `inputs`: while not mandatory, define two inputs, one for `str1` and one for `str2`.
* `implementation`: make sure you compose the path to the Python operation correctly.
* `inputs` (under `node_templates`): these should correspond to your plugin's parameters.
* `outputs`: make sure you collect the correct runtime property

## Step 6: Edit `test_plugin.py`

```bash
vi test-plugin/plugin/tests/test_plugin.py
```

* Edit the `inputs` (in the `workflow_test` decorator) dictionary to include `str1` and `str2`.
* Add appropriate assertions in the `test_my_task` method.

## Step 7: Install plugin requirements

Before running the tester, you need to install its Python dependencies.
It is a good practice to install packages into a Python virtual environment, rather than to the system-level
libraries. Therefore, we will create a virtual environment and work from there:

```bash
virtualenv ~/dev-env
cd test-plugin
~/dev-env/bin/pip install -r dev-requirements.txt
```

## Step 8: Run the unit test

```bash
~/dev-env/bin/python -m unittest plugin.tests.test_plugin
```

You will see output similar to the following:

```
2015-07-29 13:14:08 CFY <test_my_task> Starting 'install' workflow execution
2015-07-29 13:14:08 CFY <test_my_task> [test_node_template_eeade] Creating node
2015-07-29 13:14:09 CFY <test_my_task> [test_node_template_eeade] Configuring node
2015-07-29 13:14:09 CFY <test_my_task> [test_node_template_eeade] Starting node
2015-07-29 13:14:09 CFY <test_my_task> [test_node_template_eeade.start] Sending task 'plugin.tasks.my_task'
2015-07-29 13:14:09 CFY <test_my_task> [test_node_template_eeade.start] Task started 'plugin.tasks.my_task'
2015-07-29 13:14:09 CFY <test_my_task> [test_node_template_eeade.start] Task succeeded 'plugin.tasks.my_task'
2015-07-29 13:14:09 CFY <test_my_task> 'install' workflow execution succeeded
```
