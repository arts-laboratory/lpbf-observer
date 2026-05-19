import functions as fun
import datetime
import time
import cv2
import numpy as np

fun.clear_terminal()

imager = fun.connect()

print("Current focus position:", imager.getFocusMotorPosition())

client = fun.CameraClient(imager)

imager.runAsync()  # starts grabbing frames in background

recording = False       
writer = None
record_start = None

cv2.namedWindow('Thermal Camera')
cv2.createTrackbar('Focus', 'Thermal Camera', int(imager.getFocusMotorPosition()), 100, lambda x: imager.setFocusMotorPosition(x))

while True:
    image = client.getImage()

    if image is not None:
        cv2.imshow('Thermal Camera (Press "q" to stop)', image)
    
        if recording:
            writer.write(image)
            elapsed = time.time() - record_start
            if elapsed >= 15:
                recording = False
                writer.release()
                writer = None
                print("Recording saved!")

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cv2.destroyAllWindows()
imager.stopRunning()
