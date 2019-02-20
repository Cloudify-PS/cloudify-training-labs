# Lab: Multitenancy

The purpose of this lab is to show the multitenancy feature of Cloudify.

Multi-tenancy is a function that enables you to create multiple independent logical groups as isolated environments, which can be managed by a single Cloudify Manager.

A tenant is a logical entity that contains resources, such as blueprints, deployments, plugins and so on.
Using multi-tenancy is useful when you want to limit access to a specific set of data (the tenant) to a defined set of users.

When you install Cloudify, a default tenant, named `default_tenant`, is created.
You can use the default tenant, or create additional tenants, depending on your needs.
 
## Step 1: Log in as admin

Ensure that your active CLI profile is configured to use the `admin` user when communicating with the manager (use the
`cfy profiles list` command to verify). If that is not the case, either create a new profile or use the `cfy profiles
set -u <user> -p <password>` command to adjust the current profile.

## Step 2: Create two tenants

Use the following commands to create tenants:

```
cfy tenants create tenant_a 
cfy tenants create tenant_b
```

## Step 3: Display all tenants


```bash
cfy tenants list
```

This should show all three tenants that the admin can access: `default_tenant`, `tenant_a` and `tenant_b`.

```
Listing all tenants...

Tenants:
+----------------+--------+-------+
|      name      | groups | users |
+----------------+--------+-------+
| default_tenant |        |   1   |
|    tenant_a    |        |       |
|    tenant_b    |        |       |
+----------------+--------+-------+
```

## Step 4: Create users

We will now create three Cloudify users.

```bash
cfy users create user_1 -p password 
cfy users create user_2 -p password
cfy users create user_3 -p password
```

## Step 5: Create a group

```bash
cfy user-groups create group_a
```

## Step 6: Assign users to groups

```bash
cfy user-groups add-user -g group_a user_1
cfy user-groups add-user -g group_a user_2
```

## Step 7: Assign users and groups to tenants

```bash
cfy tenants add-user-group -t tenant_a group_a -r user
cfy tenants add-user -t tenant_b user_3 -r manager

```
**NOTE**: `tenant_a` should contain one user group and and two users. `tenant_b` should contain one user, no groups.

```
$ cfy tenants list
Listing all tenants...

Tenants:
+----------------+--------+-------+
|      name      | groups | users |
+----------------+--------+-------+
| default_tenant |        |   1   |
|    tenant_a    |   1    |   2   |
|    tenant_b    |        |   1   |
+----------------+--------+-------+
```

## Step 8: Upload a blueprint to a tenant

```bash
cfy blueprints upload -b mt_lab -t tenant_a ~/hello-world/no-monitoring-singlehost-blueprint.yaml
```

## Step 9: List all blueprints

```bash
cfy blueprints list
```

The blueprint uploaded to `tenant_a` should not be visible, as you are currently using the tenant `default_tenant`.

```
Listing all blueprints...

Blueprints:
+----+-------------+----------------+------------+------------+------------+-------------+------------+
| id | description | main_file_name | created_at | updated_at | permission | tenant_name | created_by |
+----+-------------+----------------+------------+------------+------------+-------------+------------+
+----+-------------+----------------+------------+------------+------------+-------------+------------+
```

## Step 10: Login as different user

Let's log in as `user_1`.

```bash
cfy profiles set -u user_1 -p password -t tenant_a
```

## Step 11: Show all tenants

```bash
cfy tenants list
```

You should only see the tenant(s) that `user_1` is allowed to see.
Example output:

```
Listing all tenants...

Tenants:
+----------+--------+-------+
|   name   | groups | users |
+----------+--------+-------+
| tenant_a |   1    |   2   |
+----------+--------+-------+
```

## Step 12: Show all blueprints

```bash
cfy blueprints list
```

You should only see blueprints that belong to this tenant.

```
Listing all blueprints...

Blueprints:
+--------+----------------------+-----------------------------------------+--------------------------+--------------------------+------------+-------------+------------+
|   id   |     description      |              main_file_name             |        created_at        |        updated_at        | visibility | tenant_name | created_by |
+--------+----------------------+-----------------------------------------+--------------------------+--------------------------+------------+-------------+------------+
| mt_lab | This blueprint ins.. | no-monitoring-singlehost-blueprint.yaml | 2018-04-22 11:30:21.122  | 2018-04-22 11:30:21.122  |   tenant   |   tenant_a  |   admin    |
+--------+----------------------+-----------------------------------------+--------------------------+--------------------------+------------+-------------+------------+
```

## Step 13: Attempt accessing disallowed tenant

Try accessing `tenant_b` with `user_1`:

```bash
cfy profiles set -u user_1 -p password -t tenant_b 
```

Manager output should contain information about the error:
```
401: User unauthorized: <User username=`user_1`> is not associated with <Tenant name=`tenant_b`>.
```

## Step 14: Login to other tenant

```bash
cfy profiles set -u user_3 -p password -t tenant_b
```

## Step 15: Display tenants

```bash
cfy tenants list
```

You should only see the tenant(s) that `user_3` is allowed to access:

```
Listing all tenants...

Tenants:
+----------+--------+-------+
|   name   | groups | users |
+----------+--------+-------+
| tenant_b |        |   1   |
+----------+--------+-------+
```

## Step 16: Show all blueprints
 
```bash
cfy blueprints list
```

You should not be able to see any blueprint, because no blueprint exists on
`tenant_b`.

Example output:

```
Listing all blueprints...

Blueprints:
+----+-------------+----------------+------------+------------+------------+-------------+------------+
| id | description | main_file_name | created_at | updated_at | permission | tenant_name | created_by |
+----+-------------+----------------+------------+------------+------------+-------------+------------+
+----+-------------+----------------+------------+------------+------------+-------------+------------+
```
