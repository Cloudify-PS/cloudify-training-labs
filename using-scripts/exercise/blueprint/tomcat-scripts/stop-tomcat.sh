#!/bin/bash -e

ctx logger info "Killing tomcat..."

PID=$(ctx instance runtime_properties pid)
kill -9 $PID

ctx logger info "Successfully stopped tomcat (process ID: ${PID})"
