#!/bin/bash

currHostName=`hostname`
currFilename=$(basename "$0")

tomcat_version=$(ctx node properties tomcat_version)
ctx logger info "${currHostName}:${currFilename} :tomcat_version ${tomcat_version}"

tomcatPort=$(ctx node properties port)
ctx logger info "${currHostName}:${currFilename} :tomcatPort ${tomcatPort}"

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

    curl_cmd=$(which curl)
    wget_cmd=$(which wget)

    if [[ ! -z ${curl_cmd} ]]; then
        response_code=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:${port})
    elif [[ ! -z ${wget_cmd} ]]; then
        response_code=$(wget --spider -S "http://localhost:${port}" 2>&1 | grep "HTTP/" | awk '{print $2}' | tail -1)
    else
        ctx logger error "Failed to retrieve response code from http://localhost:${port}: Neither 'curl' nor 'wget' were found on the system"
        exit 1;
    fi

    set -e

    echo ${response_code}

}

function wait_for_server() {

    port=$1
    server_name=$2

    started=false

    ctx logger info "Running ${server_name} liveness detection on port ${port}"

    for i in $(seq 1 360)
    do
        response_code=$(get_response_code ${port})
        ctx logger info "[GET] http://localhost:${port} ${response_code}"
        if [ ${response_code} -eq 200 ] ; then
            started=true
            break
        else
            ctx logger info "${server_name} has not started. waiting 5 seconds..."
            sleep 5
        fi
    done
    if [ ${started} = false ]; then
        ctx logger error "${server_name} failed to start. timeout ended."
        exit 1
    fi
}

export JAVA_HOME=~/java
export PATH=$PATH:/usr/sbin:/sbin:$JAVA_HOME/bin || error_exit $? "Failed on: export PATH=$PATH:/usr/sbin:/sbin"
export CLASSPATH=


tomcatHome=~/$tomcat_version
ctx logger info "${currHostName}:${currFilename} Starting Tomcat in ${tomcatHome}..."

COMMAND="$tomcatHome/bin/catalina.sh run"
nohup ${COMMAND} > /dev/null 2>&1 &
PID=$!


wait_for_server $tomcatPort 'tomcat'
# This runtime porperty is used by the stop-tomcat script for killing this tomcat instance.
ctx instance runtime_properties pid ${PID}


ctx logger info "${currHostName}:${currFilename} End of $0"
echo "End of $0"