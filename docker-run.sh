#!/bin/bash
DOCKER=$(which docker)
$DOCKER run --name honeypress -d -p 80:80 -v $(pwd)/logs:/var/log/nginx honeypress
