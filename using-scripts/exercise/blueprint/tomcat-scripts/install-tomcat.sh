#!/bin/bash -e

download_path=$(ctx node properties download_path)
ctx logger info "Download path: ${download_path}"

java_url=$(ctx node properties java_url)
ctx logger info "Java URL: ${java_url}"

# args:
# $1 the error code of the last command (should be explicitly passed)
# $2 the message to print in case of an error
# 
# an error message is printed and the script exists with the provided error code
function error_exit {
	ctx logger info "Error encountered: error code = $1, message = $2"
	exit $1
}

# Args:
# $1: Download description
# $2: Download link
# $3: Directory to extract to

function download_and_extract {
    temp_archive=$(mktemp --suffix=.tar.gz)
	ctx logger info "Downloading $1 from $2 to ${temp_archive}..."
    curl --silent -k -o ${temp_archive} -O $2 || error_exit $? "Failed downloading $1"
    mkdir -p $3
    ctx logger info "Extracting ${temp_archive} to $3..."
    tar -C $3 -zxvf ${temp_archive} --strip-components=1
    rm -f ${temp_archive}
}

download_and_extract "Tomcat" ${download_path} ~/tomcat
download_and_extract "JDK" ${java_url} ~/java
