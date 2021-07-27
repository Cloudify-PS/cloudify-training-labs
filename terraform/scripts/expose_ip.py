from cloudify import ctx

if __name__ == '__main__':
    tf = ctx.instance.runtime_properties
    ctx.instance.runtime_properties['ip'] = \
        tf['resources']['ip']['instances'][0]['attributes']['address']