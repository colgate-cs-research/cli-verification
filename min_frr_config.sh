#!/bin/bash

#Script to start frr docker container (current v8.3.1)

ACTION="$1"

if [ "$ACTION" == "stop" ]; 
then
	docker kill "myfrr"
	docker rm "myfrr"
elif [ "$ACTION" == "start" ];
then
	container=$(docker create --name "myfrr" -t --cap-add=all frrouting/frr:v8.3.1)
	docker cp config_files/vtysh.conf myfrr:/etc/frr/vtysh.conf
	docker cp config_files/daemons myfrr:/etc/frr/daemons
	docker cp config_files/bgpd.conf myfrr:/etc/frr/bgpd.conf
	docker start myfrr
	echo $container
else
	echo "Invalid action"
fi
