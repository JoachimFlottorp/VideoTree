from typing import Optional, List
from . import File
from subprocess import run, PIPE
from pydantic import BaseModel, parse_raw_as

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


class FFProbeStream(BaseModel):
    # The duration of the stream in seconds, can be None if the stream is a still image.
    duration: str | None
    # The codec type of the stream. This is either video or audio.
    codec_type: str


class FFProbeFormat(BaseModel):
    duration: Optional[str]


class FFProbeOutput(BaseModel):
    streams: List[FFProbeStream]
    format: FFProbeFormat


def resolve_duration(output: FFProbeOutput) -> Optional[int]:
    def calc_duration(duration: str) -> int:
        return int(float(duration) / 60)

    found_vid = False

    for stream in output.streams:
        if stream.codec_type != "video":
            continue

        found_vid = True

        if stream.duration is None:
            continue

        return calc_duration(stream.duration)

    if not found_vid:
        return None

    if output.format is None or output.format.duration is None:
        return None

    return calc_duration(output.format.duration)


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
    if ffprobe_stderr != b"": # TODO: Better error handling?
    #     if FFPROBE_INVALID_INPUT_ERROR in ffprobe_stderr:
    #         return
        return

    json = parse_raw_as(FFProbeOutput, ffprobe_stdout)
    return resolve_duration(json)
