import os
from VideoTree import Folder, File

CHECKMARK_UNICODE = "\u2705"
LINE_CHAR = "-"


def structure_output_as_text(folder: Folder) -> str:
    def do(folder: Folder, indent: int = 0) -> str:
        out = ""

        for file in folder.files:
            out += f"{LINE_CHAR * indent} {file.name} Found match: {CHECKMARK_UNICODE} {str(file.time)} minutes{os.linesep}"

        for child in folder.children:
            out += f" {LINE_CHAR * indent} {child.name}{os.linesep}"
            out += do(child, indent + 4)

        return out

    final = folder.path + os.linesep

    final += do(folder)

    return final
