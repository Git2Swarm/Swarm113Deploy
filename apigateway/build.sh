DOCKER_IMAGE=$(basename $(pwd))
docker build -t $DOCKER_IMAGE .
