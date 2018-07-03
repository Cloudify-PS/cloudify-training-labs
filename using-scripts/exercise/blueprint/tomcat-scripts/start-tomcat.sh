#!/bin/bash -e

tomcat_port=$(ctx node properties port)
ctx logger info "Tomcat port: ${tomcat_port}"

# args:
# $1 the error code of the last command (should be explicitly passed)
# $2 the message to print in case of an error
# 
# an error message is printed and the script exists with the provided error code
function error_exit {
	echo "$2 : error code: $1"
	exit ${1}
}

function get_response_code() {
    port=$1
    set +e
    response_code=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:${port})
    set -e
    echo ${response_code}
}

function wait_for_server() {
    port=$1
    started=false

    ctx logger info "Running liveness detection on port ${port}"

    for i in $(seq 1 12)
    do
        response_code=$(get_response_code ${port})
        ctx logger info "[GET] http://localhost:${port} returned response code ${response_code}"
        if [ ${response_code} -eq 200 ] ; then
            started=true
            break
        else
            ctx logger info "Server has not started; waiting for 5 seconds..."
            sleep 5
        fi
    done
    if [ ${started} = false ]; then
        ctx logger error "Server failed to start"
        exit 1
    fi
}

export JAVA_HOME=~/java
export PATH=${PATH}:${JAVA_HOME}/bin
export CLASSPATH=

tomcat_home=~/tomcat
ctx logger info "Starting Tomcat in ${tomcat_home}..."

command="${tomcat_home}/bin/catalina.sh run"
nohup ${command} > /dev/null 2>&1 &
PID=$!

wait_for_server ${tomcat_port}

# This runtime property is used by the stop-tomcat script for killing this tomcat instance.
# Make sure you use the same property name here and there.
REPLACE_WITH_A_COMMAND_THAT_STORES_THE_PROCESS_ID_IN_THE_RUNTIME_PROPERTIES_OF_THE_INSTANCE_VIA_THE_CONTEXT_OBJECT
