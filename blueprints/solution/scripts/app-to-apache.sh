#!/bin/bash -e

ctx logger info "Installing application located in ${app_dir} to ${document_root}..."
sudo cp -R ${app_dir} ${document_root}/app
sudo chmod go+rx ${document_root}/app
ctx logger info "Done"