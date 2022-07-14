# Image processor 🛰️

[![build status](https://gitlab.com/paulaolmedo/image-processor/badges/main/pipeline.svg)](https://gitlab.com/paulaolmedo/image-processor/-/commits/main)

# Before running

This module is mainly intented to process Sentinel-2 images. To work easily, the raster layers were pre-processed to have a human-readable names. Because of that, before working with this API please check [Sentinel Scrips](https://gitlab.com/satellite-forecast/sentinel-scripts) to clean the raster.

# Running instructions
## image_processor core
	docker run --rm -it -v $(pwd):/home/project -w /home/project paulabeatrizolmedo/image-processor bash

Once inside the container, execute the entrypoint file, with the corresponding options (see **entrypoint --help**)

## image_processor with jupyter
	docker run --rm -it -v $(pwd):/home/project -w /home/project -p 8888:8888 -t paulabeatrizolmedo/ip-jupyter
