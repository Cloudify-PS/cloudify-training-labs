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
    API_Gateway.Resources.Deployment
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    AWS API Gateway Deployment interface
'''
# Requests
import requests
# Cloudify
from cloudify.exceptions import RecoverableError, NonRecoverableError
from api_gateway.constants import NODE_TYPE_API
from api_gateway import utils
from api_gateway.connection import APIGatewayConnection
# Boto
from botocore.exceptions import ClientError

# pylint: disable=W0212


def create(ctx, **_):
    '''Creates an AWS API Gateway REST API Deployment'''
    props = ctx.node.properties
    # Get a connection to the service
    client = APIGatewayConnection(ctx.node).client()
    # Get the parent API
    api_resource_id = props.get('api_id', utils.get_ancestor_resource_id(
        ctx.instance, NODE_TYPE_API))
    # Check if we are creating something or not
    if not props['use_external_resource']:
        # Actually create the resource
        ctx.logger.info('Creating Deployment')
        # Parameters
        params = dict(
            restApiId=api_resource_id,
            stageName=props['name'],
            stageDescription=props.get('description', ''))
        resource = client.create_deployment(**params)
        ctx.logger.debug('Response: %s' % resource)
        utils.update_resource_id(ctx.instance, resource['id'])
    # Get the resource ID (must exist at this point)
    resource_id = utils.get_resource_id(raise_on_missing=True)
    # Get the resource
    ctx.logger.debug('Getting Deployment "%s" properties' % resource_id)
    try:
        resource = client.get_deployment(
            restApiId=api_resource_id, deploymentId=resource_id)
        stages = client.get_stages(
            restApiId=api_resource_id, deploymentId=resource_id)
        if not stages or 'item' not in stages or not len(stages['item']):
            raise NonRecoverableError('No stages found for deployment!')
        ctx.logger.debug('Deployment "%s": %s' % (resource_id, resource))
        ctx.instance.runtime_properties['stage_name'] = \
            stages['item'][0]['stageName']
        ctx.instance.runtime_properties['invoke_url'] = \
            'https://%s.execute-api.%s.amazonaws.com/%s' % (
                api_resource_id, client._client_config.region_name,
                stages['item'][0]['stageName'])
    except ClientError:
        raise NonRecoverableError('Error creating Deployment')


def create_validation(ctx, path, expected, **_):
    '''Validates the create process'''
    # Find the endpoint to test against
    invoke_url = ctx.instance.runtime_properties['invoke_url']
    # Normalize url / path
    if invoke_url.endswith('/'):
        invoke_url = invoke_url[:-1]
    invoke_url = invoke_url + (path if path.startswith('/') else path + '/')
    ctx.logger.debug('GET %s' % invoke_url)
    ctx.logger.debug('Expecting response: "%s"' % expected)
    # Make the request
    res = requests.get(invoke_url)
    ctx.logger.debug('Actual response: "%s"' % res.text)
    # Validate
    if res.text != expected:
        raise NonRecoverableError('Received "%s", expected "%s"'
                                  % (res.text, expected))


def delete(ctx, **_):
    '''Deletes an AWS API Gateway REST API Deployment'''
    props = ctx.node.properties
    # Get a connection to the service
    client = APIGatewayConnection(ctx.node).client()
    # Get the parent API
    api_resource_id = props.get('api_id', utils.get_ancestor_resource_id(
        ctx.instance, NODE_TYPE_API))
    # Get the resource ID (must exist at this point)
    resource_id = utils.get_resource_id()
    if not resource_id:
        ctx.logger.warn('Missing resource ID. Skipping workflow...')
        return
    # Delete the resource (if needed)
    if props['use_external_resource']:
        return
    if ctx.operation.retry_number == 0:
        stages = client.get_stages(
            restApiId=api_resource_id, deploymentId=resource_id)
        # There are stages left that must be removed
        if stages and 'item' in stages and len(stages['item']):
            for item in stages['item']:
                ctx.logger.debug('Removing deployment stage "%s"'
                                 % item['stageName'])
                client.delete_stage(restApiId=api_resource_id,
                                    stageName=item['stageName'])
        ctx.logger.info('Deleting Deployment "%s"' % resource_id)
        try:
            client.delete_deployment(
                restApiId=api_resource_id, deploymentId=resource_id)
            ctx.logger.debug('Deployment "%s" deleted' % resource_id)
        except ClientError as exc:
            raise RecoverableError('Error deleting Deployment: %s' % str(exc))
