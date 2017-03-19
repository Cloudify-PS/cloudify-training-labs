#!/bin/bash -e

ctx logger info "Stopping Apache web server..."
sudo systemctl httpd stop
ctx logger info "Done."
