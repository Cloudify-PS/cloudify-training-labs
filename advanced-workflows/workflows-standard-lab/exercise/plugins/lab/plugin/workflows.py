'''Copyright Gigaspaces, 2017, All Rights Reserved'''
import json
from cloudify.plugins.workflows import scale_entity
from cloudify.exceptions import NonRecoverableError, RecoverableError
import requests


def get_wind_speed(ctx, city_name):
    '''
        Gets wind speed from an external service based on city

    :param str city_name: Name of a city to check wind speed
        for. Format is "Boston, MA".
    :rtype: int
    :returns: Wind speed in MPH
    '''
    ctx.logger.debug('Executing get_wind_speed(%s)' % city_name)
    if not city_name:
        raise NonRecoverableError('Missing city name for wind speed check')
    url = 'https://query.yahooapis.com/v1/public/yql?q=' \
          'select wind from weather.forecast where woeid in ' \
          '(select woeid from geo.places(1) where text="%s")' \
          '&format=json&env=store://datatables.org/alltableswithkeys' \
          % city_name
    ctx.logger.debug('Querying URL "%s"' % url)
    res = requests.get(url)
    try:
        data = res.json()
        ctx.logger.debug('Response received: %s' % json.dumps(data, indent=2))
        speed = data.get('query', {}).get('results', {}).get(
            'channel', {}).get('wind', {}).get('speed')
        if not speed:
            raise RecoverableError(
                'Missing wind speed data from weather service')
        return int(speed)
    except ValueError:
        raise RecoverableError(
            'Unexpected response from weather service')


def get_scale_group_properties(ctx, scalable_entity_name):
    '''Helper method to get scaling group information'''
    # Workaround to clear any scaling group caching
    # pylint: disable=W0212
    ctx.internal.handler._scaling_groups = None
    return ctx.deployment.scaling_groups.get(
        scalable_entity_name, dict()).get('properties', dict())


def scale_if_needed(ctx, scalable_entity, delta):
    '''
        Scales a node by `delta` only if it's within
        scale thresholds (max / min). If the delta would
        cause the node instance count to go beyond or
        below the scale threshold, the scale operation will not execute.

    .. note::

        The `scale_entity` object must be scalable. Generally, this
        means that it's included in a scale group with an
        attached scale policy.

    :param str scale_entity: Cloudify entity (node or group) to scale
    :param int delta: Amount to scale by (negative value for scaling down)
    '''
    ctx.logger.debug('scale_if_needed(%s, %s)' % (scalable_entity, delta))
    # Get how many instances already exist in the scale_entity (group)
    sg_props = get_scale_group_properties(ctx, scalable_entity)
    if sg_props is None:
        raise RecoverableError('Could not get scalable entity properties '
                               'of "%s"' % scalable_entity)
    # Check scaling bounds
    if (sg_props['current_instances'] + delta) < sg_props['min_instances']:
        ctx.logger.warn('Scaling will be skipped. Instance count would '
                        'go below scaling group min_instances')
        return
    elif (sg_props['current_instances'] + delta) > sg_props['max_instances']:
        ctx.logger.warn('Scaling will be skipped. Instance count would '
                        'go above scaling group max_instances')
        return
    # Scale the node by delta
    ctx.logger.debug('Scaling "%s" by %s' % (scalable_entity, delta))
    try:
        # Call Cloudify's built-in scale method
        # This could also be done by running a scale
        # workflow on a manager's deployment using the REST API
        scale_entity(ctx=ctx,
                     scalable_entity_name=scalable_entity,
                     delta=delta,
                     scale_compute=False)
    except (AttributeError, RuntimeError) as ex:
        raise RecoverableError(
            'The built-in scale workflow encountered an '
            'exception. %s' % str(ex))


def check_wind_speed(ctx, city_name,
                     scalable_entity_name, max_wind_speed=8, **_):
    '''
        Checks the wind speed of a city and scales a node
        depending on the value. If the wind speed breeches
        `max_wind_speed`, the node is scaled down by 1. If
        the wind speed is less, the node is scaled up by 1.

    :param str city_name: Name of a city to check wind speed
        for. Format is "Boston, MA".
    :param str node_name: Name of a Cloudify node to scale.
    :param int max_wind_speed: Maximum wind speed allowed
        before scaling down occures. This really shouldn't have
        a default value... you should fix that!
    '''
    # Convert types in case it's unicode
    max_wind_speed = int(max_wind_speed)
    # Get the current wind speed
    ctx.logger.info('Checking wind speed for %s' % city_name)
    speed = get_wind_speed(ctx, city_name)
    ctx.logger.info('Wind speed for %s is currently %s mph (max = %s)'
                    % (city_name, speed, max_wind_speed))
    # ========================
    # === LAB CHALLENGE #2 ===
    # ========================
    # Now that you have the current wind speed and max safe wind speed,
    # calculate the scaling delta that you want to use. Remember,
    # there's no right answer here, as long as you don't scale up
    # when the wind speed is too high (risking virtual lives!).
    delta = 0
    # Scale based on a scale delta
    scale_if_needed(ctx, scalable_entity_name, delta)
