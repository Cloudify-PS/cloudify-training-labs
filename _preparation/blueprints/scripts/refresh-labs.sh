#!/bin/bash -e
# We download the file and then push it, rather than downloading the file directly from the CLI machine.
# Otherwise, credentials may be stored in the bash history on the CLI machine.
SSH_PARMS=(-i ${key_filename} -o "StrictHostKeyChecking no")
TEMP_LABS_ARCHIVE=/tmp/labs.tar.gz
ctx logger info "Downloading labs archive: ${labs_archive} -> ${TEMP_LABS_ARCHIVE}"
curl -L --user ${github_user}:${github_api_key} --output ${TEMP_LABS_ARCHIVE} ${labs_archive}
ctx logger info "Copying labs archive to remote machine"
scp "${SSH_PARMS[@]}" /tmp/labs.tar.gz ${user}@${host}:${TEMP_LABS_ARCHIVE}
ctx logger info "Extracting labs archive..."
ssh "${SSH_PARMS[@]}" ${user}@${host} "[ ! -f cloudify-training-labs ] || chmod -R u+w cloudify-training-labs"
ssh "${SSH_PARMS[@]}" ${user}@${host} "rm -rf cloudify-training-labs && mkdir cloudify-training-labs && cd cloudify-training-labs && tar -zxv --strip-components=1 -f ${TEMP_LABS_ARCHIVE}"
# Commented out until CFY-6724 is resolved.
# ssh "${SSH_PARMS[@]}" ${user}@${host} "chmod -R ugo-w cloudify-training-labs"
ctx logger info "Done."