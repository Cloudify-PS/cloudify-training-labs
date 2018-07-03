#!/bin/bash -e
cd ~
nohup python -m SimpleHTTPServer 8080 > ~/http.out 2> ~/http.err &
