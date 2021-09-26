# Thumbnail Generator for Synology PhotoStation
Creating thumbnails on the consumer level DiskStation NAS boxes by Synology is incredibly slow which makes indexing of large photo collections take forever to complete. It's much, much faster (days -> hours) to generate the thumbnails on your desktop computer over e.g. SMB using this small Python script.

## Usage
`python dsthumbgen.py --directory <path>`

Example: `python dsthumbgen.py --directory c:\photos`

Subdirectories will always be processed.

## Requirements
The script needs the [Pillow imaing library](https://pypi.python.org/pypi/Pillow) to be installed.

## Good to know
Given a file and folder structure like below:

```
c:\photos\001.jpg
c:\photos\dir1\002.jpg
```

...the utility will create the following:

```
c:\photos\eaDir_tmp\001.jpg\SYNOPHOTO_THUMB_XL.jpg
c:\photos\eaDir_tmp\001.jpg\SYNOPHOTO_THUMB_B.jpg
c:\photos\eaDir_tmp\001.jpg\SYNOPHOTO_THUMB_M.jpg
c:\photos\eaDir_tmp\001.jpg\SYNOPHOTO_THUMB_PREVIEW.jpg
c:\photos\eaDir_tmp\001.jpg\SYNOPHOTO_THUMB_S.jpg
c:\photos\dir1\eaDir_tmp\002.jpg\SYNOPHOTO_THUMB_XL.jpg
c:\photos\dir1\eaDir_tmp\002.jpg\SYNOPHOTO_THUMB_B.jpg
c:\photos\dir1\eaDir_tmp\002.jpg\SYNOPHOTO_THUMB_M.jpg
c:\photos\dir1\eaDir_tmp\002.jpg\SYNOPHOTO_THUMB_PREVIEW.jpg
c:\photos\dir1\eaDir_tmp\002.jpg\SYNOPHOTO_THUMB_S.jpg
```

`eaDir_tmp` is used as a temporary directory name as @ characters are not valid in file names on Windows. Therefore these folders must be renamed to `@eaDir` for PhotoStation to recognize them. This renaming process must be done via SSH to the DiskStation unless the volume is mounted by NFS. Useful commands:

```
# remove any existing thumbnail directories, dry-run check print out before running next command!
find . -depth -type d -name 'eaDir_tmp' -execdir echo '{}' \;

# remove any existing thumbnail directories
find . -depth -type d -name 'eaDir_tmp' -execdir rm -rf '{}' \;

# rename directories
find . -depth -type d -name 'eaDir_tmp' -execdir mv '{}' @eaDir \;

```
