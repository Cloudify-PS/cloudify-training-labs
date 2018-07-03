#!/bin/bash -e

ctx logger info "Uninstalling app..."

target_dir=$(ctx instance runtime_properties target_dir)

ctx logger info "Deleting directory: $target_dir..."

# Not really executing any "rm -rf" command, in case the user happened to get the system
# to a point where `target_dir` is something ferociously wrong such as '/'.

ctx logger info "Done."
