import time
import numpy
import random
import ffmpeg
import aiohttp
from PIL import Image
from io import BytesIO
from .. import sayulog
from pyrogram import Client, filters
from ..__vars__ import human_hour_readable, TESTS_CHANNEL


class NamedBytesIO(BytesIO):
    def __init__(self, content: bytes, name: str) -> None:
        super().__init__(content)
        self.name = name


@Client.on_message(filters.command(["up"]))
async def __svst__(bot, update):
    print(update)
    sayulog.warning("NO SE SI FUNCIONARA!!!", extra={"hhr": human_hour_readable()})
    _fmbd = "https://www.fembed.com/v/xgmqxh571yg2m03"
    async with aiohttp.ClientSession() as request:
        async with request.get(_fmbd) as r1:
            _host = r1.host
        async with request.post(f"https://{_host}/api/source/" + _fmbd.split("/")[-1]) as r:
            rspns_json = await r.json()
            _orl = rspns_json["data"][-1]["file"]
        async with request.get(_orl) as r2:
            print(r2.headers)
            print(r2.request_info)
            print(r2.content_length)
            _start = time.time()
            _data = ffmpeg.probe(_orl)
            _data_of_video = [stream for stream in _data["streams"] if stream["codec_type"] == "video"][0]
            print(_data)
            print(_data_of_video)
            # DATA
            width = _data_of_video["width"]
            height = _data_of_video["height"]
            duration = int(_data_of_video["duration"])
            # total_frames = int(_data_of_video['nb_frames'])
            print("Waiting... {}".format(time.time() - _start))
            _ss = int(duration / random.randint(15, 30))
            frame, err = (
                ffmpeg.input(_orl, ss=_ss)
                .output('pipe:', vframes=1, format='image2', vcodec='png')    # vcodec=mjpeg || png
                .run(quiet=True)
                # .run(capture_stdout=True)
            )
            # nimage = Image.open(BytesIO(frame))
            # nimage.save("screenshot-0.png")
            # print(f"Waiting-2... {time.time() - _start} :3")

            # data = cv2.VideoCapture(_orl)
            # frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
            # fps = int(data.get(cv2.CAP_PROP_FPS))
            # seconds = int(frames / fps)
            # print(seconds)

            # clip = VideoFileClip(_orl)
            # Extraer información del video
            # width, height = clip.size
            # duration = int(clip.duration)
            print(width, height, duration)
            await bot.send_video(
                TESTS_CHANNEL,
                # NamedBytesIO(await r.content.read(), "file")
                BytesIO(await r2.content.read()),
                file_name="@Japanemision",
                duration=duration,
                width=width,
                height=height,
                thumb=BytesIO(frame)
            )

    # _orl = "https://cdn.donmai.us/original/39/27/__izayoi_sakuya_touhou__39279272c19a06b268fd40931ff29317.mp4"
    # async with aiohttp.ClientSession() as request:


