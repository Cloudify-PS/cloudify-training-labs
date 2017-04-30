#!/bin/bash -e

TMP_CLI=$(mktemp --tmpdir cli.XXXXX)
curl -J -o $TMP_CLI ${cli_rpm}
sudo yum install -y $TMP_CLI
rm -rf $TMP_CLI