# Lab: Security

In this lab, we will demonstrate security configuration on the Cloudify manager. Our starting point will be a simple manager blueprint, with its security configuration incomplete; your task will be to complete the security configuration and demonstrate that it works.

## Prerequisites

You will need to tear down the Cloudify Manager that you have previously bootstrapped.
To do that, execute the following from your CLI VM:

```bash
cd ~/work
cfy teardown -f
```

## Instructions
















## Step 1: Logging

Replace the strings `REPLACE_WITH_LOG_FILE_PATH` and `REPLACE_WITH_LOG_LEVEL` with applicable values for your environment.

## Step 2: Users configuration

Replace the string `REPLACE_WITH_USERS_CONFIGURATION` with either one or many user configurations. Note that these configurations must be understood by the user store driver being used; for the built-in `SimpleUserstore`, the expected fields are:

* `username`
* `password`
* `email`

## Step 3: SSL

Replace the strings `REPLACE_WITH_CERT_PATH` and `REPLACE_WITH_PRIVATE_KEY_PATH` with applicable values for your environment. You can either:

1. Use the provided key (`cert.key`) and certificate (`cert.crt`) files, located in `$LAB_ROOT/resources`; or
2. Create your own certificate & key file, and use them.

## Step 4: Tear existing manager down

Your current Cloudify Manager is not secured; as security configuration can only occur during bootstrapping, you have to tear your existing manager down. To do that,
uninstall all existing deployments, delete those deployments, delete all blueprints and then tear the manager down:

```bash
cd ~/work
cfy teardown -f
```

The manager teardown process does not delete the two docker containers from the manager's machine; these have to be deleted manually. To do that, SSH into the manager's
machine and run the following commands:

```bash
sudo service docker start
sudo docker stop cfy data
sudo docker rm cfy data
```

## Step 5: Configure CLI to use SSL

As the manager is currently secured, you need to prepare the CLI environment accordingly:

```bash
export CLOUDIFY_SSL_TRUST_ALL=true
export CLOUDIFY_USERNAME=some-username
export CLOUDIFY_PASSWORD=some-password
```

* The `CLOUDIFY_SSL_TRUST_ALL` environment variable will ensure that certificate validation is skipped. This is required for this lab as we are using a self-signed certificate.
* `CLOUDIFY_USERNAME` and `CLOUDIFY_PASSWORD` must be set to a username and password which are defined in the blueprint's user store section.

## Step 6: Bootstrap a new manager

Follow instructions similar to those presented in earlier labs, to bootstrap a new Cloudify Manager using the security-enabled blueprint:

```bash
cfy bootstrap --install-plugins -p $LAB_ROOT/simple-secured.yaml -i manager-inputs.yaml
```

**NOTE:** for bootstrap inputs, you can use the same inputs YAML file you had used previously (to bootstrap the non-secured manager).

## Step 7: Verify connectivity

Execute:

```bash
cfy status
```

And ensure you receive a proper status response.

## Step 8: Access the Cloudify Manager UI

As your manager is now secured by SSL, you can only access the UI via HTTPS:

```
https://<manager-vm-public-ip>
```

Contrary to before — when the manager was not secured — you will now be presented with a login screen. In order to log in, you must enter a username & password that are defined
in the manager's blueprint (see step 2 above).

![Secured Login](../../../raw/3.4.0/security/login.png "Secured Login")