#!/bin/sh
echo $1
if [ $# != 1 ] 
then
  echo "Usage: $0 <project name>"
  exit 1
fi

docker service  update --publish-add 7979:5000 ${1}_apigateway
echo http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):7979
