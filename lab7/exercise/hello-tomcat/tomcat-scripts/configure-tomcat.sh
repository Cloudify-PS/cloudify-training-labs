#!/bin/bash -x

currHostName=`hostname`
currFilename=$(basename "$0")

newPort=$(ctx node properties port)
ctx logger info "${currHostName}:${currFilename} :newPort ${port}"

war_url=$(ctx node properties war_url)
ctx logger info "${currHostName}:${currFilename} :war_url ${war_url}"

war_filename=$(ctx node properties war_filename)
ctx logger info "${currHostName}:${currFilename} :war_filename ${war_filename}"

tomcat_version=$(ctx node properties tomcat_version)
ctx logger info "${currHostName}:${currFilename} :tomcat_version ${tomcat_version}"

application_name=$(ctx node properties application_name)
ctx logger info "${currHostName}:${currFilename} :application_name ${application_name}"

if [ -f /usr/bin/wget ]; then
	DOWNLOADER="wget"
elif [ -f /usr/bin/curl ]; then
	DOWNLOADER="curl"
fi

ctx logger info "${currHostName}:${currFilename} :DOWNLOADER ${DOWNLOADER}"

# args:
# $1 the error code of the last command (should be explicitly passed)
# $2 the message to print in case of an error
# 
# an error message is printed and the script exists with the provided error code
function error_exit {
	ctx logger info "${currHostName}:${currFilename} $2 : error code: $1"
	exit $1
}

# args:
# $1 download description.
# $2 download link.
# $3 output file.
function download {
	ctx logger info "${currHostName}:${currFilename} Downloading $1 from $2 ..."
	if [ "$DOWNLOADER" == "wget" ];then
		Q_FLAG="--no-check-certificate -q"
		O_FLAG="-O" 
		LINK_FLAG=""
	elif [ "$DOWNLOADER" == "curl" ];then
		Q_FLAG="--silent"
		O_FLAG="-o"
		LINK_FLAG="-O"
	fi
	ctx logger info "${currHostName}:${currFilename} $DOWNLOADER $Q_FLAG $O_FLAG $3 $LINK_FLAG $2" 
	$DOWNLOADER $Q_FLAG $O_FLAG $3 $LINK_FLAG $2 || error_exit $? "Failed downloading $1"
}

tomcatHome=~/$tomcat_version
applicationWar=$tomcatHome/$war_filename
tomcatConfFolder=$tomcatHome/conf
serverXml=$tomcatConfFolder/server.xml
tomcatContextPathFolder=$tomcatConfFolder/Catalina/localhost
tomcatContextFile=$tomcatContextPathFolder/$application_name.xml


ctx logger info "${currHostName}:${currFilename} tomcatHome is ${tomcatHome}"
ctx logger info "${currHostName}:${currFilename} applicationWar is ${applicationWar}"
ctx logger info "${currHostName}:${currFilename} tomcatContextPathFolder is ${tomcatContextPathFolder}"
ctx logger info "${currHostName}:${currFilename} tomcatContextFile is ${tomcatContextFile}"

download "WarFile" $war_url $applicationWar

mkdir -p $tomcatContextPathFolder

# Write the context configuration
rm -f $tomcatContextFile
echo "<Context docBase=\"${applicationWar}\" />" > $tomcatContextFile

ctx logger info "${currHostName}:${currFilename} Replacing 8080 with ${newPort} in $serverXml"
sed -i -e "s/port=\"8080\"/port=\"$newPort\"/g" $serverXml


ctx logger info "${currHostName}:${currFilename} End of $0"
echo "End of $0"




