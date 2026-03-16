import time 
import functionFIles as bruh

bruh.clear_terminal()

inputPath = r"C:\Users\mayhe\OneDrive\Documents\Thermal stuff\3_13_2026"
outputPath = r"C:\Users\mayhe\OneDrive\Documents\Dataset-battery-tab-laser-welding\data\Dataset-1\Footage"

raviFileNames = bruh.gimmeFileNames(inputPath)
raviFiles = bruh.buildFilePaths(inputPath)

for i, file in enumerate(raviFileNames):
    print(f"{i}: {file}")
    capture = bruh.captureVideo(raviFiles[i])
    bruh.makeVideo(capture, outputPath, raviFileNames[i], True, 188, 90, 125, 125)
    bruh.saveFrameCSV(capture, outputPath, raviFileNames[i], 350)

print("FINALLY DONE!")