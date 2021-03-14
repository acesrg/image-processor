import os
import re
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from support import Support
from normalized_indexes import NormalizedDifferenceIndex

from inotify_simple import INotify, flags


class EventHandler(FileSystemEventHandler):
    def on_created(self, event):
        regex = r"(.tif)|(.jp2)"  # TODO parametrizar
        matches = re.finditer(regex, event.src_path)
        images_path = ''

        inotify = INotify()

        print("listening to " + event.src_path)

        for match in matches:
            print("match found")
            images_path = os.path.dirname(event.src_path) + '/'
            img = os.path.basename(event.src_path)

            watch_flags = flags.CLOSE_WRITE
            wd = inotify.add_watch(images_path, watch_flags) # noqa

            inotify.read()  # bloquea el resto de los procesos hasta que se cierre la escritura del archivo que se está copiando
            print('copied: ' + img)

        red_exists = os.path.isfile(images_path + 'red_665_10.jp2')
        nir_exists = os.path.isfile(images_path + 'nir4_832_10.jp2')

        if red_exists and nir_exists:
            ni = NormalizedDifferenceIndex(images_path, 'sentinel')
            print("starting ndvi calculation process...")
            ni.write_ndvi_image()

            support = Support()

            src_name = 'ndvi.tif'
            original_image = images_path + src_name
            reprojected_image = images_path + 'reprojected-' + src_name

            print("starting reprojection process...")
            support.reprojection('EPSG:4326', original_image, reprojected_image)

            print("starting cropping process...")
            support.crop_process(images_path, 'reprojected-' + src_name, images_path, '/graticules', "ISO8859-1")

            print("returning to detection process")


def image_daemon(server_path):
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
