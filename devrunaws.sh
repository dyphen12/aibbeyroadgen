#!/bin/bash
app="aibbeyroad.docker"
docker build -t ${app} .
docker run  -e AWS_ACCESS_KEY_ID=your-access-key-id \
  -e AWS_SECRET_ACCESS_KEY=your-secret-access-key \
  -e AWS_DEFAULT_REGION=your-default-region \
  -d -p 56733:80 \
  --name=${app} \
  -v $PWD:/app ${app}
