#!/bin/bash

ACTION="$1"

if [ "$ACTION" == "stop" ]; 
then
	docker kill "myfrr"
	docker rm "myfrr"
elif [ "$ACTION" == "start" ];
then
	container=$(docker create --name "myfrr" -t --cap-add=all frrouting/frr:latest)
	docker cp vtysh.conf myfrr:/etc/frr/vtysh.conf
	docker cp daemons myfrr:/etc/frr/daemons
	docker cp bgpd.conf myfrr:/etc/frr/bgpd.conf
	docker start myfrr
	echo $container
else
	echo "Invalid action"
fi
