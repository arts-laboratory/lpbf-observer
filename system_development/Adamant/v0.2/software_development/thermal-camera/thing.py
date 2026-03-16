import numpy as np
import cv2
import functionFIles as ff

ff.clear_terminal()

ravi_file_name = 'Run1.ravi'
input = r"C:\Users\mayhe\OneDrive\Documents\Thermal stuff\3_13_2026"

cap = cv2.VideoCapture(str(input) + '\\' + ravi_file_name)  # Opens a video file for capturing

# Fetch undecoded RAW video streams
cap.set(cv2.CAP_PROP_FORMAT, -1)  # Format of the Mat objects. Set value -1 to fetch undecoded RAW video streams (as Mat 8UC1). [Using cap.set(cv2.CAP_PROP_CONVERT_RGB, 0) is not working]

cols  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # Get video frames width
rows = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # Get video frames height

while True:
    ret, frame = cap.read()  # Read next video frame (undecoded frame is read as long row vector).

    if not ret:
        break  # Stop reading frames when ret = False (after the last frame is read).

    # View frame as int16 elements, and reshape to cols x rows (each pixel is signed 16 bits)
    frame = frame.view(np.int16).reshape(rows, cols)

    # It looks like the first line contains some data (not pixels).
    # data_line = frame[0, :]
    frame_roi = frame[1:, :]  # Ignore the first row.

    # Normalizing frame to range [0, 255], and get the result as type uint8 (this part is used just for making the data visible).
    normed = cv2.normalize(frame_roi, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    color = cv2.applyColorMap(normed, cv2.COLORMAP_INFERNO)  # Apply a color map to the normalized frame for better visualization
        
    cv2.imshow('Color Mapped', color)  # Show the normalized video frame
    cv2.waitKey(10)

cap.release()
