#!/bin/bash -e

ctx logger info "Starting Apache web server..."
sudo systemctl start httpd
ctx logger info "Done."