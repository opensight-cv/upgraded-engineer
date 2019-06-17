import cv2
import shlex
import subprocess
from typing import Tuple

DEFAULT_SOCKET_PATH = "/tmp/engineering"
DEFAULT_EXEC = "/usr/local/bin/potential-engine"
DEFAULT_VIDEO_SIZE = (640, 480, 30)


class Engine:
    """
    Class which starts and manages a potential-engine process.
    """

    def __init__(
        self,
        socket_path: str = DEFAULT_SOCKET_PATH,
        engine_exec: str = DEFAULT_EXEC,
        video_size: Tuple[int, int, int] = DEFAULT_VIDEO_SIZE,
    ):
        launchline = "{exec_} -w {w} -h {h} -f {f} -d {sock} --shared_memory".format(
            exec_=engine_exec,
            w=video_size[0],
            h=video_size[1],
            f=video_size[2],
            sock=socket_path,
        )
        self.process = subprocess.Popen(shlex.split(launchline))


class EngineWriter(Engine):
    """
    Starts and writes data into an engine.
    """

    def __init__(
        self,
        socket_path: str = DEFAULT_SOCKET_PATH,
        engine_exec: str = DEFAULT_EXEC,
        video_size: Tuple[int, int, int] = DEFAULT_VIDEO_SIZE,
    ):
        super().__init__(socket_path, engine_exec, video_size)
        # pipeline, 0 (magic gst number), framerate, video dimensions tuple
        self.writer = cv2.VideoWriter(
            "appsrc ! videoconvert ! video/x-raw,format=I420 ! shmsink socket-path = {}".format(
                socket_path
            ),
            0,
            video_size[3],
            video_size[:2],
        )

    def write_frame(self, frame):
        """
        Write a frame into the engine. Call in a tight loop, you need to hit your given framerate!
        """
        self.writer.write(frame)