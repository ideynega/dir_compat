# Directory compatibility checker

## Getting started
A small command-line utility to check if a directory you'd like to copy to another filesystem doesn't violate its limitations, only NTFS, exFAT, EXT4 (also when protected by ecryptfs) are supported. Script isn’t filesystem-aware and doesn’t operate on a low level, what it does is analysing existing directories and files at a given location on existing filesystem. Main purpose was to avoid issues while making backups. Doesn't require escalated privileges, but doesn't handle files you don't have access to. Doesn't handle symlinks to avoid dealing with loops.

## Installation
WIP

## Usage
 ```sh
./run.py --help
usage: dir_compat [-h] -d DIRECTORY
                  [-f {ntfs,exfat,ext4,ecryptfs} [{ntfs,exfat,ext4,ecryptfs} ...]]

Directory compatibility checker, ignores symbolic links and files inaccessible
due to permissions

options:
  -h, --help            show this help message and exit
  -d DIRECTORY, --directory DIRECTORY
                        Directory to check for compatibility
  -f {ntfs,exfat,ext4,ecryptfs} [{ntfs,exfat,ext4,ecryptfs} ...], --filesystems {ntfs,exfat,ext4,ecryptfs} [{ntfs,exfat,ext4,ecryptfs} ...]
                        Filesystems to check compatibility with
```

 ```sh
./run.py -d ~/directory1
Results of checking /home/username/directory1 for compatibility issues with ntfs, exfat, ext4, ecryptfs:
Checked 0 directorires and 15 files.
No issues found.
 ```

 ```sh
 ./run.py -d ~/directory2 -f ntfs exfat
Results of checking /home/username/directory2 for compatibility issues with ntfs, exfat:
Checked 8 directorires and 19 files.
/home/username/directory2/.dir2 has case-insensitive duplicate filenames in the same directory, which isn't allowed on ntfs, exfat
/home/username/directory2/.DIR2 has case-insensitive duplicate filenames in the same directory, which isn't allowed on ntfs, exfat
/home/username/directory2/CLOCK$ is a reserved name on ntfs, exfat
/home/username/directory2/file1? contains "?", which isn't allowed on ntfs, exfat
/home/username/directory2/.dir2/CON is a reserved name on ntfs, exfat
/home/username/directory2/.dir2/file2* contains "*", which isn't allowed on ntfs, exfat
/home/username/directory2/dir1/.file1> contains ">", which isn't allowed on ntfs, exfat
/home/username/directory2/dir1/file1< contains "<", which isn't allowed on ntfs, exfat
/home/username/directory2/dir1/dir3/.file1> contains ">", which isn't allowed on ntfs, exfat
/home/username/directory2/dir1/dir3/dir4/dir5\ contains "\", which isn't allowed on ntfs, exfat
/home/username/directory2/dir1/dir3/dir4/file4_a has case-insensitive duplicate filenames in the same directory, which isn't allowed on ntfs, exfat
/home/username/directory2/dir1/dir3/dir4/file4_A has case-insensitive duplicate filenames in the same directory, which isn't allowed on ntfs, exfat
 ```