from cloudify import ctx

if __name__ == '__main__':
    ctx.instance.runtime_properties['hello_message'] = \
        "Hello, it's me! Node instance: {}".format(
            ctx.instance.id
        )