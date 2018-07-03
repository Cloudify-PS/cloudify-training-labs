#!/bin/bash -e

SSH_PARMS=(-i ${key_filename} -o "StrictHostKeyChecking no")

ssh "${SSH_PARMS[@]}" ${user}@${host} "curl -J -o /tmp/cfy-cli.rpm ${cli_rpm}"
ssh "${SSH_PARMS[@]}" ${user}@${host} "sudo yum -y install /tmp/cfy-cli.rpm"
ssh "${SSH_PARMS[@]}" ${user}@${host} "rm -rf /tmp/cfy-cli.rpm"
