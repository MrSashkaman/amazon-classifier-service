#!/bin/bash

docker stop {{  docker_image  }}-app
docker rm {{  docker_image  }}-app
docker rmi {{  docker_image  }}

