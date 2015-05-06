# Lab 8: Security

In this lab, we will demonstrate security configuration on the Cloudify manager. Our starting point will be a simple manager blueprint, with its security configuration incomplete; your task will be to complete the security configuration and demonstrate that it works.

It is assumed that the lab's files are extracted into `$LAB_ROOT`.

The blueprint, located in `$LAB_ROOT/blueprint/simple-secured.yaml`, contains placeholders for your modifications. These placeholders begin with the string `REPLACE_WITH`.

## Step 1: Logging

Replace the strings `REPLACE_WITH_LOG_FILE_PATH` and `REPLACE_WITH_LOG_LEVEL` with applicable values for your environment.

## Step 2: Users configuration

Replace the string `REPLACE_WITH_USERS_CONFIGURATION` with either one or many user configurations. Note that these configurations must be understood by the user store driver being used; for the built-in `SimpleUserstore`, the expected fields are:

* `username`
* `password`
* `email`

## Step 3: SSL

Replace the strings `REPLACE_WITH_CERT_PATH` and `REPLACE_WITH_PRIVATE_KEY_PATH` with applicable values for your environment.