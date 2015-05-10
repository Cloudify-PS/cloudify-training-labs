#!/bin/bash

currHostName=`hostname`
currFilename=$(basename "$0")

ctx logger info "${currHostName}:${currFilename} Killing tomcat..."


PID=$(ctx instance runtime_properties pid)
kill -9 $PID

ctx logger info "${currHostName}:${currFilename} Successfully stopped tomcat (${PID})"


ctx logger info "${currHostName}:${currFilename} End of $0"
echo "End of $0"