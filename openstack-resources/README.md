# Lab: Creating OpenStack Resources

In this lab, we will write a blueprint that creates resources on OpenStack. We will create:

* A virtual machine
* A security group
* A network
* A subnet
* A router

Also, we will connect all resources together.

For the preparation of this lab, you will have to use the official OpenStack plugin documentation, located at: http://docs.getcloudify.org/3.4.1/plugins/openstack/

## Step 1: Create blueprint's skeleton

```yaml
tosca_definitions_version: cloudify_dsl_1_3

imports:
  - http://www.getcloudify.org/spec/cloudify/3.4.1/types.yaml
  - http://www.getcloudify.org/spec/openstack-plugin/2.0/plugin.yaml
```

This will import the standard Cloudify types, as well as the OpenStack plugin.

## Step 2: Add the external network

Documentation: http://docs.getcloudify.org/3.4.1/plugins/openstack/#cloudify-openstack-nodes-network

Notes:

*   You're not expected to *create* the external network; you should use the existing one that most likely already exists
    in your OpenStack installation. Therefore, use the `use_external_resource` property with the value `true`, and provide
    the external network's name in the `resource_id` property.

## Step 2: Add a router

Documentation: http://docs.getcloudify.org/3.4.1/plugins/openstack/#cloudify-openstack-nodes-router

The router needs to be connected to the external network. To achieve that, establish a `cloudify.relationships.connected_to`
relationship between the router and the external network node.

## Step 3: Add a network

Documentation: http://docs.getcloudify.org/3.4.1/plugins/openstack/#cloudify-openstack-nodes-network

Don't forget to provide the new network's name through the `resource_id` property.

## Step 4: Add a subnet

Documentation: http://docs.getcloudify.org/3.4.1/plugins/openstack/#cloudify-openstack-nodes-subnet

*   The subnet needs to be contained within the network that you had created. To achieve that, create a
    `cloudify.relationships.contained_in` relationship between the subnet and the network.

*   The subnet needs to have a "leg" in the router. To achieve that: http://docs.getcloudify.org/3.4.1/plugins/openstack/#cloudify-openstack-subnet-connected-to-router

*   Parameters for the subnet should be passed as entries in a dictionary property called `subnet`, as follows:

    ```yaml
    properties:
      subnet:
        cidr: a.b.c.d/e
    ```
    
    You may come up with any CIDR you'd like.

##  Step 5: Add a security group

Documentation: http://docs.getcloudify.org/3.4.1/plugins/openstack/#cloudify-openstack-nodes-securitygroup

We need only one rule: allow ingress traffic on port 22, from anywhere.

## Step 6: Add a virtual machine

Documentation: http://docs.getcloudify.org/3.4.1/plugins/openstack/#cloudify-openstack-nodes-server

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

*   The server needs to be connected to the security group. To achieve that: http://docs.getcloudify.org/3.4.1/plugins/openstack/#cloudify-openstack-server-connected-to-security-group
