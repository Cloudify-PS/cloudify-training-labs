# Lab: Creating a Simple Blueprint

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

Add Cloudify's global `types.yaml` file using an `import` statement. The file's URL is: http://www.getcloudify.org/spec/cloudify/3.4.1/types.yaml

### Add node types

1.  Add a node type called `apache`:
    * Derived from `cloudify.nodes.Root`.
    * Containing a property called `listener_port`, of type `integer`, with the default value of `80`.
    * Implementing the `cloudify.interfaces.lifecycle` interface, and:
      * Mapping the `create` operation to `scripts/apache-install.sh`
      * Mapping the `delete` operation to `scripts/apache-uninstall.sh`

2.  Add a node type called `mysql`:
    * Derived from `cloudify.nodes.Root`.
    * Implementing the `cloudify.interfaces.lifecycle` interface, and:
      * Mapping the `create` operation to `scripts/mysql-install.sh`
      * Mapping the `delete` operation to `scripts/mysql-uninstall.sh`

### Add node templates

1.  Add a node template called `host`, of type `cloudify.nodes.Compute`.
    *   Add a property called `agent_config`, with the value being a dictionary containing the following:
    
        `install_method: none`
2.  Add a node template called `web_server`, of type `apache`.
    *   Provide an override to the `listener_port` property. The default is `80`, but we want port `8080` here.
3.  Add a node template called `database`, of type `mysql`.

### Add relationship type

Add a relationship type called `apache_connected_to_mysql`.

The relationship type should be derived from the built-in `cloudify.relationships.connected_to` type.

The relationship type will map the `establish` operation in the `cloudify.interfaces.relationship_lifecycle`
**source** interface, to `scripts/apache-to-mysql.sh`.

### Add relationship instances

*   To the `apache` node:
    * Add a relationship where the target is the `database` node, and the type is the relationship type you had created before.
    * Add a relationship where the target is the `host` node, and the type is the standard containment type.
*   To the `database` node:
    * Add a relationship where the target is the `host` node, and the type is the standard containment type.

### Add inputs

1.  Add an input for the Apache listening port. The input name should be `apache_listening_port`, the type should be `integer`, with no default.
2.  Change the `apache` node so the value of the `listener_port` property is taken from the `apache_listening_port` input.

## Run the blueprint

Now that the blueprint is ready, try running it:

```bash
cd ~/cfylocal
cfy local install -p ~/my_bp/blueprint.yaml -i 'apache_listening_port=8080'
```

Once done, invoke the `uninstall` workflow to clean up:

```bash
cfy local uninstall
```
