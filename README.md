# Cloudify Training: Labs

This project contains the labs material for the official Cloudify training course.

## Labs Order

1.  [CLI Installation](cli-installation)
2.  [Running Basic Blueprint Locally](running-basic-locally)
3.  [Creating a Simple Blueprint](blueprints)
4.  [Running NodeCellar Locally](running-nodecellar-locally)
5.  [Using Scripts in Lifecycle Events](using-scripts)
6.  [Developing a Simple Plugin](developing-simple-plugin)
7.  [Workflows](workflows)
8.  [Manager Bootstrapping](simple-bootstrap)
9.  [Installing NodeCellar on Cloudify Manager](running-nodecellar-on-manager)
10. [Monitoring](monitoring)
11. [Orchestrating OpenStack Resources](orchestrating-openstack)
12. [Cloudify Manager and OpenStack](openstack-manager)
13. [Scaling](scaling)
14. [Bootstrapping Offline](offline-bootstrap)
15. [Troubleshooting](troubleshooting)

## Virtual Machines

### Creating Your Own CLI VM

If you don't have a CLI VM provided to you, or you would like to use your own image:

* Use a CentOS 7.x image
* Allow at least 1GB of RAM and 5GB of storage
* Make sure that `iptables` is disabled. This is not a requirement of the CLI per-se, but rather
a requirement of the training labs; the labs involve using Cloudify in "local mode" to install applications locally, and
in order to verify proper installation, these applications have to be accessible through their designated ports.
  * If you are using `firewalld`, stop it and mask it:

    ```bash
    sudo systemctl stop firewalld
    sudo systemctl mask firewalld
    ```
  * If you are using `iptables-services`, stop it and mask it:

    ```bash
    sudo systemctl stop iptables
    sudo systemctl mask iptables
    ```
* Make sure that the VM is connected to a security group that is very permissive (same reasoning as for
`iptables`).

* Install `unzip` and `git` (needed for the labs; not Cloudify prerequisites)

  ```bash
  sudo yum -y install unzip git
  ```

* Install `pip` (required for the plugin development lab):

  ```bash
  curl https://bootstrap.pypa.io/get-pip.py | sudo python
  ```

* Install `virtualenv`:

  ```bash
  sudo pip install virtualenv
  ```
  
* Clone the training labs (replace `<labs-branch>` with the branch corresponding to the Cloudify version you are
  training for. For example: `3.4.2`)

  ```bash
  git clone -b <labs-branch> https://github.com/Cloudify-PS/cloudify-training-labs.git
  ```

### Creating Your Own Cloudify Manager VM

If you don't have a Manager VM provided to you, or you would like to use your own image:

* Use a CentOS 7.x image
* Ensure that the VM answers to the prerequisites documented in Cloudify's documentation website (http://docs.getcloudify.org/3.4.2/manager/prerequisites/),
with the following exceptions:
  * The minimum amount of RAM should be 4GB.
  * The security group to which this VM is connected should have more permissive rules than the ones stated,
  because certain labs install topologies on the very same VM as the Manager's.
  It is recommended to allow incoming traffic on all ports.
* Make sure that `iptables` is disabled. Similarly to the CLI VM's case, this is not a Cloudify requirement but a training
material requirement.
