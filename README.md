## VideoTree

A simple python script for finding video files in a directory that are longer than a certain length in minutes.

### Usage

VideoTree supports displaying the result in a human readable format or in a JSON format.

```bash
git clone https://github.com/JoachimFlottorp/VideoTree.git

cd VideoTree
```

###### Pre-Requirements

- Python 3.10 or higher
- [FFprobe](https://ffmpeg.org/) in your PATH

###### Windows

```ps1
py -m pip install -r requirements.txt
```

###### Linux

```bash
python3 -m pip install -r requirements.txt
```

#### Help Page

```bash
python3 run.py -h

usage: run.py [-h] [-f FILTER] [-j] path

positional arguments:
  path                  Path to the directory

options:
  -h, --help            show this help message and exit
  -f FILTER, --filter FILTER
                        Filter videos by length equal or greater than the given value in minutes
  -j, --json            Output as json

```

###### Basic Human Readable

```bash
python run.py ./testdata/Movie/ -f 1
/testdata/Movie
  avi
---- AlienPls.avi Found match: ✅ 3 minutes
  mkv
 ---- 1
-------- AlienPls.mkv Found match: ✅ 3 minutes
 ---- 2
-------- AlienPls.mkv Found match: ✅ 3 minutes
  mov
---- AlienPls.mov Found match: ✅ 3 minutes
  mp4
---- AlienPls.mp4 Found match: ✅ 3 minutes

```

###### JSON

This can be used with [jq](https://stedolan.github.io/jq/) to filter the output.
However, i won't show an example as that is too complicated for me. 😄

```bash
python3 run.py testdata/Movie -f 1 -j | jq
[
  {
    "type": "folder",
    "name": "avi",
    "children": [
      {
        "type": "file",
        "name": "AlienPls.avi",
        "duration": 3
      }
    ]
  },
  {
    "type": "folder",
    "name": "mkv",
    "children": [
      {
        "type": "folder",
        "name": "1",
        "children": [
          {
            "type": "file",
            "name": "AlienPls.mkv",
            "duration": 3
          }
        ]
      },
      {
        "type": "folder",
        "name": "2",
        "children": [
          {
            "type": "file",
            "name": "AlienPls.mkv",
            "duration": 3
          }
        ]
      }
    ]
  },
  {
    "type": "folder",
    "name": "mov",
    "children": [
      {
        "type": "file",
        "name": "AlienPls.mov",
        "duration": 3
      }
    ]
  },
  {
    "type": "folder",
    "name": "mp4",
    "children": [
      {
        "type": "file",
        "name": "AlienPls.mp4",
        "duration": 3
      }
    ]
  }
]
```
