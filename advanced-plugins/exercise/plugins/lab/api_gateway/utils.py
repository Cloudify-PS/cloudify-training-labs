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
    API_Gateway.Utils
    ~~~~~~~~~~~~~~~~~
    AWS API Gateway helper utilities
'''
from cloudify import ctx
from cloudify.exceptions import NonRecoverableError
from api_gateway import constants


def get_resource_id(node=None, instance=None,
                    raise_on_missing=False):
    '''
        Gets the (external) resource ID of a Cloudify node and/or instance.
        depending on the environment available.
    :param `cloudify.context.NodeContext` node:
        Cloudify node.
    :param `cloudify.context.NodeInstanceContext` instance:
        Cloudify node instance.
    :param boolean raise_on_missing: If True, causes this method to raise
        an exception if the resource ID is not found.
    :raises: :exc:`cloudify.exceptions.NonRecoverableError`
    '''
    node = node if node else ctx.node
    instance = instance if instance else ctx.instance
    props = node.properties if node else {}
    runtime_props = instance.runtime_properties if instance else {}
    # Search instance runtime properties first, then the node properties
    resource_id = runtime_props.get(
        constants.EXTERNAL_RESOURCE_ID, props.get('resource_id'))
    if not resource_id and raise_on_missing:
        raise NonRecoverableError(
            'Missing resource ID! Node=%s, Instance=%s' % (
                node.id if node else None,
                instance.id if instance else None))
    return resource_id


def update_resource_id(instance, val):
    '''Updates an instance's resource ID'''
    instance.runtime_properties[constants.EXTERNAL_RESOURCE_ID] = val


def find_rels_by_type(node_instance, rel_type):
    '''
        Finds all specified relationships of the Cloudify
        instance.
    :param `cloudify.context.NodeInstanceContext` node_instance:
        Cloudify node instance.
    :param str rel_type: Cloudify relationship type to search
        node_instance.relationships for.
    :returns: List of Cloudify relationships
    '''
    return [x for x in node_instance.relationships
            if rel_type in x.type_hierarchy]


def find_rel_by_type(node_instance, rel_type):
    '''
        Finds a single relationship of the Cloudify instance.
    :param `cloudify.context.NodeInstanceContext` node_instance:
        Cloudify node instance.
    :param str rel_type: Cloudify relationship type to search
        node_instance.relationships for.
    :returns: A Cloudify relationship or None
    '''
    rels = find_rels_by_type(node_instance, rel_type)
    return rels[0] if len(rels) > 0 else None


def get_ancestor_by_type(inst, node_type):
    '''
        Gets an ancestor context (recursive search)
    :param `cloudify.context.NodeInstanceContext` inst: Cloudify instance
    :param string node_type: Node type name
    :returns: Ancestor context or None
    '''
    # Find a parent of a specific type
    rel = find_rel_by_type(inst, 'cloudify.relationships.contained_in')
    if not rel:
        return None
    if node_type in rel.target.node.type_hierarchy:
        return rel.target
    return get_ancestor_by_type(rel.target.instance, node_type)


def get_ancestor_resource_id(node_instance,
                             node_type,
                             raise_on_missing=True):
    '''Finds an ancestor and gets its resource ID'''
    ancestor = get_ancestor_by_type(node_instance, node_type)
    if not ancestor:
        if raise_on_missing:
            raise NonRecoverableError('Error locating ancestor resource ID')
        return None
    return get_resource_id(instance=ancestor.instance,
                           raise_on_missing=raise_on_missing)
