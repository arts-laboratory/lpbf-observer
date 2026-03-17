import os 
from pathlib import Path
import cv2
import ffmpeg
import numpy as np


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

def converttoRAW(inputFile, outputFile):
    ffmpeg.input(inputFile).output(outputFile, format="rawvideo", pix_fmt="yuv420p").run()

def captureVideo(path):
    capture = cv2.VideoCapture(path)
    capture.set(cv2.CAP_PROP_FORMAT, -1)

    return capture

def readFrame(capture):
    ret, frame = capture.read()

    return ret, frame 
    
def makeVideo(capture, path, name, cropped, x, y, w, h):
    frameFolder = folderFind(path, name)
    count, fps, width, height = getVideoInfo(capture)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    colorWriter = cv2.VideoWriter(str(frameFolder / f"{name}.mp4"), fourcc, fps, (width, height), isColor=True)
    croppedWriter = cv2.VideoWriter(str(frameFolder / f"{name}Cropped.mp4"), fourcc, fps, (w, h), isColor=True)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))

    while True:
        ret, frame = readFrame(capture)
        if not ret:
            break
        
        #View frame as int16 elements, and reshape to cols x rows (each pixel is signed 16 bits)
        frame = frame.view(np.int16).reshape(height, width)

        # It looks like the first line contains some data (not pixels).
        # data_line = frame[0, :]
        frame_roi = frame[1:, :]  # Ignore the first row.

        # Normalizing frame to range [0, 255], and get the result as type uint8 (this part is used just for making the data visible).
        normed = cv2.normalize(frame_roi, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
        cl1 = clahe.apply(normed)
        nor = cv2.cvtColor(cl1, cv2.COLOR_GRAY2BGR)
        color = cv2.applyColorMap(nor, cv2.COLORMAP_INFERNO)  # Apply a color map to the normalized frame for better visualization
        cropped = cropROI(color, x, y, w, h)
        croppedWriter.write(cropped)
        colorWriter.write(color)
        count += 1
    
    colorWriter.release()
    print("Done!")

    
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

def saveFrameCSV(capture, outputPath, name, frameNumber=0, calibrationFile=None):
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
    frame = convertToTemperature(frame, calibrationFile)
    
    outPath = str(Path(outputPath) / f"{Path(name).stem}_frame{frameNumber}.csv")
    np.savetxt(outPath, frame, delimiter=",", fmt="%d")
    print(f"Saved: {outPath}")
    
def readCalibrationFile(calibrationFile):
    calibrationData = np.loadtxt(calibrationFile)
    
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