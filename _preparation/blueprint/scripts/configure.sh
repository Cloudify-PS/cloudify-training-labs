#!/bin/bash -e
ssh -i ${key_filename} -o "StrictHostKeyChecking no" ${user}@${host} "git clone -b ${labs_branch} ${labs_repo_url}"
scp -i ${key_filename} -o "StrictHostKeyChecking no" ${key_filename} ${user}@${host}:~/
