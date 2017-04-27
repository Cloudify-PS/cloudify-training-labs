#!/bin/bash -e
# We download the file and then push it, rather than downloading the file directly from the CLI machine.
# Otherwise, credentials may be stored in the bash history on the CLI machine.
SSH_PARMS=(-i ${key_filename} -o "StrictHostKeyChecking no")
TEMP_LABS_ARCHIVE=$(mktemp --tmpdir labs.XXXXX)
#TEMP_NODECELLAR_ARCHIVE=$(mktemp --tmpdir nodecellar.XXXXX)
TEMP_PLUGIN_TEMPLATE_ARCHIVE=$(mktemp --tmpdir plugin-template.XXXXX)

ctx logger info "Downloading labs archive: ${labs_archive} -> ${TEMP_LABS_ARCHIVE}"
curl -L --user ${github_user}:${github_api_key} --output ${TEMP_LABS_ARCHIVE} ${labs_archive}

#ctx logger info "Downloading NodeCellar archive: ${nodecellar_archive} -> ${TEMP_NODECELLAR_ARCHIVE}"
#curl -L --user ${github_user}:${github_api_key} --output ${TEMP_NODECELLAR_ARCHIVE} ${nodecellar_archive}

ctx logger info "Downloading plugin template archive: ${plugin_template_archive} -> ${TEMP_PLUGIN_TEMPLATE_ARCHIVE}"
curl -L --user ${github_user}:${github_api_key} --output ${TEMP_PLUGIN_TEMPLATE_ARCHIVE} ${plugin_template_archive}

ctx logger info "Extracting labs archive..."
cat ${TEMP_LABS_ARCHIVE} | ssh "${SSH_PARMS[@]}" ${user}@${host} "rm -rf cloudify-training-labs; mkdir cloudify-training-labs; cd cloudify-training-labs; tar -zxv --strip-components=1"

#ctx logger info "Extracting NodeCellar archive..."
#cat ${TEMP_NODECELLAR_ARCHIVE} | ssh "${SSH_PARMS[@]}" ${user}@${host} "rm -rf nodecellar; mkdir nodecellar; cd nodecellar; tar -zxv --strip-components=1"

ctx logger info "Extracting plugin template archive..."
cat ${TEMP_PLUGIN_TEMPLATE_ARCHIVE} | ssh "${SSH_PARMS[@]}" ${user}@${host} "rm -rf plugin-template; mkdir plugin-template; cd plugin-template; tar -zxv --strip-components=1"

ctx logger info "Done."