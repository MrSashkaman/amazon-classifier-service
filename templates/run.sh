#!/bin/bash

docker build -t {{  docker_image  }} --target prod .
docker run -d --name {{  docker_image  }}-app -p {{  app_port  }}:80 {{  docker_image  }}
