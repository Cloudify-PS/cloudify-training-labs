# Lab: The Plugin Development Template

In this lab, we will develop a very simple plugin and use it within a blueprint.

The lab is designed so the developed plugin is embedded with the blueprint; however, note that, most typically, plugins are packaged and stored on a server, so they can be reused
by multiple blueprints.

## Prerequisites

To develop a plugin, please git clone this repository on your CLI VM and go to `developing-simple-plugin` directory:
```
git clone https://github.com/Cloudify-PS/cloudify-training-labs.git
cd cloudify-training-labs/developing-simple-plugin
```

## Step 1: Edit `setup.py`

```bash
cd plugin-template
vi setup.py
```

Edit the `setup.py` file for your needs. Fill in all the missing values beginning with `ENTER`. 

**NOTE**: the `install_requires` and `test_requires` keys: these ensure that proper dependencies are provided to the plugin during build and runtime.

## Step 2: Edit `tasks.py`

```bash
vi plugin/tasks.py
```

Modify the `my_task` function (you may rename it as well). Our goal is to write an operation that:

* Receives two arguments, `str1` and `str2`
* Prints the arguments to the Cloudify log
* Stores a concat of these two strings under a runtime property called `result` on the same node instance that the plugin operates on
* Prints the result to the Cloudify log

## Step 3: Edit `test_plugin.yaml`

```bash
vi plugin/tests/blueprint/plugin/test_plugin.yaml
```

This YAML file is intended to function as a `plugin.yaml` file for the plugin, when run through integration tests. Edit it as follows:

* `plugin_name` should be replaced with any name you desire. That would be the plugin's name as it is referred-to in blueprints.

## Step 4: Edit `blueprint.yaml`

```bash
vi plugin/tests/blueprint/blueprint.yaml
```

This YAML file is a standard blueprints file, against which the plugin test runs. Change it to accommodate your plugin. In particular, pay attention to the following:

* `inputs`: while not mandatory, define two inputs, one for `str1` and one for `str2`.
* `implementation`: make sure you compose the path to the Python operation correctly.
* `inputs` (under `node_templates`): these should correspond to your plugin's parameters.
* `outputs`: make sure you collect the correct runtime property

## Step 5: Edit `test_plugin.py`

```bash
vi plugin/tests/test_plugin.py
```

* Edit the `inputs` (in the `workflow_test` decorator) dictionary to include `str1` and `str2`.
* Add appropriate assertions in the `test_my_task` method.

## Step 6: Install plugin requirements

Before running the tester, you need to install its Python dependencies.
It is a good practice to install packages into a Python virtual environment, rather than to the system-level
libraries. Therefore, we will create a virtual environment and work from there:

```bash
python3 -m venv ~/dev-env
~/dev-env/bin/pip install -r dev-requirements.txt
```

## Step 8: Run the unit test

```bash
~/dev-env/bin/python -m unittest plugin.tests.test_plugin
```

You will see output similar to the following:

```
2017-01-29 01:38:13 CFY <test_my_task> Starting 'install' workflow execution
2017-01-29 01:38:13 CFY <test_my_task> [test_node_template_jjthv4] Creating node
2017-01-29 01:38:13 CFY <test_my_task> [test_node_template_jjthv4] Configuring node
2017-01-29 01:38:14 CFY <test_my_task> [test_node_template_jjthv4] Starting node
2017-01-29 01:38:14 CFY <test_my_task> [test_node_template_jjthv4.start] Sending task 'plugin.tasks.my_task'
2017-01-29 01:38:14 CFY <test_my_task> [test_node_template_jjthv4.start] Task started 'plugin.tasks.my_task'
2017-01-29 01:38:14 LOG <test_my_task> [test_node_template_jjthv4.start] INFO: str1=mark, str2=knopfler
2017-01-29 01:38:14 LOG <test_my_task> [test_node_template_jjthv4.start] INFO: result=markknopfler
2017-01-29 01:38:14 CFY <test_my_task> [test_node_template_jjthv4.start] Task succeeded 'plugin.tasks.my_task'
2017-01-29 01:38:14 CFY <test_my_task> 'install' workflow execution succeeded
.
----------------------------------------------------------------------
Ran 1 test in 2.092s

OK
```
