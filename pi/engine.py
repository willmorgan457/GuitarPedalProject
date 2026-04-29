import sounddevice as sd
import numpy as np
import pedalboard
import threading
from effects.reverb import ReverbEffect
from effects.delay import DelayEffect
from effects.neural_amp import NeuralAmpEffect
from effects.distortion import DistortionEffect

INPUT_DEVICE = 16
OUTPUT_DEVICE = 16

reverb = ReverbEffect()
reverb._plugin.wet_level = 0.8
reverb._plugin.room_size = 0.9

delay = DelayEffect()
neural_amp = NeuralAmpEffect("effects/MRSH SA100 I Edge BAL CAB.nam")
distortion = DistortionEffect()

reverb_on = False
delay_on = False
neural_on = False
distortion_on = False

def rebuild_board():
    plugins = []
    if distortion_on:
        plugins.append(distortion.get_plugin())
    if reverb_on:
        plugins.append(reverb.get_plugin())
    if delay_on:
        plugins.append(delay.get_plugin())
    return pedalboard.Pedalboard(plugins)
board = rebuild_board()

def callback(indata, outdata, frames, time, status):
    guitar = indata[:, 1:2]
    audio = guitar.T
    processed = board(audio, 48000, reset=False).T
    outdata[:, 0] = processed[:, 0]
    outdata[:, 1] = processed[:, 0]

def input_loop():
    global board, reverb_on, delay_on, neural_on, distortion_on
    while True:
        key = input()
        if key == '1':
            reverb_on = not reverb_on
            board = rebuild_board()
            print(f"Reverb: {'ON' if reverb_on else 'OFF'}")
        elif key == '2':
            delay_on = not delay_on
            board = rebuild_board()
            print(f"Delay: {'ON' if delay_on else 'OFF'}")
        elif key == '3':
            neural_on = not neural_on
            board = rebuild_board()
            print(f"Neural Amp: {'ON' if neural_on else 'OFF'}")
        elif key == '4':
            distortion_on = not distortion_on
            board = rebuild_board()
            print(f"Distortion: {'ON' if distortion_on else 'OFF'}")

def run_engine():
    asio_in = sd.AsioSettings(channel_selectors=[0, 1])
    asio_out = sd.AsioSettings(channel_selectors=[0, 1])
    t = threading.Thread(target=input_loop, daemon=True)
    t.start()
    with sd.Stream(
        device=(INPUT_DEVICE, OUTPUT_DEVICE),
        samplerate=48000,
        blocksize=32,
        dtype='float32',
        channels=(2, 2),
        callback=callback,
        extra_settings=(asio_in, asio_out),
    ):
        print("Audio engine running. Press 1=reverb, 2=delay, 3=neural amp, 4=distortion.")
        t.join()

if __name__ == "__main__":
    run_engine()