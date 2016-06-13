# Cloudify Training: Labs

This project contains the labs material for the official Cloudify training course.

## Virtual Machines

### Creating your own CLI VM

If you don't have a CLI VM provided to you, or you would like to use your own image:

* Use a CentOS 7.0 image
* Allow at least 1GB of RAM and 5GB of storage
* Make sure that `iptables` is disabled. This is not a requirement of the CLI per-se, but rather
a requirement of the training labs; the labs involve using Cloudify in "local mode" to install applications locally, and
in order to verify proper installation, these applications have to be accessible through their designated ports.
  * If you are using `firewalld`, stop it and mask it:

    ```
    sudo systemctl stop firewalld
    sudo systemctl mask firewalld
    ```
  * If you are using `iptables-services`, stop it and mask it:

    ```
    sudo systemctl stop iptables
    sudo systemctl mask iptables
    ```
* Make sure that the VM is connected to a security group that is very permissive (same reasoning as for
`iptables`).

* Install `unzip` and `git` (needed for the labs; not Cloudify prerequisites)

  ```
  sudo yum -y install unzip git
  ```

### Creating your own Cloudify Manager VM

If you don't have a Manager VM provided to you, or you would like to use your own image:

* Use a CentOS 7.0 image
* Ensure that the VM answers to the prerequisites documented in Cloudify's documentation website (http://docs.getcloudify.org/3.4.0/manager/prerequisites/),
with the following exceptions:
  * The minimum amount of RAM should be 4GB.
  * The security group to which this VM is connected should have more permissive rules than the ones stated,
  because other labs (that depend on this one) install topologies on the very same VM as the Manager's.
  It is recommended to allow incoming traffic on all ports.
* Make sure that `iptables` is disabled. Similarly to the CLI VM's case, this is not a Cloudify requirement but a training
material requirement.

