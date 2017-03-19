#!/bin/bash -e

ctx logger info "Installing application located in ${app_dir} to ${document_root}..."
sudo ln -sf ${app_dir} ${document_root}
ctx logger info "Done"