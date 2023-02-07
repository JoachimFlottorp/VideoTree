from VideoTree import Folder, File
import json

def structure_output_as_json(folder: Folder, time_filter: int, indent: int = 0) -> str:
    def do(folder: Folder, time_filter: int, indent: int) -> list:
        out = []
        
        for file in folder.files:
            out.append({
                "type": "file",
                "name": file.name,
                "duration": file.time,
            })

        for child in folder.children:
            out.append({
                "type": "folder",
                "name": child.name,
                "children": do(child, time_filter, indent + 4)
            })
            
        return out

    return json.dumps(do(folder, time_filter, indent))