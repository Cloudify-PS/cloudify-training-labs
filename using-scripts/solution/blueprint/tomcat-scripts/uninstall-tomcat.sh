#!/bin/bash -e

tomcat_home=~/tomcat
ctx logger info "Removing ${tomcat_home}..."
rm -rf ${tomcat_home}

java_home=~/java
ctx logger info "Removing ${java_home}..."
rm -rf ${java_home}
