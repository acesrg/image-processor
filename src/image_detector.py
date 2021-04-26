#
# Copyright (c) 2021 PAULA B. OLMEDO.
#
# This file is part of IMAGE_PROCESSOR
# (see https://github.com/paulaolmedo/image-processor).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.#
import os
import re
import time
import logging
import requests
import configparser
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from sentinel_scripts.src.rename_sentinel_files import RenameRaster


# esto habría que reescribirlo para que directamente tome el contenido de la clase image_processor
# cosa de que, al detectar una imagen, el eventhandler le diga a gitlab "tengo una nueva imagen" y arranque a hacer el comando del entry point
class EventHandler(FileSystemEventHandler):
    def on_created(self, event):
        regex = r"(.zip)"  # TODO parametrizar / agregar un regex que represente el zip de sentinel
        matches = re.finditer(regex, event.src_path)
        if matches:
            print("new raster found at: " + event.src_path)
            user_response = input("is this right? press y/n \n")

            if user_response == "y":
                logging.info(":)")
                rename_raster = RenameRaster(event.src_path)
                rename_raster.rename_raster_file()  #  archivo donde van a parar las imágenes nuevas pero no toy segura que vaya a usar la variable que devuelve

                # finalmente, disparo el pipeline
                properties = configparser.ConfigParser()
                properties.read('safo_impro/service/constants.ini')  #  mmm sacar esto de acá

                url = properties.get("ci_configuration", "url")
                token = properties.get("ci_configuration", "ci_token")

                payload = {'token': token}

                r = requests.post(url, params=payload)

                logging.info(r.text)

            else:
                logging.info(":(")
           

def image_daemon(server_path):
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    observer = Observer()
    event_handler = EventHandler()
    observer.schedule(event_handler, path=server_path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


# start the daemon process
server_path = 'test'
if os.path.isdir(server_path) is True:
    print('starting daemon')
    image_daemon(server_path)
else:
    print('server path not found')
