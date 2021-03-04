# image-processor

[![Build Status](https://travis-ci.com/paulaolmedo/image-processor.svg?token=bqY7JHfPDqjwZn2ypbwq&branch=dev)](https://travis-ci.com/paulaolmedo/image-processor)

## to build the docker image
	docker build -f .ci/Dockerfile  -t [some-useful-tag] .
## and then run it...
	docker run --rm -it -v $(pwd):/home/project -w /home/project -t [some-useful-tag] bash