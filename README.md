# Thumbnail Generator for Synology Photos

Creating thumbnails on the consumer level DiskStation NAS boxes by Synology is incredibly slow which makes indexing large photo collections take forever to complete. It's much, much faster (days -> hours) to generate the thumbnails on your desktop computer over e.g. SMB using this small Python script.

## Requirements

- [Pillow imaing library](https://pypi.python.org/pypi/Pillow)
- [Python 3](https://www.python.org/downloads/)

## Installation

Install [Python 3](https://www.python.org/downloads/) onto your machine and then open a terminal so that you can install the [Pillow](https://pypi.python.org/pypi/Pillow). You can use the following command to install it: `pip install Pillow`

## Usage

```bash
# Run the following command in your terminal. Path is the path to the folder you want to generate thumbnails for
python3 dsthumbgen.py --directory <path>

# Example on Windows
python3 dsthumbgen.py --directory C:\Photos\
```

## Good to know

Given a file and folder structure like below:

```text
C:\Photos\001.jpg
C:\Photos\dir1\002.jpg
```

...the utility will create the following:

```text
C:\Photos\eaDir_tmp\001.jpg\SYNOPHOTO_THUMB_XL.jpg
C:\Photos\eaDir_tmp\001.jpg\SYNOPHOTO_THUMB_B.jpg
C:\Photos\eaDir_tmp\001.jpg\SYNOPHOTO_THUMB_M.jpg
C:\Photos\eaDir_tmp\001.jpg\SYNOPHOTO_THUMB_PREVIEW.jpg
C:\Photos\eaDir_tmp\001.jpg\SYNOPHOTO_THUMB_S.jpg
C:\Photos\dir1\eaDir_tmp\002.jpg\SYNOPHOTO_THUMB_XL.jpg
C:\Photos\dir1\eaDir_tmp\002.jpg\SYNOPHOTO_THUMB_B.jpg
C:\Photos\dir1\eaDir_tmp\002.jpg\SYNOPHOTO_THUMB_M.jpg
C:\Photos\dir1\eaDir_tmp\002.jpg\SYNOPHOTO_THUMB_PREVIEW.jpg
C:\Photos\dir1\eaDir_tmp\002.jpg\SYNOPHOTO_THUMB_S.jpg
```

`eaDir_tmp` is used as a temporary directory name as @ characters are not valid in file names on Windows. Therefore these folders must be renamed to `@eaDir` for PhotoStation to recognize them. This renaming process must be done via SSH to the DiskStation unless the volume is mounted by NFS. Useful commands:

```bash
# Remove any existing thumbnail directories, dry-run check print out before running next command!
find . -depth -type d -name 'eaDir_tmp' -execdir echo '{}' \;

# Remove any existing thumbnail directories
find . -depth -type d -name 'eaDir_tmp' -execdir rm -rf '{}' \;

# Rename directories
find . -depth -type d -name 'eaDir_tmp' -execdir mv '{}' @eaDir \;
```
