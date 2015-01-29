#!/bin/bash

currHostName=`hostname`
currFilename=$(basename "$0")

newPort=$(ctx node properties port)
ctx logger info "${currHostName}:${currFilename} :newPort ${newPort}"

download_path=$(ctx node properties download_path)
ctx logger info "${currHostName}:${currFilename} :download_path ${download_path}"

tomcat_version=$(ctx node properties tomcat_version)
ctx logger info "${currHostName}:${currFilename} :tomcat_version ${tomcat_version}"

application_name=$(ctx node properties application_name)
ctx logger info "${currHostName}:${currFilename} :application_name ${application_name}"

java_url=$(ctx node properties java_url)
ctx logger info "${currHostName}:${currFilename} :java_url ${java_url}"

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


installDir=~/installDir
zipName=tomcat.zip
destZip=$installDir/$zipName

mkdir -p $installDir
ctx logger info "${currHostName}:${currFilename} Wgetting ${download_path} to ${destZip} ..."
download "tomcat" $download_path $destZip

type unzip
retVal=$?
ctx logger info "${currHostName}:${currFilename} :type unzip return value is ${retVal}..."
if [ $retVal -ne 0 ]; then
  ctx logger info "${currHostName}:${currFilename} :Apt-getting unzip ..."
  sudo apt-get install -y -q unzip
  ctx logger info "${currHostName}:${currFilename} :Apt-got unzip ..."
fi

tomcatHome=~/$tomcat_version

ctx logger info "${currHostName}:${currFilename} Unzipping ${destZip} to ${tomcatHome}/ ..."
unzip $destZip -d ~/
chmod +x $tomcatHome/bin/*.sh

download "JDK" $java_url ~/java.bin
ctx logger info "${currHostName}:${currFilename} Chmodding ~/java.bin ..."
chmod +x ~/java.bin
echo -e "\n" > ~/input.txt
rm -rf ~/java || error_exit $? 102 "Failed removing old java installation directory"
mkdir ~/java
cd ~/java
	
ctx logger info "Installing JDK ..."
~/java.bin < ~/input.txt > /dev/null
mv ~/java/*/* ~/java || error_exit $? "Failed moving JDK installation"
rm -f ~/input.txt
export JAVA_HOME=~/java
rm -f ~/java.bin || error_exit $? "Failed deleting java.bin from home directory"

myPublicIP=$1
ctx logger info "${currHostName}:${currFilename} :myPublicIP ${myPublicIP}"

application_url=${myPublicIP}:${newPort}/${application_name}
ctx logger info "${currHostName}:${currFilename} :application_url ${application_url}"

ctx instance runtime_properties application_url ${application_url}



ctx logger info "${currHostName}:${currFilename} End of $0"
echo "End of $0"




