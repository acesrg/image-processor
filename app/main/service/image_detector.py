import os
import re
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from support import Support


class EventHandler(FileSystemEventHandler):
    def on_created(self, event):
        regex = r"(.tif)|(.jp2)"  # TODO parametrizar
        matches = re.finditer(regex, event.src_path)
        for match in matches:
            images_path = os.path.dirname(event.src_path)
            src_name = os.path.basename(event.src_path)
            print("new image found at: ", images_path)
            print("filename: ", src_name)

            print("start cropping process...")
            support = Support()
            support.crop_process(images_path, src_name, images_path, '/places.json')


def image_daemon(server_path):
    observer = Observer()
    event_handler = EventHandler()
    observer.schedule(event_handler, path=server_path)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


# start the daemon process
image_daemon('/server_path_where_the_images_are_stored')
