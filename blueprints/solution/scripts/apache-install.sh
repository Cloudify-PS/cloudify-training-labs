#!/bin/bash -e

listening_port=$(ctx node properties listener_port)
ctx logger info "Installing Apache; listening port is $listening_port"
