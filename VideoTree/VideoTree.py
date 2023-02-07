from __future__ import annotations
from . import Folder, File
from .file import read_time_from_file
import traceback
import os
import sys
from typing import Callable, Optional
from VideoTree import Folder


def read_file(path: str) -> Optional[File]:
    """
    Reads a file and returns a File object containing the name, path, time and extension of the file.

    Args:
        path (str): Full path to the file
    """
    name = os.path.basename(path)
    extension = os.path.splitext(path)[1]
    file = File(name, path, read_time_from_file(path), extension)
    if file.time is None:
        return None

    return file


def read_files_recurse(path: str, time_filter: int) -> Folder:
    """
    Reads through every folder recurseively in the given path.
    
    Args:
        path (str): Full path to the directory
        time_filter (int): Minimum time in minutes to be considered a match
        
    Returns:
        Folder: Folder object containing every video file and folder in the path and its subfolders
    """
    folders = []
    files = []

    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            folders.append(read_files_recurse(item_path, time_filter))
        else:
            try:
                file = read_file(item_path)
                if file is None:
                    continue # Ignore files that are not videos

                if file.time and file.time >= time_filter:
                    files.append(file)

            except Exception:
                print("Errror reading time from file: ", item_path, file=sys.stderr)
                print(traceback.format_exc(), file=sys.stderr)
                continue

    return Folder(os.path.basename(path), path, folders, files)

def remove_empty_folders(folder: Folder) -> None:
    """
    Removes empty folders from a Folder object.
    
    Args:
        folder (Folder): Folder object to remove empty folders from
    """
    for child in folder.children:
        remove_empty_folders(child)

    folder.children = [child for child in folder.children if len(child.files) > 0 or len(child.children) > 0]
    
    return folder
    
def videotree(path: str,  output_fn: Callable[[Folder, int, Optional[int]], str], time_filter: int = 20) -> str:
    rec_files = read_files_recurse(path, time_filter)
    remove_empty_folders(rec_files)
    
    return output_fn(rec_files, time_filter=time_filter)
