#!/usr/bin/env python3

import argparse
import os
from typing import List, Tuple, Set

FS_NTFS = 'ntfs'
FS_EXFAT = 'exfat'
FS_EXT = 'ext'
FILESYSTEMS_SUPPORTED = [FS_NTFS, FS_EXFAT, FS_EXT]

EXT_PROHIBITED_SYMBOLS = {'/'}
WIN_PROHIBITED_SYMBOLS = {'/', '\\', ':', '*', '?', '"', '<', '>', '|'}
WIN_PROHIBITED_NAMES = ['CON', 'PRN', 'AUX', 'CLOCK$', 'NUL']
WIN_PROHIBITED_NAMES.extend([f'COM{i}' for i in range(1, 10)])
WIN_PROHIBITED_NAMES.extend([f'LPT{i}' for i in range(1, 10)])

def _get_vars_from_kwargs(**kwargs) -> Tuple[str]:
    filename = kwargs['filename']
    path = kwargs['path']
    filesystems = ', '.join(kwargs['fs'])
    siblings = kwargs['siblings']
    full_path = os.path.sep.join([path, filename])
    return filename, path, filesystems, siblings, full_path

def _linux_filename_limit(**kwargs) -> str:
    pass

def _windows_filename_limit(**kwargs) -> str:
    pass

def _path_length_limit(**kwargs) -> str:
    pass

def _symbols_not_allowed(full_path: str, filename: str, fs: str, prohibited_set: Set[str]) -> str:
    prohibited = set(filename) & prohibited_set
    if prohibited:
        return f"{full_path} contains \"{''.join(prohibited)}\", which isn't allowed on {fs}"

def _win_symbols_not_allowed(**kwargs) -> str:
    filename, _, fs, _, full_path = _get_vars_from_kwargs(**kwargs)
    return _symbols_not_allowed(full_path, filename, fs, WIN_PROHIBITED_SYMBOLS)

def _ext_symbols_not_allowed(**kwargs) -> str:
    filename, _, fs, _, full_path = _get_vars_from_kwargs(**kwargs)
    return _symbols_not_allowed(full_path, filename, fs, EXT_PROHIBITED_SYMBOLS)

def _win_names_not_allowed(**kwargs) -> str:
    filename, _, fs, _, full_path = _get_vars_from_kwargs(**kwargs)
    if filename.upper() in WIN_PROHIBITED_NAMES:
        return f"{full_path} is a reserved name on {fs}"

def _case_insensitive(**kwargs) -> str:
    filename, _, fs, siblings, full_path = _get_vars_from_kwargs(**kwargs)
    if filename.lower() in map(lambda x: x.lower(), siblings):
        return f"{full_path} has case-insensitive duplicate filenames in the same directory, which isn't allowed on {fs}"

NTFS_AND_EXFAT_COMMON_RESTRICTIONS = [_case_insensitive, _win_names_not_allowed, _win_symbols_not_allowed]

RESTRICTIONS = {
    FS_NTFS: NTFS_AND_EXFAT_COMMON_RESTRICTIONS,
    FS_EXFAT: NTFS_AND_EXFAT_COMMON_RESTRICTIONS,
    FS_EXT: [_ext_symbols_not_allowed]
}

def check_all(directory: str, filesystems: list[str] = FILESYSTEMS_SUPPORTED, silent: bool = False) -> List[str]:
    def _get_checks():
        checks = {}
        for fs in filesystems:
            for check in RESTRICTIONS[fs]:
                if check.__name__ in checks:
                    checks[check.__name__]['fs'].append(fs)
                else:
                    checks[check.__name__] = {'fun': check, 'fs': [fs]}
        return list(checks.values())

    checks = _get_checks()

    def _check_file(path: str, filename: str, siblings: List[str]) -> List[str]:
        if os.path.islink(os.path.sep.join([path, filename])):
            return []

        results = []
        nonlocal checks
        for check in checks:
            check_result = check['fun'](path=path, filename=filename, siblings=siblings, fs=check['fs'])
            if check_result:
                results.append(check_result)
        return results

    def _walk_directory(current_path: str, dirname: str, siblings: List[str]) -> List[str]:
        results = _check_file(current_path, dirname, siblings)
        for path, dirs, files in os.walk(os.path.sep.join([current_path, dirname])):
            siblings = dirs + files
            for f in siblings:
                file_checks = _check_file(path, f, filter(lambda x: x != f, siblings))
                if file_checks:
                    results.extend(file_checks)
        return results

    def print_results(results: List[str]):
        print(f"Results of checking {directory} for compatibility issues with {', '.join(filesystems)}:")
        for result in results:
            print(result)

    if not (os.path.exists(directory) and os.path.isdir(directory)):
        print(f"{directory} isn't a directory")
        return 1

    path, dirname = os.path.split(directory)
    print_results(_walk_directory(path, dirname, []))

def main():
    parser = argparse.ArgumentParser(prog='dir_compat',
                                     description='Directory compatibility checker, ignores symbolic links')
    parser.add_argument('-d', '--directory', help='Directory to check for compatibility', required=True)
    parser.add_argument('-f', '--filesystems', help='Filesystems to check compatibility with', choices=FILESYSTEMS_SUPPORTED, default=FILESYSTEMS_SUPPORTED)
    args = vars(parser.parse_args())
    check_all(**args)

if __name__ == "__main__":
    main()
