import os 
from pathlib import Path
import cv2
import numpy as np
import re
from pytictoc import TicToc

#temp scale shit
low = 0
high = 250
time = TicToc()

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

def loadData(path, name):
    print(f"Loading {name}.")

    data = np.load(path)
    frames = data['frames']
    timestamp = data['timestamp']

    print(f"Loaded {frames.shape[0]} frames in {name}.")

    return frames, timestamp


def saveVideo(path, name, output):
    print(f"Producing video for {name}")
    time.tic()

    folder = Path(output) / name
    folder.mkdir(parents = True, exist_ok = True)

    frames, timestamp = loadData(path, name)
    totalFrames, height, width, lo, hig, fps = getFramesInfo(frames)

    writer = cv2.VideoWriter(str(folder / f"{name}.mp4"), cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height), isColor = True)
    
    for frame in frames:
        normalized = ((frame - lo) / (hig - lo) * 255).astype(np.uint8)
        color = cv2.applyColorMap(normalized, cv2.COLORMAP_INFERNO)
        writer.write(color)

    writer.release()

    time.toc()
    print(f"Saved → {folder}\n")
    

def getFramesInfo(frames):
    totalFrames, height, width = frames.shape
    low = frames.min()
    high = frames.max()
    fps = 80

    return totalFrames, height, width, low, high, fps





