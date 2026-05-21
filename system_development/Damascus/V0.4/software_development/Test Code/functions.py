import sys
from pathlib import Path
import cv2

BASE_DIR = Path(__file__).resolve().parent

OPTRIS_PATH = BASE_DIR / "optris"

sys.path.insert(0, str(OPTRIS_PATH))

import optris.otcsdk as otc
import os
import numpy as np
import datetime
import time


def clear_terminal():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def connect(serialNumber=0):
    otc.Sdk.init(otc.Verbosity_Info, otc.Verbosity_Off, sys.argv[0])
    otc.EnumerationManager.getInstance().addEthernetDetector("192.168.0.0/24")

    imager = otc.IRImagerFactory.getInstance().create('native')
    imager.connect(serialNumber)

    return imager



class CameraClient(otc.IRImagerClient):
    def __init__(self, imager):
        super().__init__()
        self._imager = imager
        self._imager.addClient(self)
        self.recording = False
        self.recorded_frames = []   # RAM buffer: list of float32 temp maps
        self.recorded_timestamps = []
        self._latest_frame = None
        self._frame_updated = False
        self._builder = otc.ImageBuilder(
            colorFormat=otc.ColorFormat_BGR,
            widthAlignment=otc.WidthAlignment_OneByte
        )

    def onFrame(self, evt):
        self._latest_frame = evt.clone()
        self._frame_updated = True

        if self.recording:
            frame = self._latest_frame.thermalFrame
            h = frame.getHeight()
            w = frame.getWidth()

            # copyTemperaturesTo writes into a flat float32 array
            temp_flat = np.empty(h * w, dtype=np.float32)
            frame.copyTemperaturesTo(temp_flat)
            
            self.recorded_frames.append(temp_flat.reshape(h, w))
            self.recorded_timestamps.append(time.perf_counter_ns())

    def start_recording(self):
        """Clear the buffer and begin capturing thermal frames into RAM."""
        self.recorded_frames = []
        self.recorded_timestamps = []
        self.recording = True
        print("Recording started.")

    def stop_recording(self):
        """Stop capturing and return the collected frames."""
        self.recording = False
        frames = self.recorded_frames
        print(f"Recording stopped. {len(frames)} frames captured.")
        return frames

    def save_recording(self, save_dir=r"C:\Users\mayhe\OneDrive\Documents\GitHub\In-situ-monitoring-of-powder-bed-fusion-additive-manufacturing\system_development\Damascus\V0.4\software development\Recordings"):
        if not self.recorded_frames:
            print("No frames to save.")
            return None

        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(save_dir, f"thermal_{ts}.npz")
        
        stack = np.stack(self.recorded_frames, axis=0)
        np.savez_compressed(
            path,
            frames=stack,
            frame_timestamps_ns=np.array(self.recorded_timestamps, dtype=np.int64),
            timestamp=np.array(datetime.datetime.now().isoformat())
        )
        print(f"Saved {stack.shape[0]} frames → {path}")
        return path

    def getImage(self):
        """Return the latest BGR false-colour preview image, or None if not ready."""
        if self._latest_frame is None or not self._frame_updated:
            return None
        self._builder.setThermalFrame(thermalFrame=self._latest_frame.thermalFrame)
        self._builder.convertTemperatureToPaletteImage()
        image = np.empty(
            (self._builder.getHeight(), self._builder.getWidth(), 3),
            dtype=np.uint8
        )
        self._builder.copyImageDataTo(image)
        self._frame_updated = False
        
def seePreview(client, imager):
    while True: 
        image = client.getImage()

        if image is not None:
            cv2.imshow('Thermal Camera ("q" to quit)', image)
        
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            if client.recording:
                client.stop_recording()
            break