# Lab: Creating OpenStack Resources

In this lab, we will write a blueprint that creates resources on OpenStack. We will create:

* A virtual machine
* A security group
* A network
* A subnet
* A router

Also, we will connect all resources together.

For the preparation of this lab, you will have to use the official OpenStack plugin documentation, located at: http://docs.getcloudify.org/4.3.0/plugins/openstack/

## Step 1: Create blueprint's skeleton

```yaml
tosca_definitions_version: cloudify_dsl_1_3

imports:
  - http://www.getcloudify.org/spec/cloudify/4.3/types.yaml
  - http://www.getcloudify.org/spec/openstack-plugin/2.6.0/plugin.yaml
```

This will import the standard Cloudify types, as well as the OpenStack plugin.

## Step 2: Add OpenStack endpoint inputs

To be able to talk to OpenStack, and avoid hard-coding endpoint information in the blueprint, add the following inputs
to the blueprint:

* `keystone_username`
* `keystone_password`
* `keystone_tenant_name`
* `keystone_url`
* `region`

All inputs should be of type `string`.

## Step 3: Add OpenStack endpoint DSL definition

(Reference: http://docs.getcloudify.org/4.3/blueprints/spec-dsl-definitions/)

Add a DSL definition called `openstack_configuration`. The value should be a dictionary with the following keys:

* `username`: maps to the value of the `keystone_username` input
* `password`: maps to the value of the `keystone_password` input
* `tenant_name`: maps to the value of the `keystone_tenant_name` input
* `auth_url`: maps to the value of the `keystone_url` input
* `region`: maps to the value of the `region` input

## Step 4: Add OpenStack node templates

**NOTE**: each and every OpenStack node type supports a property called `openstack_config`. You should provide that
property, giving it the value of the expansion of the `openstack_configuration` DSL definition. For example:

```yaml
node_templates:
  my_node:
    type: cloudify.openstack.nodes.Server
    properties:
      openstack_config: *openstack_configuration
```

### Add the external network

Documentation: http://docs.getcloudify.org/4.3/plugins/openstack/#cloudify-openstack-nodes-network

Notes:

*   You're not expected to create the external network; you should use the existing one that most likely already exists
    in your OpenStack installation. Therefore, use the `use_external_resource` property accordingly.
*   To identify the existing resource's name, use the `resource_id` property. The value of the property should be taken
    from an input, to avoid hard-coding resource names. You'll need to add an input for that (for example,
    `external_network_name`).

### Add a router

Documentation: http://docs.getcloudify.org/4.3/plugins/openstack/#cloudify-openstack-nodes-router

*   The router needs to be connected to the external network. To achieve that, establish a `cloudify.relationships.connected_to`
    relationship between the router and the external network node.
*   To avoid hard-coding a router name, provide it as an input.

### Add a network

Documentation: http://docs.getcloudify.org/4.3/plugins/openstack/#cloudify-openstack-nodes-network

*   Don't forget to provide the new network's name through the `resource_id` property.
*   Avoid hard-coding a network name; use an input instead.

### Add a subnet

Documentation: http://docs.getcloudify.org/4.3/plugins/openstack/#cloudify-openstack-nodes-subnet

*   The subnet needs to be contained within the network that you had created. To achieve that, create a
    `cloudify.relationships.contained_in` relationship between the subnet and the network.
*   The subnet needs to have a "leg" in the router. To achieve that: http://docs.getcloudify.org/4.1/plugins/openstack/#cloudify-openstack-subnet-connected-to-router
*   Parameters for the subnet should be passed as entries in a dictionary property called `subnet`, as follows:

    ```yaml
    properties:
      subnet:
        cidr: a.b.c.d/e
    ```
    
    You may come up with any CIDR you'd like. Again, to avoid hard-coding, use an input.

###  Add a security group

Documentation: http://docs.getcloudify.org/4.3/plugins/openstack/#cloudify-openstack-nodes-securitygroup

We need only one rule: allow ingress traffic on port 22, from anywhere.

### Add a keypair

Documentation: http://docs.getcloudify.org/4.3/plugins/openstack/#cloudify-openstack-nodes-keypair

We want to create a new keypair. Therefore, make sure to set the `private_key_path` property to a proper path to receive
the generated private key.

### Add a virtual machine

Documentation: http://docs.getcloudify.org/4.3/plugins/openstack/#cloudify-openstack-nodes-server

Notes:

*   The server has to be based on a CentOS 7.0 image. You will need to get the ID of an image on your OpenStack installation,
    which represents a CentOS 7.0 image. To do that, you can use any OpenStack API (or Horizon).
    
    Using the OpenStack REST API:
    
    (GET) `<glance-endpoint-url>/v2/images`
    
    Or using the Python OpenStack client:
    
    ```bash
    glance image-list
    ```
    
    (`glance` is provided by the `python-glanceclient` package. To install it: `pip install python-glanceclient`)
*   You can use any flavour. Since Horizon doesn't provide the functionality of viewing flavour ID's unless you're an administrator,
    you should use the OpenStack API for that:
    
    (GET) `<nova-endpoint-url>/flavors`
    
    Or, with Python:
    
    ```bash
    nova flavor-list
    ```
*   The server needs to be connected to the security group. To achieve that: http://docs.getcloudify.org/4.3/plugins/openstack/#cloudify-openstack-server-connected-to-security-group
*   The server needs to be associated with a keypair. To achieve that, use the `cloudify.openstack.server_connected_to_keypair` relationship.
*   The server needs to be connected to the network. To achieve that, use a `cloudify.relationships.connected_to` relationship
    between the server and the network.
*   Add the property for agent configuration (`agent_config`) as follows:

    ```yaml
    properties:
      agent_config:
        install_method: { get_input: agent_install_method }
        user: { get_input: agent_user }
        key: { get_input: agent_key }
    ```

    Also, add the relevant input definitions to the `input:` section. The type of all three inputs should be `string`.
    The default for `agent_install_method` should be `none`, and the default for the two others should be an empty string
    (`''`).
    
## Step 5: Run the blueprint locally

Prepare an inputs file, containing the values for the various inputs you had defined.
For local invocations (using `local` profile), you don't have to specify the `agent_*` inputs.

Then:

```bash
cfy install <path_to_blueprint> -i <path_to_inputs_file>
```

## Step 6 (optional): Run the blueprint on a manager

Modify the inputs file so it contains overrides to the `agent_*` inputs:

*   `agent_install_method` should be set to `remote`.
*   `agent_user` should be set to a user that is allowed to log into the VM you're creating.
*   `agent_key` should be set to the path of the private key file that the manager should use to SSH into the
    new VM.
