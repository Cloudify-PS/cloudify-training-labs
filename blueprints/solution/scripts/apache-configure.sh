#!/bin/bash -e

document_root=$(ctx node properties document_root)
ctx logger info "Configuring Apache web server to listen on port $port"

sudo sh -c 'echo "Listen '${port}'" > /etc/httpd/conf.d/listen.conf'

# If started - reload the configuration.

if $(sudo systemctl status httpd); then
    ctx logger info "Apache web server already started; reloading configuration..."
    sudo systemctl reload httpd
fi

ctx logger info "Done."
