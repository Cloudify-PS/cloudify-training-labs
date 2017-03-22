#!/bin/bash -e

url=$(ctx node properties url)
target_dir=$(mktemp -d --tmpdir my-app.XXXXX)

ctx instance runtime_properties target_dir $target_dir

temp_file=$(mktemp --tmpdir static-appXXX.zip)

ctx logger info "Installing application: downloading from $url into $temp_file..."
curl -J -o $temp_file $url

ctx logger info "Creating directory: $target_dir"
mkdir -p $target_dir

ctx logger info "Unzipping app into $target_dir"
unzip $temp_file -d $target_dir

ctx logger info "Done"