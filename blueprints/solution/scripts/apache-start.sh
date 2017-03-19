#!/bin/bash -e

ctx logger info "Starting Apache web server..."
sudo systemctl apache2 start
ctx logger info "Done."