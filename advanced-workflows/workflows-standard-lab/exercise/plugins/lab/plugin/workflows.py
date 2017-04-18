'''Copyright Gigaspaces, 2017, All Rights Reserved'''
import json
import re
from cloudify.exceptions import NonRecoverableError, RecoverableError
import requests

CITY_NAME_REGEX = (r'^([a-z]+\,\s?[a-z]{2})$', re.IGNORECASE)


def get_wind_speed(ctx, city_name):
    '''
        Gets wind speed from an external service based on city

    :param str city_name: Name of a city to check wind speed
        for. Format is "<City>, <State Abbr.>".
    :rtype: int
    :returns: Wind speed in MPH
    '''
    ctx.logger.debug('Executing get_wind_speed(%s)' % city_name)
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


def check_wind_speed(ctx, city_name="Boston, MA", **_):
    '''
        Checks the wind speed of a city and logs the results.

    :param `CloudifyWorkflowContext` ctx: Cloudify workflow context. This
        is auto-injected into the function when called as a workflow.
    :param str city_name: Name of a city to check wind speed
        for. Format is "<City>, <State Abbr.>". By the time you complete
        the lab tasks, this should *not* have a default value.
    '''
    # Validate city name
    if re.compile(*CITY_NAME_REGEX).match(city_name) is None:
        raise NonRecoverableError(
            'Invalid city name format (regex: %s)' % CITY_NAME_REGEX[0])
    # Get the current wind speed
    ctx.logger.info('Checking wind speed for %s' % city_name)
    speed = get_wind_speed(ctx, city_name)
    ctx.logger.info('Wind speed for %s is currently %s mph'
                    % (city_name, speed))
