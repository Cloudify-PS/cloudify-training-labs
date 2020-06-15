# ansible-example

Cloudify solves the problem of integrating your multiple deployment vectors:
  - Infrastructure Management
  - Deployment Configuration
  - CI/CD Integration

Integrations are accomplished via plugins. We have the plugins for IaaS (Openstack, Azure, AWS, GCP, etc.) And we also have plugins for configuration (Fabric, Script, REST, etc).

Add to that list Ansible support.

We have a new Ansible plugin at Cloudify. This plugin enables users who provision resources with Cloudify to configure their resources with Ansible. Also, ansible users can bring their existing playbooks into Cloudify blueprints.

Let’s start off with a simple example, like Ansible’s “Writing Your First Playbook”. Below, we will take that playbook and put it into a Cloudify Blueprint and deploy it.

You can download the code from this example [here](https://github.com/EarthmanT/ansible-example).

## Preliminary: Create a work directory:

Note: You will need a Cloudify Manager, as well as the IP, Username, and SSH key file to an existing VM to run this example.

```python
mkdir ansible-example
cd ansible-example
```

Next, we will create the Ansible Playbook.

Put the final code from the Ansible Example in your playbook.yaml.

```bash
touch playbook.yaml
```

```
---
- name: Install nginx
  hosts: host.name.ip
  become: true
  tasks:
  - name: Add epel-release repo
    yum:
      name: epel-release
      state: present
  - name: Install nginx
    yum:
      name: nginx
      state: present
  - name: Insert Index Page
    template:
      src: index.html
      dest: /usr/share/nginx/html/index.html
  - name: Start NGiNX
    service:
      name: nginx
      state: started
```

Add the index.html file:

```bash
touch index.html
```

```
<html>
    <header>
        <title>Cloudify Hello World</title>
    </header>
<body>
    <h1>Hello, World!</h1>
</body>
</html>
```

Now, we want a blueprint in blueprint.yaml:

```bash
touch blueprint.yaml
```

```
tosca_definitions_version: cloudify_dsl_1_3

imports:
  - http://cloudify.co/spec/cloudify/4.5.5/types.yaml
  - http://www.getcloudify.org/spec/ansible-plugin/2.0.2/plugin.yaml

inputs:

  ip:
    type: string
    description: The VM IP.

  username:
    type: string
    description: The VM SSH user.

  private_key:
    type: string
    description: Full path to the VM's private key.

node_types:

  vm:
    derived_from: cloudify.nodes.Compute
    properties:
      agent_config:
        default:
          install_method: none
          key: { get_input: private_key }
          user: { get_input: username }
    interfaces:
      cloudify.interfaces.lifecycle:
        start:
          implementation: ansible.cloudify_ansible.tasks.run
          inputs:
            site_yaml_path:
              default: playbook.yaml

node_templates:

  vm:
    type: vm
    properties:
      ip: { get_input: ip }
```

Install via Cloudify:

```bash
cfy plugins bundle-upload
cfy install blueprint.yaml
```

That was a pretty basic example, however we have other examples, such as:
- [Kubernetes Blueprint](https://github.com/cloudify-community/blueprint-examples/tree/master/kubernetes), based on Kubespray (Ansible Kubernetes Playbook).
- [DB-LB-App](https://github.com/cloudify-community/blueprint-examples/tree/master/db-lb-app), a modular application utilizing Ansible Playbooks for MariaDB/Galera Cluster, HAProxy, and Drupal7.
- Testing Examples with Vagrantfile (OpenVPN, Clearwater, LAMP, etc).

Explore those examples, and submit questions on our [Google User Groups](https://groups.google.com/forum/#!forum/cloudify-users) or [Blueprint Examples Github Repo](https://github.com/cloudify-community/blueprint-examples).

