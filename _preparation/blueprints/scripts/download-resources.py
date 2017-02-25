import urllib
from urllib2 import urlparse
import os

from cloudify import ctx
from cloudify.state import ctx_parameters as p

for x in p['resources']:
    url = x['url']
    location = x['location']

    location = os.path.expanduser(location)

    if location[-1] == '/':
        if not os.path.exists(location):
            os.makedirs(location)
    else:
        dirname = os.path.dirname(location)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

    if os.path.isdir(location):
        # 'location' is an existing directory. Get filename from url and use that.
        filename = urlparse.urlsplit(url).path.split('/')[-1]
        location = os.path.join(location, filename)

    ctx.logger.info("Downloading: {} -> {}".format(url, location))
    urllib.urlretrieve(url, location)
