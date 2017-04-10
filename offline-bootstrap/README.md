# Lab: Bootstrapping Offline

In this lab, we will imitate a scenario whereby both the CLI and the targeted Manager VM are disconnected from the outside
world, and bootstrap a Cloudify Manager that way.

**Note to instructor**: don't forget to reinstate public network access after this lab is done.

### (Instructor) Disable access to the public network

The instructor should disable access from within the training's environment to the public network.

### Verify access to files

A "Resources" VM has been prepared by the instructor, containing all resources required for bootstrapping a Manager without
having to access the public network. The resource locations are:

* YAML files referred to by the manager blueprint
  * http://<resources-vm-ip>:8080/yaml/spec/cloudify/4.0/types.yaml
  * http://<resources-vm-ip>:8080/yaml/spec/fabric-plugin/1.4.2/plugin.yaml
* Wagon file(s) for plugins used by the manager blueprint
  * http://<resources-vm-ip>:8080/cloudify_fabric_plugin-1.4.2-py27-none-linux_x86_64-centos-Core.wgn
* Manager resources package
  * http://<resources-vm-ip>:8080/cloudify-manager-resources_4.0.0-ga.tar.gz

Make sure that:

* Your CLI machine can access the YAML files and the Wagon file(s); and
* Your Manager machine can access the Manager resources package.

### Create a Cloudify working directory

```bash
mkdir ~/offline && cd ~/offline
```

### Create a new virtualenv

We're going to use a new virtualenv here, in order to exercise the installation of the Fabric plugin's wagon into it:

```bash
python get-cloudify.py --version 4.0 -e ~/offline-cfy-env -v
. ~/offline-cfy-env/bin/activate

cfy --version
```

### Install the Fabric wagon

For the bootstrap process to have access to the Fabric plugin code (remember: the Fabric plugin is used during
the bootstrap), the Fabric plugin's code needs to be available in the Python path. To do that, simply install the Fabric
plugin's Wagon file:

```bash
wagon install -s http://<resources-vm-ip>:8080/cloudify_fabric_plugin-1.4.2-py27-none-linux_x86_64-centos-Core.wgn -v
```

### Edit the `config.yaml` file

Edit the file `.cloudify/config.yaml` to add the necessary Import Resolver rules:

```yaml
import_resolver:
  implementation: dsl_parser.import_resolver.default_import_resolver:DefaultImportResolver
  parameters:
    rules:
      - 'http://www.getcloudify.org': 'http://<resources-vm-ip>:8080/yaml'
```

### Prepare a manager inputs file

```bash
cp ~/cloudify-manager-blueprints-3.4.2/simple-manager-blueprint-inputs.yaml ./offline-mgr-inputs.yaml
vi offline-mgr-inputs.yaml
```

And edit the required inputs. These were exercised in a previous lab; however, there's two more inputs that must
be uncommented and customized:

*   `dsl_resources`: you should only keep the `types.yaml` file and the Fabric plugin's `plugin.yaml` file. Remember
    to change the `source_path` so it leads to the Resources VM (`http://<resources-vm-ip>:8080/yaml/...`).

*   `import_resolver_rules`: should be uncommented, not modified. Note that it reads:
    ```yaml
    import_resolver_rules:
      - {'http://www.getcloudify.org/spec': 'file:///opt/manager/resources/spec'}
    ```

    - which means that all import requests to `http://www.getcloudify.org/spec/*` will be rewritten.

### Execute the bootstrap

```bash
cfy bootstrap -p ~/cloudify-manager-blueprints-3.4.2/simple-manager-blueprint.yaml -i offline-mgr-inputs.yaml  
```

_Note that in the command above, we didn't specify `--install-plugins`. There's no need to (as the required plugins
were already installed on the virtualenv by virtue of installing their Wagon files), plus it would not work as it'd
require access to the public network which is now disabled._

### Validate

Ensure that the manager is functioning properly:

```bash
cfy status
```

### (Instructor) Enable access to the public network

Don't forget!