import sys
import os
import re
import argparse
import errno
import time
from PIL import Image
from multiprocessing import Pool
from multiprocessing import Value
import subprocess
import tempfile
from PIL import ImageOps
from PIL.ExifTags import TAGS

class State(object):
    def __init__(self):
        self.counter = Value('i', 0)
        self.start_ticks = Value('d', time.process_time())

    def increment(self, n=1):
        with self.counter.get_lock():
            self.counter.value += n

    @property
    def value(self):
        return self.counter.value

    @property
    def start(self):
        return self.start_ticks.value


def init(s, args):
    global state
    state = s
    state.eaDir = args.eaDir
    state.force = args.force


def main():
    args = parse_args()
    state = State()

    files = find_files(args.directory)

    cores = os.cpu_count()
    half_cores = cores // 2
    parallel = max(4, half_cores)

    with Pool(processes=parallel, initializer=init, initargs=(state, args)) as pool:
        pool.map(process_file, files)

    print("{0} files processed in total.".format(state.value))


def parse_args():
    parser = argparse.ArgumentParser(
        description="Create thumbnails for Synology Photo Station.")
    parser.add_argument('-d', "--directory", required=True,
                        help="Directory to generate thumbnails for. "
                             "Subdirectories will always be processed.")
    parser.add_argument("-e", "--eaDir", required=False, default=False, action="store_true",
                        help="write directly to @eaDir rather than eaDir_tmp")
    parser.add_argument("-f", "--force", required=False, default=False, action="store_true",)

    return parser.parse_args()


def find_files(dir):
    valid_exts = ('jpeg', 'jpg', 'bmp', 'gif', 'png', 'avi', 'mp4', 'mov', 'm4v')
    valid_exts_re = "|".join(
        map((lambda ext: ".*\\.{0}$".format(ext)), valid_exts))

    for root, dirs, files in os.walk(dir):
        for name in files:
            if re.match(valid_exts_re, name, re.IGNORECASE) \
                    and not name.startswith('SYNOPHOTO_THUMB'):
                yield os.path.join(root, name)


def print_progress():
    global state
    state.increment(1)
    processed = state.value
    if processed % 10 == 0:
        print("{0} files processed so far, averaging {1:.2f} files per second."
              .format(processed, float(processed) /
                                 (float(time.process_time() - state.start))))


def process_file(file_path):
    global state
    print(file_path)

    (dir, filename) = os.path.split(file_path)
    
    if (state.eaDir):
        thumb_dir = os.path.join(dir, '@eaDir', filename)
    else:
        thumb_dir = os.path.join(dir, 'eaDir_tmp', filename)
    ensure_directory_exists(thumb_dir)

    create_thumbnails(file_path, thumb_dir)

    print_progress()


def ensure_directory_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def create_thumbnails(source_path, dest_dir):
    global state
    to_generate = (('SYNOPHOTO_THUMB_XL.jpg', 1280),
                   ('SYNOPHOTO_THUMB_B.jpg', 640),
                   ('SYNOPHOTO_THUMB_M.jpg', 320),
                   ('SYNOPHOTO_THUMB_PREVIEW.jpg', 160),
                   ('SYNOPHOTO_THUMB_S.jpg', 120))

    skip_this = True
    if state.force:
        skip_this = False
    else:
        for thumb in to_generate:
            if os.path.exists(os.path.join(dest_dir, thumb[0])):
                continue
            else:
                skip_all = False
                break

    if skip_this:
        return

    spath_low = source_path.lower()
    video_ext = ('avi', 'mp4', 'mov', 'm4v') 
    snapshot_file = False

    try:
        if (spath_low.endswith(video_ext)):
            temp_name = next(tempfile._get_candidate_names())
            snapshot_file=os.path.join(dest_dir, temp_name + ".jpg")
            subprocess.call(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-i', source_path, '-ss', '00:00:00.000', '-vframes', '1', snapshot_file])
            im = Image.open(snapshot_file)
        else:
            im = Image.open(source_path)
    except Exception as e:
        print(e)
        return

    try:
        exif = im._getexif()
        image = ImageOps.exif_transpose(im)
        im = image
    except Exception as e:
        print(e)



    for thumb in to_generate:
        if not state.force:
            if os.path.exists(os.path.join(dest_dir, thumb[0])):
                continue

        try:
            im.thumbnail((thumb[1], thumb[1]), Image.ANTIALIAS)
            im.save(os.path.join(dest_dir, thumb[0]))
        except Exception as e:
            print(e)

    if snapshot_file:
        os.remove(snapshot_file)


if __name__ == "__main__":
    sys.exit(main())
