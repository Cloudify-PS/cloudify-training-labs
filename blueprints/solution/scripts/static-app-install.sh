#!/bin/bash -e

web_page_path=$(ctx node properties web_page)

ctx logger info "Downloading blueprint resource ${web_page_path}"
web_page=$(ctx download-resource ${web_page_path})
ctx logger info "Resource downloaded into ${web_page}"

target_dir=$(mktemp -d --tmpdir my-app.XXXXX)
ctx instance runtime_properties target_dir ${target_dir}

ctx logger info "Creating directory: ${target_dir}"
mkdir -p ${target_dir}

ctx logger info "Moving app into ${target_dir}"
mv web_page ${target_dir}

ctx logger info "Done"
