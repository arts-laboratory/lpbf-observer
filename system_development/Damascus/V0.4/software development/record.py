"""
record.py — live thermal preview with on-demand recording.

Controls
--------
  r  — start recording thermal frames into RAM
  s  — stop recording and save to a .npz file
  q  — quit

The saved .npz contains:
  frames    : float32 array (N, H, W) of temperatures in °C
  timestamp : ISO string
"""

import time
import cv2
import numpy as np
import functions as fun

fun.clear_terminal()

imager = fun.connect()
print("Focus position:", imager.getFocusMotorPosition())

client = fun.CameraClient(imager)
imager.runAsync()

cv2.namedWindow('Thermal Camera')
cv2.createTrackbar(
    'Focus', 'Thermal Camera',
    int(imager.getFocusMotorPosition()), 100,
    lambda x: imager.setFocusMotorPosition(x)
)

print("Press  r = record | s = stop & save | q = quit")

while True:
    image = client.getImage()

    if image is not None:
        # Burn a small REC indicator into the preview when recording
        if client.recording:
            n = len(client.recorded_frames)
            cv2.circle(image, (12, 12), 8, (0, 0, 220), -1)
            cv2.putText(image, f"REC {n}", (24, 17),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 220), 1, cv2.LINE_AA)

        cv2.imshow('Thermal Camera (r=rec  s=stop+save  q=quit)', image)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('r'):
        if not client.recording:
            client.start_recording()
        else:
            print("Already recording — press s to stop.")

    elif key == ord('s'):
        if client.recording:
            client.stop_recording()
            client.save_recording()   # saves thermal_YYYYMMDD_HHMMSS.npz
        else:
            print("Not currently recording.")

    elif key == ord('q'):
        if client.recording:
            client.stop_recording()
        break

cv2.destroyAllWindows()
imager.stopRunning()
