from typing import Optional, List
from subprocess import run, PIPE
import json

# FFPROBE_INVALID_INPUT_ERROR = b"Invalid data found when processing input"
FFPROBE_ARGUMENTS = [
    "ffprobe",
    "-v",
    "error",
    "-show_entries",
    "stream=duration,codec_type",
    "-show_format",
    "-hide_banner",
    "-print_format",
    "json",
]


def resolve_duration(output: dict) -> Optional[int]:
    def calc_duration(duration: str) -> int:
        return int(float(duration) / 60)

    found_vid = False

    for stream in output["streams"]:
        codec = stream.get("codec_type", "")
        duration = stream.get("duration")
        if codec != "video":
            continue

        found_vid = True

        if duration is None:
            continue

        return calc_duration(duration)

    if not found_vid:
        return None

    format = output.get("format", {})
    duration = format.get("duration")
    if not format or duration is None:
        return None

    return calc_duration(output["format"]["duration"])


def run_ffprobe(path: str) -> tuple[str, str]:
    """
    Run ffprobe with with a given path and returns a tuple of the stdout and stderr.
    """
    args = FFPROBE_ARGUMENTS + ["-i", path]

    proc = run(args, stdout=PIPE, stderr=PIPE)
    return proc.stdout, proc.stderr


def read_time_from_file(path: str) -> Optional[int]:
    """
    Reads the length of a given file and returns it in minutes.

    The expected return is an int, however this is only if the file is a video. Images, text files etc. will return None.
    """
    ffprobe_stdout, ffprobe_stderr = run_ffprobe(path)
    if ffprobe_stderr != b"":  # TODO: Better error handling?
        #     if FFPROBE_INVALID_INPUT_ERROR in ffprobe_stderr:
        #         return
        return

    json_data = json.loads(ffprobe_stdout)
    return resolve_duration(json_data)
