#!/bin/bash -e

# Create resources for "blueprints" lab.

ctx logger info "Packaging resources from ${resources_root} into ${resources_target}..."

mkdir -p ${resources_target}
tar -cvzf ${resources_target}/static-app.tar.gz --directory ${resources_root}/static-app .
