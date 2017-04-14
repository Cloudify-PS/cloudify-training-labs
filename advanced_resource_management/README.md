# Lab: Advanced user and resource management

The purpose of this lab is to show the advanced user and resource management

This lab shows the following procedures:
* Changing a user's role
* Uploading resources as private
* Showing the resource's creator 
* Deactivating a user. 


## Step 1: Login as admin:
```
cfy profiles set -u admin -p <password> -t TenantA 
```

Use the password provided by bootstrap process in Manager Bootstrapping lab

## Step 2: Change the role of user2 to admin:
```
cfy users set-role -r admin User2
```

## Step 3: Login as User2:
```
cfy profiles set -u User2 -p password -t TenantA 
```

## Step 4: Show current profile
```
cfy profiles show-current 
```

Example output:
```
...

Active profile:
+---------------+--------------+----------+-------------------------------------+----------+-----------+---------------+------------------+----------------+-----------------+
|      name     |  manager_ip  | ssh_user |             ssh_key_path            | ssh_port | rest_port | rest_protocol | manager_username | manager_tenant | bootstrap_state |
+---------------+--------------+----------+-------------------------------------+----------+-----------+---------------+------------------+----------------+-----------------+
| *10.239.2.241 | 10.239.2.241 |  centos  | /Users/user/rackspace/key.pem       |    22    |     80    |      http     |      User2       |     TenantA    |     Complete    |
+---------------+--------------+----------+-------------------------------------+----------+-----------+---------------+------------------+----------------+-----------------+

...
```


## Step 5: Upload a blueprint as private:
```
cfy blueprints upload -b openstack-blueprint.yaml -t TenantA --private-resource https://github.com/cloudify-cosmo/cloudify-hello-world-example/archive/master.zip
```

## Step 6: Show the tenant’s resources - the current user can see all of them. Pay attention to the “created_by” field:
```
cfy blueprints list
```

Example output

```
Listing all blueprints...

Blueprints:
+------------------------------+----------------------+---------------------------+--------------------------+--------------------------+------------+----------------+------------+
|              id              |     description      |       main_file_name      |        created_at        |        updated_at        | permission |  tenant_name   | created_by |
+------------------------------+----------------------+---------------------------+--------------------------+--------------------------+------------+----------------+------------+
| singlehost-blueprint.yaml    |                      | singlehost-blueprint.yaml | 2017-04-04 06:48:53.255  | 2017-04-04 06:48:53.255  |  creator   |     TenantA    |   User2    |
+------------------------------+----------------------+---------------------------+--------------------------+--------------------------+------------+----------------+------------+
```

## Step 7: Login as User1
```
cfy profiles set -u User1 -p password -t TenantA 
```

## Step 8: Show the tenant’s resources - the current user can only see the public resources in the tenant:
```
cfy blueprints list 
```

example output:
```
Listing all blueprints...

Blueprints:
+------------------------------+----------------------+---------------------------+--------------------------+--------------------------+------------+----------------+------------+
|              id              |     description      |       main_file_name      |        created_at        |        updated_at        | permission |  tenant_name   | created_by |
+------------------------------+----------------------+---------------------------+--------------------------+--------------------------+------------+----------------+------------+
+----------
```


## Step 9: Login as admin:
```
cfy profiles set -u admin -p <password> 
```

Use the password provided by bootstrap process in Manager Bootstrapping lab

## Step 10: Show the tenant’s resources - the current user is admin and therefore can see all of them:
```
cfy blueprints list
```

Output should contain blueprint from Step 6

## Step 11: Deactivate User1:
```
cfy users deactivate User1 
```

## Step 12: Try to login as User1
```
cfy profiles set -u User1 -p Aa123456 -t tenantA. 
```

You should receive the error -  <User username=`User1`> is not active.

