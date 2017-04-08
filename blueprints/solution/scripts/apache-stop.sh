#!/bin/bash -e

ctx logger info "Stopping Apache web server..."
sudo systemctl stop httpd
ctx logger info "Done."
