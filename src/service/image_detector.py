import os
import re
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from support import Support
from normalized_indexes import NormalizedDifferenceIndex

from inotify_simple import INotify, flags


class EventHandler(FileSystemEventHandler):
    def on_created(self, event): #detecta cada una de las carpetas interiores ??????
        #regex = r"(MSIL1C_)(\d{8})(\/)(IMG_DATA)$"  # detecta la carpeta una vez que pasa por el proceso de renombrado. es exclusivo de los de sentinel leider     
        regex = r"(.tif)|(.jp2)"  # TODO parametrizar
        matches = re.finditer(regex, event.src_path)
        images_path = ''

        inotify = INotify()


        for match in matches:
            images_path = os.path.dirname(event.src_path) + '/'
            img = os.path.basename(event.src_path)
            timout_s = 10
            timed_out = False
            start_ts = time.monotonic()
                
            wd = inotify.add_watch(images_path, watch_flags)
            watch_flags = flags.CLOSE_WRITE

            print('toy acá')
            inotify.read()
            print("written " + img)

        print('no hay matches todavía sorry bro')
            
            #while not timed_out:
            #    try:
            #        with open(img, 'w') as f:
            #            #s = f.read()
                        #print('read this bytes ' + len(s))
            #            print("todo ok para " + img)
            #            break
            #    except IOError as e:
            #            print('error ', e.errno, ',', e.strerror)

            #    if (time.monotonic() - start_ts) > timout_s:
            #        timed_out = True
        
        #if os.path.isdir(images_path):
            #red_exists = os.path.isfile(images_path + 'red_665_10.jp2')
            #nir_exists = os.path.isfile(images_path + 'nir4_832_10.jp2')
            #img 
            #try:
                #with open(images_path + 'red_665_10.jp2', 'rw') as f:
                    #print("todo ok para " + images_path + 'red_665_10.jp2')

            #if red_exists and nir_exists:
                #print("starting norm indexes calculation process...")
                #ni = NormalizedDifferenceIndex(images_path, 'sentinel')
                #ni.calculate_ndvi()

                #print("starting crop process...")
                #support = Support()
                #support.crop_process(images_path, 'ndvi.tif', data_path, '/places.json')

        
            

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
image_daemon('file_folder')
