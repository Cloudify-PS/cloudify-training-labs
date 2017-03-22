#!/bin/bash -e

# Create resources for "blueprints" lab.

ctx logger info "Packaging resources from ${resources_root} into ${resources_target}..."

mkdir -p ${resources_target}
cd ${resources_root}/static-app && zip -r ${resources_target}/static-app.zip .

