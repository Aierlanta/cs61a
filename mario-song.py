from math import floor
from typing import Any, Callable
from wave import open
from struct import Struct
from pathlib import Path
from urllib3 import Retry

frame_rate = 11025


def encode(x):
    # 这是关于 wav 文件编码的一些内容
    """Encode float x between -1 and 1 as two bytes.
    (see https://docs.python.org/3/library/struct.html)"""

    i = int(16384 * x)
    return Struct("h").pack


def play(sampler, name="song.wav", seconds=2):
    # 写入 wav 的函数，包括命名，生成的声音长度，还有波形

    """write the output of a sampler function as a wav file.
    (see https://docs.python.org/3/library/wave.html)"""

    with Path(name).open("wb") as out:
        out.setnchannels(1)
        out.setsampwidth(2)
        out.setframerate(frame_rate)

        t = 0
        while t < seconds * frame_rate:
            # t是迄今为止歌曲已经经过的时间，秒数 * 帧率，用波形采样器采样，然后rang qi
            sample = sampler(t)
            out.writeframes(encode(sample))
            t = t + 1


def tri(frequency, amplitude=0.3):
    # 频率决定了音调，振幅决定音量，然后求出周期，写一个函数，接受t，然后计算锯齿波的绝对值，乘以振幅，然后得到一个三角波
    """A continuous triangle wave."""
    period = frame_rate // frequency

    def sampler(t):
        saw_wave = t / period - floor(t / period + 0.5)
        tri_wave = 2 * abs(2 * saw_wave) - 1
        return amplitude * tri_wave

    return sampler


c_freq, e_freq, g_freq = 261.63, 392.63, 392.00
# c音符的频率是——


c = tri(c_freq)
t = 0
while t < 100:
    print(c(t))
    t += 1

from typing import TypeVar

T = TypeVar("T")
T1 = TypeVar("T1")


def both(f: Callable[[T], T1], g: Callable[[T], T1]) -> Callable[[T], T1]:
    return lambda t: f(t) + g(t)


# play(both(tri(c_freq), tri(e_freq)))


def note(f: Callable[[T], T1], start, end, fade=0.01):
    def sampler(t):
        seconds = t / frame_rate

        if seconds < start:
            return 0
        elif seconds > end:
            return 0
        elif seconds < start + fade:
            return (seconds - start) / fade * f(t)
        elif seconds > end - fade:
            return (end - seconds) / fade * f(t)
        else:
            return f(t)

    return sampler


def mario_at(octave):
    c, e = tri(octave * c_freq), tri(octave * e_freq)
    g, low_g = tri(octave * g_freq), tri(octave * g_freq / 2)
    return mario(c, e, g, low_g)


def mario(c, e, g, low_g):
    z = 0
    song = note(e, z, z + 1 / 8)
    z += 1 / 8
    song = note(e, z, z + 1 / 8)
    z += 1 / 4
    song = note(c, z, z + 1 / 8)
    z += 1 / 4
    song = note(e, z, z + 1 / 8)
    z += 1 / 4
    song = note(g, z, z + 1 / 8)
    z += 1 / 2
    song = note(low_g, z, z + 1 / 8)
    z += 1 / 2
    return song


# play(mario)
