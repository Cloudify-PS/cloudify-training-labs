# Lab: Creating a Simple Blueprint

This lab accompanies the "Blueprints" section of the training. It is meant to be completed gradually, alongside the
presentation of the training slide deck.

## Preparations

Create a new directory:

```bash
mkdir ~/my_bp
cd ~/my_bp
```

Create a new file to contain the blueprint:

```bash
vi blueprint.yaml
```

## Create the blueprint
 
### TOSCA definitions version

Add the TOSCA definitions version directive at the top of the file:

```yaml
tosca_definitions_version: <add_version_here>
```

### Imports

* Add Cloudify's global `types.yaml` file using an `import` statement. The file's URL is: http://www.getcloudify.org/spec/cloudify/4.3.1/types.yaml
* Add an import statement to a file called `include/type-definitions.yaml`.

### Add node types

We will create our type definitions in a separate file located in `include/type-definitions.yaml` relative to the
main blueprint file's root. While this is not a requirement, typically, reusable definitions are placed in YAML files
external to the main blueprint, and included from there.

1.  Add a node type called `apache`:
    * Derived from `cloudify.nodes.Root`.
    * Containing a property called `port`, of type `integer`, with the default value of `80`.
    * Containing a property called `document_root`, of type `string`, with the default value of `/var/www/html`.
    * Implementing the `cloudify.interfaces.lifecycle` interface, and:
      * Mapping the `create` operation to `scripts/apache-install.sh`
      * Mapping the `configure` operation to `scripts/apache-configure.sh`
      * Mapping the `start` operation to `scripts/apache-start.sh`
      * Mapping the `stop` operation to `scripts/apache-stop.sh`
      * Mapping the `delete` operation to `scripts/apache-uninstall.sh`

2.  Add a node type called `static_web_app`:
    * Derived from `cloudify.nodes.Root`.
    * Containing the following properties:
        *   Name: `web_page`, type: `string` (no default value)
    * Implementing the `cloudify.interfaces.lifecycle` interface, and:
      * Mapping the `create` operation to `scripts/static-app-install.sh`
      * Mapping the `delete` operation to `scripts/static-app-uninstall.sh`

**VERY IMPORTANT**: the script located in `scripts/static-app-install.sh` defines a runtime property
called `target_dir` on the node instance for which the operation is running. You will need this information
later.

### Add node templates

**Back in `~/my_bp/blueprint.yaml`**, we will now create some node templates.

1.  Add a node template called `host`, of type `cloudify.nodes.Compute`.
    *   Add a property called `ip`, with the value being the IP address of your **App VM**.
    *   Add a property called `agent_config`, with the value being a dictionary containing the following:
    
        ```
        user: centos
        key: /etc/cloudify/cfy-training.pem
        ```
    
        For example:
        
        ```yaml
        host:
          <...>
          properties:
            ip: 192.178.0.10
            agent_config:
              user: centos
              key: /etc/cloudify/cfy-training.pem
        ```

2.  Add a node template called `web_server`, of type `apache`.
    *   Provide an override to the `port` property. The default is `80`, but we want port `8080` here.
3.  Add a node template called `my_app`, of type `static_web_app`.
    *   Provide the following property values:
        *   `web_page`: `resources/hello.html`

### Add relationship type

**Back in `~/my_bp/include/type-definitions.yaml`**, add a relationship type called `app_contained_in_apache`.

The relationship type should be derived from the built-in `cloudify.relationships.contained_in` type.

The relationship type will map the `establish` operation in the `cloudify.interfaces.relationship_lifecycle`
**source** interface, to `scripts/app-to-apache.sh`.

### Add relationship instances

**Back in `~/my_bp/blueprint.yaml`**:

*   To the `web_server` node:
    * Add a relationship where the target is the `host` node, and the type is the standard containment type.
*   To the `my_app` node:
    * Add a relationship where the target is the `web_server` node, and the type is `app_contained_in_apache`.

### Add blueprint inputs

(This should be done in `~/my_bp/blueprint.yaml`)

1.  Add a blueprint input for the Apache listening port. The input name should be `apache_listening_port`, the type should be `integer`, with no default.
2.  Change the `web_server` node so the value of the `port` property is taken from the `apache_listening_port` input.
3.  Add a blueprint input for the App VM's IP address. The input name should be `ip`, the type should be `string`, with no default.
4.  Change the `host` node so the value of the `ip` property is taken from the `ip` input.

### Add a property reference

Open `include/type-definitions.yaml`. For the `configure` operation in the `apache` node type, add an input called `port`,
of type `integer`. The default value for the input should be defined so the following happens: when the `configure`
operation is called, Cloudify retrieves the value of the `port` property for the same node instance that the
operation runs on.

### Edit relationship type

In a previous step, you created a relationship type called `app_contained_in_apache`. Edit the definition of the
`establish` operation there. The operation should now receive the following inputs:
*   `app_dir`: the default value should be an attribute reference, retrieving the value of the `target_dir`
    attribute from whoever is at the *source* end of the relationship.
*   `document_root`: the default value should be a property reference, retrieving the value of the `document_root`
    property from whoever is at the *target* end of the relationship.

### Add outputs

Edit the main blueprint file again (`blueprint.yaml`) and add an `outputs` section. The `outputs` section should contain
only one item called `installation_info`. Its value should be a dictionary containing two elements:

* `port`: the value should be a property reference, obtaining the value of the `port` property from `web_server`.
* `app_dir`: the value should be an attribute reference, obtaining the value of the `target_dir` attribute from `my_app`.

### Add supporting resources

Copy the contents of the `solution/scripts` directory into your blueprint's directory:

```bash
cp -R ~/cloudify-training-labs/blueprints/solution/scripts ~/my_bp
```

Now, copy the contens of the `solution/resources` directory into your blueprint's directory:

```bash
cp -R ~/cloudify-training-labs/blueprints/solution/resources ~/my_bp
```

## Run the blueprint

Now that the blueprint is ready, try running it:

```bash
cfy install ~/my_bp/blueprint.yaml -i apache_listening_port=8080 -i ip=<your-app-VM-IP> -b bp_test -d dep1
```

(Replace `<your-app-VM-IP>` with your App VM's IP address)

When installation is done, obtain the outputs:

```bash
cfy deployments outputs dep1
```

You should receive the value of the `outputs` section defined in the blueprint, with values calculated in
real time.

You should now be able to point your browser at `http://<app-vm-public-ip>:8080/app/hello.html` and get the static
app that had just been deployed.

Once done, invoke the `uninstall` workflow to clean up:

```bash
cfy uninstall dep1
```
