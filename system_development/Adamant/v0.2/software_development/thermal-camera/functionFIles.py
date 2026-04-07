import os 
from pathlib import Path
import cv2
import numpy as np
import re
import time

#temp scale shit
low = 20
high = 800

def clear_terminal():
    # Check the operating system
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For macOS and Linux
        os.system('clear')

def gimmeFileNames(path, includeFolders=False):
    folder = Path(path)
    if includeFolders:
        names = [item.name for item in folder.iterdir()]
    else:
        names = [file.name for file in folder.iterdir() if file.is_file()]
    return names

def buildFilePaths(path):
    fileNames = gimmeFileNames(path)
    filePath = []
    
    for files in fileNames:
        filePath.append(os.path.join(path, files))
        
    return filePath

def captureVideo(path):
    capture = cv2.VideoCapture(path)
    capture.set(cv2.CAP_PROP_FORMAT, -1)

    return capture

def readFrame(capture):
    ret, frame = capture.read()

    return ret, frame 
    
def makeVideo(capture, path, name, do_crop, x, y, w, h, calibration20_100, calibrationFile0_250, calibrationFile150_900):
    start = time.time()

    frameFolder = folderFind(path, name)
    count, fps, width, height = getVideoInfo(capture)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    colorWriter = cv2.VideoWriter(str(frameFolder / f"{name}.mp4"), fourcc, fps, (width, height - 1), isColor=True)
    croppedWriter = cv2.VideoWriter(str(frameFolder / f"{name}Cropped.mp4"), fourcc, fps, (w, h), isColor=True)
    maxMean = 0
    frameIndex = 0


    while True:
        ret, frame = readFrame(capture)
        if not ret:
            break

        frame = frame.view(np.int16).reshape(height, width)
        frame_roi = frame[1:, :]  # Strip metadata row

        # Convert raw values to temperature using combined calibration
        temp = convertToTemperatureExtended(frame_roi, calibration20_100, calibrationFile0_250, calibrationFile150_900)
        
        mean_temp = np.mean(temp)
        if mean_temp > maxMean:
            maxMean = mean_temp
            frame = frameIndex

        # Normalize temperature to [0, 255] for visualization
        scaled = np.clip(temp, low, high)
        scaled = ((scaled - low) / (high - low) * 255).astype(np.uint8)
        nor = cv2.cvtColor(scaled, cv2.COLOR_GRAY2BGR)
        color = cv2.applyColorMap(nor, cv2.COLORMAP_INFERNO)

        cropped = cropROI(color, x, y, w, h)
        croppedWriter.write(cropped)
        colorWriter.write(color)
        frameIndex += 1

    colorWriter.release()
    croppedWriter.release()
    end = time.time()

    print(f"Processed {count} frames in {end - start:.2f} seconds.")
    print(f"Max mean temperature: {maxMean:.2f} at frame {frame}")
    print("Done!")

    return frame

def folderFind(path, Name):
    folder = Path(path) / Name
    folder.mkdir(parents=True, exist_ok=True)
    
    return folder 

def getVideoInfo(capture):
    frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT) or 30)
    fps = capture.get(cv2.CAP_PROP_FPS)
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    return frame_count, fps, width, height

def cropROI(frame, cx, cy, w, h):
    x = cx - w // 2
    y = cy - h // 2
    return frame[y:y+h, x:x+w]

def saveFrameCSV(capture, outputPath, name, frameNumber=0, calibrationFile1=None, calibrationFile2=None, calibrationFile3=None):
    """Save a specific frame as CSV of raw int16 values"""
    capture.set(cv2.CAP_PROP_POS_FRAMES, frameNumber)
    ret, frame = capture.read()
    if not ret:
        print("Could not read frame")
        return
    
    frame = frame.view(np.int16).reshape(
        int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    )
    frame = frame[1:, :]  # remove metadata line
    frame = convertToTemperatureExtended(frame, calibrationFile1, calibrationFile2, calibrationFile3)
    
    outPath = str(Path(outputPath) / f"{Path(name).stem}_frame{frameNumber}.csv")
    np.savetxt(outPath, frame, delimiter=",", fmt="%d")
    print(f"Saved: {outPath} as {Path(name).stem}_frame{frameNumber}.csv")
    
def readCalibrationFile(calibrationFile):
    rows = []
    with open(calibrationFile, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = re.split(r'\s+|(?<=\d)(?=-)', line)
            if len(parts) == 2:
                rows.append((float(parts[0]), float(parts[1])))
    
    calibrationData = np.array(rows)
    
    floats = calibrationData[:, 0].astype(int)
    temperatures = calibrationData[:, 1]

    return floats, temperatures

def interpolateTemp(values, floats, temperatures):
    """Interpolate temperature values based on the calibration data"""
    return np.interp(values, floats, temperatures)

def convertToTemperature(frame,calibrationFile):
    """Convert raw frame values to temperature using interpolation"""
    floats, temperatures = readCalibrationFile(calibrationFile)
    return interpolateTemp(frame, floats, temperatures)

def convertToTemperatureExtended(frame, calibration20_100, calibrationFile0_250, calibrationFile150_900):
    floats20_100, temps20_100 = readCalibrationFile(calibration20_100)
    floats0_250, temps0_250 = readCalibrationFile(calibrationFile0_250)
    floats150_900, temps150_900 = readCalibrationFile(calibrationFile150_900)

    interp20_100 = interpolateTemp(frame, floats20_100, temps20_100)
    interp0_250 = interpolateTemp(frame, floats0_250, temps0_250)
    interp150_900 = interpolateTemp(frame, floats150_900, temps150_900)

    result = np.maximum.reduce([interp20_100, interp0_250, interp150_900])

    return result 
