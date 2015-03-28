from cloudify import ctx

"""
Gets the mongo ip address and port and stores them in a file to be sourced by
the nodecellar startup script
"""

mongo_ip_address = ctx.target.instance.host_ip

ctx.logger.info('Mongo IP address is {0}'.format(mongo_ip_address))

props = {
    'MONGO_HOST': mongo_ip_address
}

ctx.source.instance.runtime_properties['docker_env_var'] = props
