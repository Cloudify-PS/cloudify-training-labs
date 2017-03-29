# Plugins lab

In this lab we will be using a custom plugin for the AWS API Gateway service. It should
create a new REST API, import a Swagger API definition, and publish the API for public access.

There is also a custom validation operation that will be used to confirm that API's health after
installation.

This lab requires Amazon Web Services (AWS) API access. Before attempting to run this lab, make sure you the following information on hand:

* AWS API access key ID
* AWS API secret access key
* AWS region name (ex. "us-east-1")


## Usage

Since this lab folder includes both the blueprint as well as the needed plugin, there's no need to do separate operations to load the plugin.

**Running on a Cloudify Manager**

```bash
# Upload the blueprint (and plugin) to a manager
cfy blueprints upload -b lab-plugins -p exercise/blueprint.yaml

# Create a new deployment from the blueprint
cfy deployments create -d lab-plugins-01 -b lab-plugins -i exercise/inputs.yaml

# Execute the install workflow
cfy executions start -d lab-plugins-01 -w install -l

# Execute the validation workflow
cfy executions start -d lab-plugins-01 -w execute_operation \
    -p "operation=cloudify.interfaces.validation.creation" -l
```

**Running locally** _(requires being in a VirtualEnv)_

```bash
# Uninstall any previously installed version of the plugin
# Windows users: If using Cygwin, use "winpty" before "pip".
pip uninstall -y cloudify-aws-api-gateway-plugin

# Install the local plugin into your VirtualEnv
pip install ./exercise/plugins/lab/

# Initialize the deployment
cfy local init --install-plugins \
	--blueprint-path exercise/blueprint.yaml \
    --inputs exercise/inputs.yaml

# Execute the install workflow
cfy local execute --debug \
    --task-retries 60 --task-retry-interval 15 \
    --workflow install

# Execute the validation workflow
cfy local execute --debug \
    --task-retries 60 --task-retry-interval 15 \
    --workflow execute_operation
    --parameters "operation=cloudify.interfaces.validation.creation"
```


## Lab tasks


### Task \#1

Check the plugin source using both *pylint* and *flake8* and correct any issues found.

When running PyLint, use the following command for this lab - `pylint --reports=n --disable=I ./exercise/plugins/lab/api_gateway/` which will
disable the verbose "reports" feature (you can enable it if you want, but it's usually more burden than
help) and also ignore purely information messages.

For Flake8 -

### Task \#2

Run the *install* workflow using the included blueprint and your own inputs.

### Task \#3

Once the *install* workflow succeeds, display the outputs and make sure you can reach the
URL indicated by the *endpoint* output. This should display a JSON object with the status
of the newly deployed API.

### Task \#4

Execute the `cloudify.interfaces.validation.creation` operation on the deployment. This should
pass successfully using default inputs.
