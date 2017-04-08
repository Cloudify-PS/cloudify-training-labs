# Lab: CLI Advanced Installation

In this lab, we will uninstall the RPM-based CLI installation from the CLI VM's, and then reinstall it using the
Cloudify installation script.

### Step 1: Uninstall the RPM-based CLI

```
sudo rpm -ev cloudify
```

### Step 2: Download the CLI installation script

The installation script is available here: http://gigaspaces-repository-eu.s3.amazonaws.com/org/cloudify3/get-cloudify.py

(You can get the link to it from the Cloudify official documentation: http://docs.getcloudify.org/4.0.0/installation/from-script/)

```bash
curl -J -O http://gigaspaces-repository-eu.s3.amazonaws.com/org/cloudify3/get-cloudify.py
```

### Step 3: Run the installation script

```bash
python get-cloudify.py --version 3.4.2 -e ~/cfy-env -v
```

This will create a Python virtualenv in `~/cfy-env` and install the CLI in it.

### Step 4: Test the installation

```bash
. ~/cfy-env/bin/activate
cfy --version
```

You should receive the following output:

```bash
Cloudify CLI 3.4.2
```