# To make this program work automatically, we need a watchdog. 
# Watchdog is a Python API library used to monitor file system events. 
# The command 'pip3 install watchdog' allows us to do this

# importing relevant libraries
from os import scandir, rename
from os.path import splitext, exists, join
from shutil import move
from time import sleep

import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# Declare a source directory. In this case, my downloads folder
source_dir = "/Users/adriancortez/Downloads"
# Declare destination directories for where the downloads will go (can be any destination, mine are here for example)
dest_dir_images = "/Users/adriancortez/Desktop/Media/screenshots"
dest_dir_videos = "/Users/adriancortez/Desktop/Media/videos"
dest_dir_sfx = "/Users/adriancortez/Desktop/Media/SFX"
dest_dir_wallpapers = "/users/adriancortez/Desktop/Media/Wallpapers"
 # I happened to have many labs in my download folder
dest_dir_labs330 = "/Users/adriancortez/Desktop/Olivet Nazarene University/Sophomore Year/Spring 2024/COMP 330 - Web Dev"
# folder for unsorted files
dest_dir_unsorted = "/Users/adriancortez/Desktop/Other Documents/Unsorted/Other"
dest_dir_unsortedDocuments = "/Users/adriancortez/Desktop/Other Documents/Unsorted/Document Files"

# function that moves the file. If such file exists already, ir renames it.
def move_file(dest, entry, name):
    if exists(f"{dest}/{name}"):
        unique_name = make_unique(dest, name)
        oldName = join(dest, name)
        newName = join(dest, unique_name)
        rename(oldName, newName)
    move(entry.path, dest)

# function that creates a unique file name
def make_unique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    # * IF FILE EXISTS, ADDS NUMBER TO THE END OF THE FILENAME
    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1

    return name


class MoverHandler(FileSystemEventHandler):
    def on_modified(self, event):
        # 'with' block ensures files are properly closed after the block is executed
        # 'scandir' is a directory-listing function that returns an iterator of all the objects in a directory including file attribute information
        # 'entries' is a list of the files in the source directory
        with scandir(source_dir) as entries: 
            for entry in entries:
                fileName = entry.name
                dest = source_dir
                if fileName.endswith('.jpg') or fileName.endswith('.jpeg') or fileName.endswith('.png') or fileName.endswith('.img'):
                    if "unsplash" in fileName: # all of my wallpapers include this string when downloaded
                        dest = dest_dir_wallpapers
                    else:
                        dest = dest_dir_images
                    logging.info(f"Moved image file: {fileName}")
                elif fileName.endswith('.mov') or fileName.endswith('.mp4'):
                    dest = dest_dir_videos
                    logging.info(f"Moved video file: {fileName}")
                elif fileName.endswith('.wav') or fileName.endswith('.mp3'):
                    dest = dest_dir_sfx
                    logging.info(f"Moved SFX file: {fileName}")
                elif "LAB_" in fileName:
                    dest = dest_dir_labs330
                    logging.info(f"Moved lab file: {fileName}")
                elif fileName.endswith('.docx'):
                    dest = dest_dir_unsortedDocuments
                else:
                    dest = dest_dir_unsorted
                    logging.info(f"Moved file: {fileName}")

                # move the file to the chosen directory
                move_file(dest, entry, fileName)



# Watchdog event handler. Whenever there is a change in the source directory, the 'on modified' function is fired
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()