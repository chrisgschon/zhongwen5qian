#!/bin/sh

# start a neo4j docker container with apoc and bloom (server variant) configured
# this requires to have
# * curl, unzip and jq being installed
# * having a valid bloom license file

# released under the WTFPL (http://www.wtfpl.net/)
# (c) Stefan Armbruster

NEO4J_VERSION=3.5.7
APOC_VERSIONS_JSON=https://raw.githubusercontent.com/neo4j-contrib/neo4j-apoc-procedures/master/versions.json
BLOOM_VERSION=1.1.1
BLOOM_LICENSE_FILE=bloom-plugin.license
NEO4J_PASSWORD=123

[ -d plugins ] || mkdir plugins
[ -d plugins ] || mkdir data

cp "${BLOOM_LICENSE_FILE}" plugins/bloom-plugin.license
cd plugins

# download apoc if not yet there. 
# note: we need to follow redirects and want to use orig filename
# gotcha: if you have a non-matching version of apoc, this will *not* fail.
if ! ls apoc-*-all.jar 1> /dev/null 2>&1; then
	# resolve correct apoc version 
	APOC_URL=`curl -s $APOC_VERSIONS_JSON | jq -r ".[] | select (.neo4j == \"$NEO4J_VERSION\") | [.jar] | first"`
	#echo $APOC_URL
	curl -L -C - -O -J "$APOC_URL"
fi 

# download bloom plugin and extract it
if [ ! -f bloom-plugin-${BLOOM_VERSION}.jar ]; then
	curl -C - -O -J "https://neo4j.com/artifact.php?name=neo4j-bloom-${BLOOM_VERSION}.zip"
	unzip neo4j-bloom-${BLOOM_VERSION}.zip "*jar"
fi
cd ..

docker run \
--rm \
-e NEO4J_AUTH=neo4j/${NEO4J_PASSWORD} \
-e NEO4J_ACCEPT_LICENSE_AGREEMENT=yes \
-e NEO4J_apoc_import_file_enabled=true \
-e NEO4J_dbms_security_procedures_unrestricted=apoc.\\\*,bloom.\\\* \
-e NEO4J_neo4j_bloom_license__file=/plugins/bloom-plugin.license \
-e NEO4J_dbms_unmanaged__extension__classes=com.neo4j.bloom.server=/browser/bloom \
-e NEO4J_neo4j_bloom_authorization__role=admin,architect \
-v "$PWD/plugins":/plugins \
-p 7474:7474 \
-p 7687:7687 \
-v "$PWD/data":/data \
-v "$PWD/import":/var/lib/neo4j/import \
--user=$(id -u):$(id -g) \
--name=neo4jbloom \
neo4j:${NEO4J_VERSION}-enterprise