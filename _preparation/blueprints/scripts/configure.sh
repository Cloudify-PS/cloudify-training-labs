#!/bin/bash -e
# We download the file and then push it, rather than downloading the file directly from the CLI machine.
# Otherwise, credentials may be stored in the bash history on the CLI machine.
SSH_PARMS=(-i ${key_filename} -o "StrictHostKeyChecking no")
ctx logger info "Copying key file (${key_filename}) to remote machine..."
scp "${SSH_PARMS[@]}" ${key_filename} ${user}@${host}:~/
key_file_basename=$(basename ${key_filename})
ssh "${SSH_PARMS[@]}" ${user}@${host} "chmod 600 ${key_file_basename}"
ctx logger info "Done."
