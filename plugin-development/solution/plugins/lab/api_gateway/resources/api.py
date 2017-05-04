# #######
# Copyright (c) 2017 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    * See the License for the specific language governing permissions and
#    * limitations under the License.
'''
    API_Gateway.Resources.API
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    AWS API Gateway REST API interface
'''
import json
# Cloudify
from cloudify.exceptions import RecoverableError, NonRecoverableError
from api_gateway import utils
from api_gateway.connection import APIGatewayConnection
# Boto
from botocore.exceptions import ClientError


def create(ctx, **_):
    '''Creates an AWS API Gateway REST API'''
    props = ctx.node.properties
    # Get a connection to the service
    client = APIGatewayConnection(ctx.node).client()
    # Check if we are creating something or not
    if not props['use_external_resource']:
        # Actually create the resource
        ctx.logger.info('Creating REST API')
        resource = client.create_rest_api(**dict(
            name=props['name'],
            description=props['description'],
            version=props['version']))
        ctx.logger.debug('Response: %s' % resource)
        utils.update_resource_id(ctx.instance, resource['id'])
    # Get the resource ID (must exist at this point)
    resource_id = utils.get_resource_id(raise_on_missing=True)
    # Get the resource
    ctx.logger.debug('Getting REST API "%s" properties' % resource_id)
    try:
        resource = client.get_rest_api(restApiId=resource_id)
        ctx.logger.debug('REST API "%s": %s' % (resource_id, resource))
    except ClientError:
        raise NonRecoverableError('Error creating REST API')


def configure(ctx, **_):
    '''Configures an AWS API Gateway REST API'''
    props = ctx.node.properties
    if 'import' not in props or not props['import']:
        ctx.logger.debug('Skipping API import')
        return
    # Get a connection to the service
    client = APIGatewayConnection(ctx.node).client()
    # Get the resource ID (must exist at this point)
    resource_id = utils.get_resource_id(raise_on_missing=True)
    # Import data
    params = dict(restApiId=resource_id,
                  mode=props.get('import_mode', 'overwrite'))
    if isinstance(ctx.node.properties['import'], dict):
        ctx.logger.debug('Importing data from YAML definition')
        params['body'] = json.dumps(ctx.node.properties['import'])
    elif isinstance(ctx.node.properties['import'], str):
        ctx.logger.debug('Importing data from file')
        params['body'] = open(ctx.node.properties['import'], 'rb')
    else:
        raise NonRecoverableError(
            'Invalid import data format. Expected either dict or str.')
    ctx.logger.debug('Importing REST API data')
    resource = client.put_rest_api(**params)
    ctx.logger.debug('Response: %s' % resource)


def delete(ctx, **_):
    '''Deletes an AWS API Gateway REST API'''
    # Get a connection to the service
    client = APIGatewayConnection(ctx.node).client()
    # Get the resource ID (must exist at this point)
    resource_id = utils.get_resource_id()
    if not resource_id:
        ctx.logger.warn('Missing resource ID. Skipping workflow...')
        return
    # Delete the resource (if needed)
    if ctx.node.properties['use_external_resource']:
        return
    if ctx.operation.retry_number == 0:
        ctx.logger.info('Deleting REST API "%s"' % resource_id)
        try:
            client.delete_rest_api(restApiId=resource_id)
            ctx.logger.debug('REST API "%s" deleted' % resource_id)
        except ClientError as exc:
            raise RecoverableError('Error deleting REST API: %s' % str(exc))
