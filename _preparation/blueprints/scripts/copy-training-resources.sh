#!/bin/bash -e

SSH_PARMS=(-i ${key_filename} -o "StrictHostKeyChecking no")
ctx logger info "Copying key file (${key_filename}) to remote machine..."
scp "${SSH_PARMS[@]}" ${key_filename} ${user}@${host}:~/
ctx logger info "Done."
