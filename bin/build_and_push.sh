#!/bin/bash -xe

PROJ_ROOT="$(dirname $(readlink -f "${BASH_SOURCE[0]}"))/.."
cd "${PROJ_ROOT}"

#aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin 775573995290.dkr.ecr.eu-west-1.amazonaws.com
docker build -t bi-dev-demoef55f8b60c2e4a5f846c20e930489b94 .
docker tag bi-dev-demoef55f8b60c2e4a5f846c20e930489b94:latest 775573995290.dkr.ecr.eu-west-1.amazonaws.com/bi-dev-demoef55f8b60c2e4a5f846c20e930489b94:latest
docker push 775573995290.dkr.ecr.eu-west-1.amazonaws.com/bi-dev-demoef55f8b60c2e4a5f846c20e930489b94:latest