#!/bin/bash -e
cd /home/centos
nohup python -m SimpleHTTPServer 8080 > ~/http.out 2> ~/http.err &
