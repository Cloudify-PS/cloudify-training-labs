#!/bin/bash -e

new_port=$(ctx node properties port)
REPLACE_WITH_A_COMMAND_THAT_WRITES_THE_TOMCAT_PORT_TO_THE_LOG_VIA_THE_CONTEXT_OBJECT

war_url=$(ctx node properties war_url)
ctx logger info "war_url: ${war_url}"

war_filename=$(ctx node properties war_filename)
ctx logger info "war_filename: ${war_filename}"

application_name=$(ctx node properties application_name)
ctx logger info "application_name: ${application_name}"

# args:
# $1 the error code of the last command (should be explicitly passed)
# $2 the message to print in case of an error
# 
# an error message is printed and the script exists with the provided error code
function error_exit {
	ctx logger info "Error encountered: error code = $1, message = $2"
	exit $1
}

tomcat_home=~/tomcat
application_war=${tomcat_home}/${war_filename}
tomcat_conf_dir=${tomcat_home}/conf
server_xml_file=${tomcat_conf_dir}/server.xml
tomcat_context_path_dir=${tomcat_conf_dir}/Catalina/localhost
tomcat_context_file=${tomcat_context_path_dir}/${application_name}.xml

ctx logger info "Tomcat home: ${tomcat_home}"
ctx logger info "Application WAR: ${application_war}"
ctx logger info "Tomcat context path directory: ${tomcat_context_path_dir}"
ctx logger info "Tomcat context file: ${tomcat_context_file}"

mkdir -p ${tomcat_home}
curl --silent -k -o ${application_war} -O ${war_url} || error_exit $? "Failed downloading $1"

mkdir -p ${tomcat_context_path_dir}

# Write the context configuration
rm -f ${tomcat_context_file}

cat << EOF > ${tomcat_context_file}
<Context docBase="${application_war}" />
EOF

ctx logger info "Replacing 8080 with ${new_port} in ${server_xml_file}"
sed -i -e "s/port=\"8080\"/port=\"${new_port}\"/g" ${server_xml_file}

public_ip=$1
ctx logger info "Public IP: ${public_ip}"

application_url=${public_ip}:${new_port}/${application_name}/
ctx logger info "Application URL: ${application_url}"

REPLACE_WITH_A_COMMAND_THAT_STORES_THE_APPLICATION_URL_IN_THE_RUNTIME_PROPERTIES_OF_THE_INSTANCE_VIA_THE_CONTEXT_OBJECT
