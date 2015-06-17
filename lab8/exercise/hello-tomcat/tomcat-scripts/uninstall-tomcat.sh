#!/bin/bash

currHostName=`hostname`
currFilename=$(basename "$0")

tomcat_version=$(ctx node properties tomcat_version)
ctx logger info "${currHostName}:${currFilename} :tomcat_version ${tomcat_version}"

installDir=~/installDir
ctx logger info "${currHostName}:${currFilename} Removing $[installDir}... "
rm -rf $installDir

tomcatHome=~/$tomcat_version
ctx logger info "${currHostName}:${currFilename} Removing ${tomcatHome} ..."
rm -rf $tomcatHome

export JAVA_HOME=~/java
ctx logger info "${currHostName}:${currFilename} Removing ${JAVA_HOME} ..."
rm -rf $JAVA_HOME


ctx logger info "${currHostName}:${currFilename} End of $0"
echo "End of $0"




