# Lab: Multitenancy

The purpose of this lab is to show the multitenancy features implemented in Cloudify.

Multi-tenancy is a function that enables you to create multiple independent logical groups as isolated environments, which can be managed by a single Cloudify Manager. A tenant is a logical entity that contains all its resources, for example, blueprint, deployment, workflows and so on. Using multi-tenancy is useful when you want to limit access to a specific set of data (the tenant) to a defined set of users.
When you install Cloudify, a default tenant, named default-tenant, is also installed. You can use the default tenant or create one or more new tenants.
 
## Step 1: Log in as admin
```
cfy profiles use -u admin -p <password>
```
Use the password generated during the Manager Bootstrapping lab.

## Step 2: Create 2 tenants using the following commands
```
cfy tenants create TenantA 
cfy tenants create TenantB
```

## Step 3: Show all 3 tenants that the admin can access (default_tenant, TenantA and TenantB)

```
cfy tenants list
```

You should be able to see the nely created tenants
```
...

Listing all tenants...

Tenants:
+----------------+--------+-------+
|      name      | groups | users |
+----------------+--------+-------+
| default_tenant |        |   1   |
|   TenantA      |        |       |
|   TenantB      |        |       |
+----------------+--------+-------+
```

## Step 4: Create 3 users:
cfy users create User1 -p password 
cfy users create User2 -p password
cfy users create User3 -p password

## Step 5: Create a user-group using:
```
cfy user-groups create UserGroupI
```

## Step 5: Add 2 users (User1 and User2) to the user-group:
```
cfy user-groups add-user -g UserGroupI User1
cfy user-groups add-user -g UserGroupI User2
```

## Step 6: Assign users to the tenants:
```
cfy tenants add-user-group -t TenantA UserGroupI
cfy tenants add-user -t TenantB User3
```

## Step 7: Upload a blueprint to the tenant using the -t tenant flag:
```
cfy blueprints upload -b singlehost-blueprint.yaml -t TenantA https://github.com/cloudify-cosmo/cloudify-hello-world-example/archive/master.zip
```

## Step 8: See the resource that was just uploaded:
```
cfy blueprints list
```

You should be able to see your blueprint listed for the specified tenant
```
Listing all blueprints...

Blueprints:
+------------------------------+----------------------+---------------------------+--------------------------+--------------------------+------------+----------------+------------+
|              id              |     description      |       main_file_name      |        created_at        |        updated_at        | permission |  tenant_name   | created_by |
+------------------------------+----------------------+---------------------------+--------------------------+--------------------------+------------+----------------+------------+
| singlehost-blueprint.yaml    |                      | singlehost-blueprint.yaml | 2017-04-04 06:48:53.255  | 2017-04-04 06:48:53.255  |  creator   |     TenantA    |   admin    |
+------------------------------+----------------------+---------------------------+--------------------------+--------------------------+------------+----------------+------------+
```

## Step 9: Login as User1
```
cfy profiles set -u User1 -p password -t TenantA
```

## Step 10: Show the user can only see TenantA
```
cfy tenants list
```

Example output

```
Listing all tenants...

Tenants:
+----------------+--------+-------+
|      name      | groups | users |
+----------------+--------+-------+
|   TenantA      |   1    |   1   |
+----------------+--------+-------+
```

## Step 11: Show the user can see the resources in TenantA
```
cfy blueprints list
```
You should be able to see previously uploaded bluyeprint for this tenant
```
Listing all blueprints...

Blueprints:
+------------------------------+----------------------+---------------------------+--------------------------+--------------------------+------------+----------------+------------+
|              id              |     description      |       main_file_name      |        created_at        |        updated_at        | permission |  tenant_name   | created_by |
+------------------------------+----------------------+---------------------------+--------------------------+--------------------------+------------+----------------+------------+
| singlehost-blueprint.yaml    |                      | singlehost-blueprint.yaml | 2017-04-04 06:48:53.255  | 2017-04-04 06:48:53.255  |  creator   |     TenantA    |   admin    |
+------------------------------+----------------------+---------------------------+--------------------------+--------------------------+------------+----------------+------------+
```


## Step 12: Show that User1 can’t access tenants he’s not associated with: 
```
cfy profiles set -u User1 -p password -t TenantB 
```

You should get error message: <User username=`User1`> is not associated with <Tenant name=`TenantB`>

## Step 13: Login with User3 to tenantB:
```
cfy profiles set -u User3 -p password -t TenantB
```

## Step 14: Show the user can only see TenantB
```
cfy tenants list
```

```
Listing all tenants...

Tenants:
+----------------+--------+-------+
|      name      | groups | users |
+----------------+--------+-------+
|   TenantB      |   1    |   1   |
+----------------+--------+-------+
```

## Step 15: Show the user can't see any resources because there aren't any in tenantB. 
```
cfy blueprints list
```

Example output:

```
Listing all blueprints...

Blueprints:
+------------------------------+----------------------+---------------------------+--------------------------+--------------------------+------------+----------------+------------+
|              id              |     description      |       main_file_name      |        created_at        |        updated_at        | permission |  tenant_name   | created_by |
+------------------------------+----------------------+---------------------------+--------------------------+--------------------------+------------+----------------+------------+
+------------------------------+----------------------+---------------------------+--------------------------+--------------------------+------------+----------------+------------+
```
User should not be able to view TenantA blueprint

