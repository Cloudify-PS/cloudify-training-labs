# Lab: Developing a Simple Plugin

In this lab, we will develop a very simple plugin and use it within a blueprint.

The lab is designed so the developed plugin is embedded with the blueprint; however, if you have access to a Git repository, you are encouraged to store the plugin there instead, and modify the plugin declaration accordingly.

**NOTE**: Although you can run this lab on any VM (as it does not require communicating with the Cloudify Manager), it is recommended that you run it on the
CLI VM, in order to keep all your work on the same machine. Also, your CLI VM already contains the Cloudify virtualenv, which is required for the completion of this lab. 

## Step 1: Download the plugin template

```bash
mkdir ~/work/plugin-lab && cd ~/work/plugin-lab
wget -O template.zip https://github.com/cloudify-cosmo/cloudify-plugin-template/archive/3.4rc1.zip
unzip template.zip
rm template.zip
mv cloudify-plugin-template-3.4rc1 test-plugin
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
* Prints the result

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

* Edit the `inputs` (in the `setUp` method) dictionary to include `str1` and `str2`.
* Add appropriate assertions in the `test_my_task` method.

## Step 7: Install plugin requirements

Before running the tester, you need to install its Python dependencies. You may either use your current virtualenv, or create another; for simplicity, we will use the same virtualenv
we use elsewhere. If that virtualenv is not currently active, then activate it.

Then:

```bash
cd test-plugin
pip install -r dev-requirements.txt
```

## Step 8: Run the unit test

```bash
python -m unittest plugin.tests.test_plugin
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