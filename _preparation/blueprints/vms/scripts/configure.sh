#!/bin/bash -e
ssh -i ${key_filename} ${user}@${host} "git clone -b ${labs_branch} ${labs_repo_url}"
scp -i ${key_filename} ${key_filename} ${user}@${host}:~/
