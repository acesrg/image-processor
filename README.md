# image-processor

[![build status](https://gitlab.com/paulaolmedo/image-processor/badges/main/pipeline.svg)](https://gitlab.com/paulaolmedo/image-processor/-/commits/main)

## to build the docker image
	docker build -f .ci/Dockerfile.original -t [some-useful-tag] .
## and then run it...
	docker run --rm -it -v $(pwd):/home/project -w /home/project -t [some-useful-tag] bash
