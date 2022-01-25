# image-processor

[![build status](https://gitlab.com/paulaolmedo/image-processor/badges/main/pipeline.svg)](https://gitlab.com/paulaolmedo/image-processor/-/commits/main)

# Running instructions
## image_processor core
	docker run --rm -it -v $(pwd):/home/project -w /home/project paulabeatrizolmedo/image-processor bash

Once inside the container, execute the entrypoint file, with the corresponding options (see entrypoint --help)

## image_processor with jupyter
	docker run --rm -it -v $(pwd):/home/project -w /home/project -p 8888:8888 -t paulabeatrizolmedo/ip-jupyter