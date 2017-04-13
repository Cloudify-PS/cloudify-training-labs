# Lab: Advanced user and resource management

The purpose of this lab is to show the advanced user and resource management

This lab shows the following procedures:
-Changing a user's role
-Uploading resources as private
-Showing the resource's creator 
-Deactivating a user. 


## Step 1: Login as admin:
```
cfy profiles set -u admin -p admin -t TenantA 
```

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

## Step 5: Upload a blueprint as private:
```
cfy blueprints upload -b openstack-blueprint.yaml -t TenantA --private-resource https://github.com/cloudify-cosmo/cloudify-hello-world-example/archive/master.zip
```

## Step 6: Show the tenant’s resources - the current user can see all of them. Pay attention to the “created_by” field:
```
cfy blueprints list
```

## Step 7: Login as User1
```
cfy profiles set -u User1 -p password -t TenantA 
```

## Step 8: Show the tenant’s resources - the current user can only see the public resources in the tenant:
```
cfy blueprints list 
```

## Step 9: Login as admin:
```
cfy profiles set -u admin -p admin 
```

## Step 10: Show the tenant’s resources - the current user is admin and therefore can see all of them:
```
cfy blueprints list
```

## Step 11: Deactivate User1:
```
cfy users deactivate User1 
```

## Step 12: Try to login as User1
```
cfy profiles set -u User1 -p Aa123456 -t tenantA. 
```

You should receive the error -  <User username=`User1`> is not active.

